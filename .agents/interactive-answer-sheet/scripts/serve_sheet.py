#!/usr/bin/env python3
"""
ONE server for every test in tests/ — the three screens of the exam app:

  screen 1  GET  /                          the test list + per-test progress
  screen 2  GET  /tests/<id>/解答.html      the exam itself (built by build_interactive.py)
  screen 3  (in page, after 「採点する」)     the result view, with a 「一覧へ戻る」 button

It saves as you go, into tests/<id>/:
  - each radio selection → ユーザー解答.json        (POST /api/tests/<id>/answers)
  - 「採点する」          → 採点結果.json + ユーザー解答.json (POST /api/tests/<id>/submit)
  - 「結果を削除」 on the list → deletes both JSON files (POST /api/tests/<id>/clear)

There is no per-test server any more: `make serve` takes no test id, and screen 1
reads the two JSON files above to show how far each test has got.

Usage:
    python3 .agents/interactive-answer-sheet/scripts/serve_sheet.py
    # or: make serve
"""
import argparse
import html
import importlib.util
import json
import re
import socket
import sys
import urllib.parse
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TESTS = ROOT / "tests"

# Screen 1's chrome is the SAME stylesheet 解答.html uses for screens 2 and 3.
# Imported, never copied — see app_style.py.
_style_spec = importlib.util.spec_from_file_location(
    "app_style", Path(__file__).resolve().with_name("app_style.py"))
app_style = importlib.util.module_from_spec(_style_spec)
_style_spec.loader.exec_module(app_style)

# 71 言語知識・読解 + 30 聴解. `make check` asserts 解答.html carries exactly this
# many radio groups, so it is safe to use as the progress denominator.
QUESTION_COUNT = 101

RANGE_RE = re.compile(r"^bytes=(\d*)-(\d*)$")
# /api/tests/<id>/answers | /api/tests/<id>/submit | /api/tests/<id>/clear
API_RE = re.compile(r"^/api/tests/([^/]+)/(answers|submit|clear)$")
SHEET = "解答.html"
ANSWERS_JSON = "ユーザー解答.json"
RESULT_JSON = "採点結果.json"


# ------------------------------------------------------------ test discovery
def natural_key(name: str):
    """`10` sorts after `9`; imported-* after plain ids; other names last."""
    if name.isdigit():
        return (0, int(name), "")
    if name.startswith("imported-"):
        return (1, 0, name)
    return (2, 0, name)


def test_origin(test_id: str) -> str:
    """Folder-name origin flag: ``imported-`` prefix ⇒ imported; else generated."""
    return "imported" if test_id.startswith("imported-") else "generated"


def test_dir(test_id: str) -> Path | None:
    """Resolve a test id to its directory, refusing anything outside tests/."""
    if not test_id or "/" in test_id or "\\" in test_id or test_id.startswith("."):
        return None
    d = (TESTS / test_id).resolve()
    if d.is_dir() and d.parent == TESTS.resolve():
        return d
    return None


def progress_of(d: Path) -> dict:
    """How far this test has got, read straight off the two saved JSON files."""
    answered = 0
    ua = d / ANSWERS_JSON
    if ua.is_file():
        try:
            data = json.loads(ua.read_text(encoding="utf-8"))
            for half in ("言語知識_読解", "聴解"):
                answered += sum(1 for v in (data.get(half) or {}).values() if v is not None)
        except (json.JSONDecodeError, OSError):
            answered = 0

    result = None
    rj = d / RESULT_JSON
    if rj.is_file():
        try:
            res = json.loads(rj.read_text(encoding="utf-8"))
            summary = res.get("summary", {})
            result = {
                "passed": bool(summary.get("passed")),
                "total_scaled_score": summary.get("total_scaled_score"),
                "max_scaled_score": summary.get("max_scaled_score", 180),
                "graded_at": res.get("graded_at"),
            }
        except (json.JSONDecodeError, OSError):
            result = None

    return {
        "id": d.name,
        "origin": test_origin(d.name),
        "answered": answered,
        "total": QUESTION_COUNT,
        "has_sheet": (d / SHEET).is_file(),
        "has_audio": (d / "聴解.mp3").is_file(),
        "result": result,
    }


def all_tests() -> list[dict]:
    if not TESTS.is_dir():
        return []
    dirs = [d for d in TESTS.iterdir()
            if d.is_dir() and ((d / SHEET).is_file() or (d / "言語知識・読解.md").is_file())]
    return [progress_of(d) for d in sorted(dirs, key=lambda p: natural_key(p.name))]


