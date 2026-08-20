#!/usr/bin/env python3
"""
Validate the filled translation packets and merge them into the deliverable
tests/<id>/詳細解説.<lang>.json.

    python3 .agents/exam-answer-translation/scripts/merge_translation.py \
        tests/20260807_1 --lang vi
    make merge-translation 20260807_1 TLANG=vi

The merge is the gate, not a concatenation. It refuses to write while any of
these is true — each is a way a half-done translation has of looking finished:

  * a packet listed in meta.json has no chunk-NN.target.json beside it, or the
    target holds an item the packet does not (a renumbered paper, a stray edit)
  * the item set does not exactly match 詳細解説.json's
  * any target string is empty, or an array is shorter/longer than its source
  * a target is character-for-character its Japanese source (untranslated
    paste). points entries only warn: a one-word 語彙 entry can legitimately
    keep its Japanese head-word.
  * 詳細解説.json changed since the packets were scaffolded (digest mismatch) —
    the explanations were edited underneath the translation, so at least the
    changed items must be re-translated. --allow-stale-source overrides it
    only after you have re-read the diff.
  * the language's UI labels (.agents/exam-answer-translation/ui/<lang>.json)
    are missing or still carry template Japanese.

On success it writes 詳細解説.<lang>.json: `_meta` (lang, label, ui, digest of
the Japanese source it was made from) plus one entry per item, with each
deduplicated passage/script translation expanded back onto every item that
referenced it. Then rebuild the page: `make model-answer <id>`.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
UI_DIR = ROOT / ".agents/exam-answer-translation/ui"


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_ui(lang: str, errors: list) -> dict:
    ui_path = UI_DIR / f"{lang}.json"
    template = json.loads((UI_DIR / "_template.json").read_text(encoding="utf-8"))
    template.pop("_comment", None)
    if not ui_path.is_file():
        errors.append(f"missing {ui_path.relative_to(ROOT)} — scaffold it and translate its values")
        return {}
    ui = json.loads(ui_path.read_text(encoding="utf-8"))
    ui.pop("_comment", None)
    missing = [k for k in template if k not in ui]
    if missing:
        errors.append(f"{ui_path.relative_to(ROOT)}: missing UI key(s) {missing}")
    untranslated = [k for k, v in template.items() if ui.get(k) == v]
    if untranslated:
        errors.append(f"{ui_path.relative_to(ROOT)}: still the Japanese template for {untranslated}")
    if "{n}" in template.get("question_label", "") and "{n}" not in ui.get("question_label", ""):
        errors.append(f"{ui_path.relative_to(ROOT)}: question_label lost its {{n}} placeholder")
    return ui


def merge(test_dir: Path, lang: str, allow_stale: bool) -> Path:
    test_dir = Path(test_dir).resolve()
    src_path = test_dir / "詳細解説.json"
    work = test_dir / "_translation" / lang
    meta_path = work / "meta.json"
    if not meta_path.is_file():
        raise SystemExit(f"no {meta_path} — run scaffold_translation.py first")

    raw = src_path.read_text(encoding="utf-8")
    source = json.loads(raw)
    source.pop("_meta", None)
    meta = json.loads(meta_path.read_text(encoding="utf-8"))

    errors: list[str] = []
    warnings: list[str] = []

    if meta.get("source_sha256") != digest(raw):
        msg = (f"詳細解説.json changed since the packets were scaffolded — re-translate the "
               f"edited items (or re-scaffold with --force)")
        (warnings if allow_stale else errors).append(msg)

    ui = load_ui(lang, errors)

    shared: dict[str, dict] = {}
    items: dict[str, dict] = {}
    refs: dict[str, dict] = {}
    for name in meta.get("chunks", []):
        packet_path = work / name
        target_path = work / name.replace(".json", ".target.json")
        if not packet_path.is_file():
            errors.append(f"missing packet {name}")
            continue
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
        for key, entry in (packet.get("items") or {}).items():
            if key in refs:
                errors.append(f"{name}: item {key} also appears in an earlier packet")
            refs[key] = entry
        if not target_path.is_file():
            errors.append(f"{target_path.name} not written — packet {name} is untranslated")
            continue
        try:
            target = json.loads(target_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{target_path.name}: does not parse — {exc}")
            continue

        tgt_shared = target.get("shared") or {}
        for ref, block in (packet.get("shared") or {}).items():
            text = (tgt_shared.get(ref) or "").strip()
            if not text:
                errors.append(f"{target_path.name}: shared {ref} ({block.get('kind')}) not translated")
            elif text == (block.get("source") or "").strip():
                errors.append(f"{target_path.name}: shared {ref} is a verbatim copy of the source")
            shared[ref] = {"kind": block.get("kind"), "target": text}
        for ref in tgt_shared:
            if ref not in (packet.get("shared") or {}):
                errors.append(f"{target_path.name}: shared {ref} is not in packet {name}")

        tgt_items = target.get("items") or {}
        for key in packet.get("items") or {}:
            if key not in tgt_items:
                errors.append(f"{target_path.name}: item {key} missing")
        for key, entry in tgt_items.items():
            if key not in (packet.get("items") or {}):
                errors.append(f"{target_path.name}: item {key} is not in packet {name}")
                continue
            items[key] = entry

    missing = [k for k in source if k not in items]
    extra = [k for k in items if k not in source]
    if missing:
        errors.append(f"{len(missing)} item(s) absent from the packets: {missing[:8]}")
    if extra:
        errors.append(f"item(s) the source does not have: {extra[:8]}")

    merged: dict[str, dict] = {}
    for key in source:
        tgt = items.get(key)
        if tgt is None:
            continue
        src = source[key]
        out: dict[str, object] = {}

        why = (tgt.get("why_correct") or "").strip()
        if not why:
            errors.append(f"item {key}: why_correct not translated")
        elif why == (src.get("why_correct") or "").strip():
            errors.append(f"item {key}: why_correct is a verbatim copy of the Japanese source")
        out["why_correct"] = why

        for field, verbatim_is_error in (("options_analysis", True), ("points", False)):
            src_list = list(src.get(field) or [])
            tgt_list = list(tgt.get(field) or [])
            if len(tgt_list) != len(src_list):
                errors.append(f"item {key}: {field} has {len(tgt_list)} entries, source has {len(src_list)}")
            clean = []
            for i, value in enumerate(tgt_list, 1):
                value = (value or "").strip()
                if not value:
                    errors.append(f"item {key}: {field}[{i}] not translated")
                elif i <= len(src_list) and value == (src_list[i - 1] or "").strip():
                    note = f"item {key}: {field}[{i}] is a verbatim copy of the Japanese source"
                    (errors if verbatim_is_error else warnings).append(note)
                clean.append(value)
            out[field] = clean

        for kind in ("passage", "script"):
            if not src.get(kind):
                continue
            ref = (refs.get(key) or {}).get(f"{kind}_ref")
            block = shared.get(ref or "")
            if not block:
                errors.append(f"item {key}: {kind} has no translated shared text (ref {ref!r})")
                continue
            out[kind] = block["target"]

        merged[key] = out

    if errors:
        print(f"✗ {test_dir.name} [{lang}]: {len(errors)} problem(s); nothing written\n")
        for e in errors[:40]:
            print(f"  - {e}")
        if len(errors) > 40:
            print(f"  … and {len(errors) - 40} more")
        raise SystemExit(1)

    out_path = test_dir / f"詳細解説.{lang}.json"
    payload = {
        "_meta": {
            "lang": lang,
            "label": meta.get("label") or lang,
            "html_lang": lang,
            "source_sha256": digest(raw),
            "ui": ui,
        }
    }
    payload.update(merged)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for w in warnings:
        print(f"  WARN  {w}")
    print(f"✓ {out_path.relative_to(ROOT)} — {len(merged)} items, "
          f"{len(shared)} passage/script translation(s)")
    print(f"  next: make model-answer {test_dir.name}")
    return out_path


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("test_dir", help="path to the test directory (e.g. tests/20260807_1)")
    ap.add_argument("--lang", required=True, help="target language code (e.g. vi)")
    ap.add_argument("--allow-stale-source", action="store_true",
                    help="downgrade the 詳細解説.json digest mismatch to a warning")
    args = ap.parse_args()
    merge(Path(args.test_dir), args.lang, args.allow_stale_source)


if __name__ == "__main__":
    sys.exit(main())