# --------------------------------------------------------- screen 1: the list
INDEX_CSS = """
*{box-sizing:border-box}
body{margin:0;background:#f8fafc;color:var(--ink);font-family:var(--ui)}
/* Wider than exam/result (60em): cards with many action buttons need the room. */
main{max-width:80em;margin:0 auto;padding:1.4em 1.2em 4em}
.lede{margin:0 0 1.4em;font-size:10.5pt;color:var(--muted)}
/* Equal card height. Meter uses display:contents so the track shares a row with
   the status chip (left-aligned); the lbl sits on the row under the track —
   flex + align-items:center was optically centering the whole meter block and
   made the bar look offset from the chip. */
.card{display:grid;grid-template-columns:20em auto minmax(12em,1fr) auto auto;
  grid-template-rows:1fr auto;column-gap:1em;row-gap:.2em;align-items:center;
  background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:.55em 1.2em;
  margin-bottom:.9em;box-sizing:border-box;height:5.1em;min-height:5.1em;
  max-height:5.1em;overflow:hidden}
.card h2{grid-column:1;grid-row:1/-1;margin:0;font-size:13pt;min-width:0;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;align-self:center}
.card .origin{grid-column:2;grid-row:1/-1;align-self:center}
.card .meter{display:contents}
.card .meter .track{grid-column:3;grid-row:1;align-self:center;width:100%;min-width:0}
.card .meter .lbl{grid-column:3;grid-row:2;text-align:left;margin:0;line-height:1.2;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.card .status{grid-column:4;grid-row:1/-1;align-self:center}
.acts{grid-column:5;grid-row:1/-1;display:flex;flex-wrap:nowrap;gap:.4em;
  align-self:center}
.acts .ui-btn{padding:.35em .75em;font-size:10.5pt;white-space:nowrap}
.empty{background:#fff;border:1px dashed var(--line);border-radius:10px;padding:2em;
  text-align:center;color:var(--muted)}
code{background:#f1f5f9;padding:.1em .4em;border-radius:4px;font-size:10pt}
.badge.origin-imp{background:#e0f2fe;color:#0369a1;border:1px solid #bae6fd}
.badge.origin-gen{background:#f1f5f9;color:#475569;border:1px solid #e2e8f0}
"""


def meter_html(t: dict) -> str:
    answered, total = t["answered"], t["total"]
    ratio = 0 if not total else min(100, round(answered / total * 100))
    fill = "fill done" if answered >= total else "fill"
    return (f'<div class="meter"><div class="track">'
            f'<div class="{fill}" style="width:{ratio}%"></div></div>'
            f'<div class="lbl">解答済み {answered} / {total}（{ratio}%）</div></div>')


def origin_badge_html(t: dict) -> str:
    if t.get("origin") == "imported":
        return '<span class="badge origin-imp">imported</span>'
    return '<span class="badge origin-gen">generated</span>'


def badge_html(t: dict) -> str:
    if not t["has_sheet"]:
        return '<span class="badge warn">解答.html 未生成</span>'
    r = t["result"]
    if not r:
        return '<span class="badge none">未採点</span>'
    cls = "pass" if r["passed"] else "fail"
    label = "合格" if r["passed"] else "不合格"
    return (f'<span class="badge {cls}">{label} '
            f'{r["total_scaled_score"]} / {r["max_scaled_score"]}</span>')


def card_html(t: dict) -> str:
    tid = html.escape(t["id"])
    tid_js = html.escape(t["id"], quote=True)
    base = "/tests/" + urllib.parse.quote(t["id"]) + "/" + urllib.parse.quote(SHEET)
    if t["has_sheet"]:
        if t["result"]:
            # Already graded: the result view is the default destination, but the
            # exam is one click away and keeps the saved answers, so it can be redone.
            acts = [f'<a class="ui-btn primary" href="{base}?screen=result">結果を見る</a>',
                    f'<a class="ui-btn" href="{base}">もう一度解く</a>']
        else:
            label = "続きから" if t["answered"] else "受験する"
            acts = [f'<a class="ui-btn primary" href="{base}">{label}</a>']
    else:
        acts = [f'<a class="ui-btn" href="#" onclick="return false" '
                f'title="make sheet {tid} を実行">受験する</a>']
    # Clear progress whenever either file exists — graded or mid-exam.
    if t["result"] or t["answered"]:
        acts.append(
            f'<button type="button" class="ui-btn danger" '
            f'data-clear="{tid_js}">結果を削除</button>')
    return (f'<div class="card"><h2 title="テスト {tid}">テスト {tid}</h2>'
            f'<span class="origin">{origin_badge_html(t)}</span>'
            f'{meter_html(t)}'
            f'<span class="status">{badge_html(t)}</span>'
            f'<div class="acts">{"".join(acts)}</div></div>')


INDEX_JS = """
async function clearTestProgress(id){
  if (!confirm('テスト「' + id + '」の採点結果と保存済みの解答を削除しますか？\\n'
             + 'この操作は元に戻せません。')) return;
  try {
    const r = await fetch('/api/tests/' + encodeURIComponent(id) + '/clear', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: '{}'
    });
    const data = await r.json();
    if (!r.ok || !data.success){
      alert((data && data.error) || '削除に失敗しました。');
      return;
    }
    location.reload();
  } catch (e){
    alert('削除に失敗しました: ' + e);
  }
}
document.addEventListener('click', (ev) => {
  const btn = ev.target && ev.target.closest && ev.target.closest('[data-clear]');
  if (btn) clearTestProgress(btn.getAttribute('data-clear'));
});
"""


def index_html() -> str:
    tests = all_tests()
    if tests:
        body = "".join(card_html(t) for t in tests)
    else:
        body = ('<div class="empty">tests/ にテストがありません。'
                '<code>make sheet &lt;test_id&gt;</code> で解答用紙を生成してください。</div>')
    graded = sum(1 for t in tests if t["result"])
    return (
        '<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>JLPT N2 模擬試験 — テスト一覧</title>'
        f'<style>{app_style.APP_CSS}{INDEX_CSS}</style></head><body>'
        # The same #bar as screens 2 and 3, from the same stylesheet.
        '<div id="bar"><b>JLPT N2 模擬試験</b><span class="grow"></span>'
        f'<span class="sub">テスト {len(tests)} 件 / 採点済み {graded} 件</span></div>'
        '<main><p class="lede">受験するテストを選んでください。'
        '解答は選択するたびに保存され、採点結果は 採点結果.json に残ります。'
        '「結果を削除」で採点結果と解答の両方を消せます。</p>'
        f'{body}</main><script>{INDEX_JS}</script></body></html>')

# ------------------------------------------------------------------- handler
class AnswerSheetHandler(SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    # -- client disconnects are normal, not server errors -------------------
    # The audio element aborts its 聴解.mp3 request every time you seek, change
    # speed, or leave the page, which kills the socket mid-copyfile. Without
    # these two guards Python dumps a BrokenPipeError traceback per abort.
    def handle(self):
        try:
            super().handle()
        except (BrokenPipeError, ConnectionResetError):
            self.close_connection = True

    def finish(self):
        try:
            super().finish()
        except (BrokenPipeError, ConnectionResetError):
            pass

    # ---------------------------------------------------------------- GET
    def do_GET(self):
        route = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)

        if route in ("", "/", "/index.html", "/index.htm"):
            return self._write_html(index_html())
        if route.rstrip("/") == "/api/tests":
            return self._write_json(200, {"tests": all_tests()})

        # /tests/<id> and /tests/<id>/ land on that test's sheet.
        m = re.fullmatch(r"/tests/([^/]+)/?", route)
        if m:
            if not test_dir(m.group(1)):
                return self.send_error(404, "Unknown test")
            target = "/tests/" + urllib.parse.quote(m.group(1)) + "/" + urllib.parse.quote(SHEET)
            self.send_response(302)
            self.send_header("Location", target)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

        if not self._under_tests():
            return self.send_error(404, "Not Found")
        if self.serve_range():
            return
        super().do_GET()

    def do_HEAD(self):
        route = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)
        if route in ("", "/", "/index.html", "/index.htm"):
            return self._write_html(index_html(), body=False)
        if not self._under_tests():
            return self.send_error(404, "Not Found")
        super().do_HEAD()

    def _under_tests(self) -> bool:
        """Only tests/ is on the web. The server's cwd is the whole repo."""
        try:
            path = Path(self.translate_path(self.path)).resolve()
        except (OSError, ValueError):
            return False
        return path == TESTS.resolve() or TESTS.resolve() in path.parents

    def serve_range(self) -> bool:
        """Answer a `Range:` request with 206 Partial Content.

        SimpleHTTPRequestHandler ignores Range and restreams the whole ~30 MB
        MP3, so every seek in the 聴解 player downloaded the file again and the
        browser cancelled the previous transfer. Returns False (fall through to
        the normal 200 path) for anything it cannot serve as a range.
        """
        header = self.headers.get("Range")
        if not header:
            return False
        m = RANGE_RE.match(header.strip())
        if not m:
            return False
        path = Path(self.translate_path(self.path))
        if not path.is_file():
            return False

        size = path.stat().st_size
        first, last = m.group(1), m.group(2)
        if first:
            start = int(first)
            end = int(last) if last else size - 1
        elif last:                      # suffix form: bytes=-500
            start, end = max(0, size - int(last)), size - 1
        else:
            return False
        end = min(end, size - 1)
        if start > end or start >= size:
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{size}")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return True

        length = end - start + 1
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(str(path)))
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(length))
        self.send_header("Last-Modified", self.date_time_string(int(path.stat().st_mtime)))
        self.end_headers()
        with path.open("rb") as f:
            f.seek(start)
            remaining = length
            while remaining > 0:
                chunk = f.read(min(64 * 1024, remaining))
                if not chunk:
                    break
                self.wfile.write(chunk)
                remaining -= len(chunk)
        return True

    def guess_type(self, path):
        ctype = super().guess_type(path)
        if ctype.startswith("text/") or ctype in ("application/json", "application/javascript"):
            if "charset=" not in ctype:
                ctype += "; charset=utf-8"
        return ctype

    def end_headers(self):
        if self.command == "GET":
            self.send_header("Accept-Ranges", "bytes")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    # --------------------------------------------------------------- writers
    def _write_json(self, code: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _write_html(self, markup: str, body: bool = True):
        payload = markup.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")   # progress must be live
        self.end_headers()
        if body:
            self.wfile.write(payload)

    @staticmethod
    def _write_json_file(d: Path, name: str, data) -> str:
        (d / name).write_text(json.dumps(data, indent=2, ensure_ascii=False),
                              encoding="utf-8")
        return name

    # ---------------------------------------------------------------- POST
    def do_POST(self):
        route = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path).rstrip("/")
        m = API_RE.match(route)
        if not m:
            return self.send_error(404, "Not Found")
        d = test_dir(m.group(1))
        if not d:
            return self.send_error(404, "Unknown test")

        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length).decode("utf-8") if length else "{}"
            data = json.loads(raw or "{}")

            action = m.group(2)
            if action == "clear":
                removed = []
                for name in (RESULT_JSON, ANSWERS_JSON):
                    p = d / name
                    if p.is_file():
                        p.unlink()
                        removed.append(name)
                msg = (f"{'、'.join(removed)} を削除しました。" if removed
                       else "削除するファイルはありませんでした。")
                return self._write_json(200, {
                    "success": True,
                    "message": msg,
                    "removed_files": removed,
                })

            saved = []
            answers = data.get("answers")
            if answers is not None:
                saved.append(self._write_json_file(d, ANSWERS_JSON, answers))
            if action == "submit":
                result = data.get("result")
                if result is None:
                    return self._write_json(400, {"success": False,
                                                  "error": "no result in payload"})
                saved.append(self._write_json_file(d, RESULT_JSON, result))

            self._write_json(200, {
                "success": True,
                "message": f"{'、'.join(saved)} を tests/{d.name}/ に保存しました。",
                "saved_files": saved,
            })
        except Exception as e:                               # noqa: BLE001
            self._write_json(500, {"success": False, "error": str(e)})


# -------------------------------------------------------------------- runner
def get_free_port(start_port: int = 8765, max_attempts: int = 20) -> int:
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    return start_port


def run_server(port: int = 8765, open_browser: bool = True):
    if not TESTS.is_dir():
        sys.exit(f"Error: {TESTS} does not exist — nothing to serve.")

    actual_port = get_free_port(port)

    # Threaded: a single-threaded server blocks the 採点する POST behind an
    # in-flight 聴解.mp3 stream, so submitting while the audio buffers hung.
    ThreadingHTTPServer.allow_reuse_address = True
    httpd = ThreadingHTTPServer(("127.0.0.1", actual_port), AnswerSheetHandler)

    tests = all_tests()
    print("==========================================================================")
    print(f" JLPT mock exam server — {len(tests)} test(s) in {TESTS}")
    print(f" URL: http://127.0.0.1:{actual_port}/")
    for t in tests:
        state = "no 解答.html (run make sheet)" if not t["has_sheet"] else \
                f"{t['answered']}/{t['total']} answered" + \
                (f", scored {t['result']['total_scaled_score']}/180" if t["result"] else "")
        print(f"   - {t['id']}: {state}")
    print(" Selecting a choice autosaves ユーザー解答.json; 採点する also saves 採点結果.json.")
    print(" Press Ctrl+C to stop the server.")
    print("==========================================================================")

    if open_browser:
        webbrowser.open(f"http://127.0.0.1:{actual_port}/")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        httpd.server_close()


def main():
    parser = argparse.ArgumentParser(
        description="Serve every test in tests/ from one server (test list + exam + result).")
    parser.add_argument("--port", type=int, default=8765, help="Port to serve on (default: 8765)")
    parser.add_argument("--no-open", action="store_true", help="Do not automatically open browser")
    args = parser.parse_args()

    run_server(port=args.port, open_browser=not args.no_open)


if __name__ == "__main__":
    main()
