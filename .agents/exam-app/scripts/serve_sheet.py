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
    python3 .agents/exam-app/scripts/serve_sheet.py
    # or: make serve
"""
import argparse
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

# Screen 1's markup, CSS and actions are the SAME ones the GitHub Pages build
# uses — imported, never copied. See index_view.py (and app_style.py, which it
# imports for the chrome shared with screens 2 and 3).
sys.path.insert(0, str(Path(__file__).resolve().parent))
import app_style      # noqa: E402
import grade_answers as ga  # noqa: E402  (per-test item counts)
import index_view     # noqa: E402

# 71 言語知識・読解 + 30 聴解. `make check` asserts 解答.html carries exactly this
# many radio groups, so it is safe to use as the progress denominator.
QUESTION_COUNT = index_view.QUESTION_COUNT

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


def question_count_of(d: Path) -> int:
    """This test's own item count, off its answer-key tables.

    QUESTION_COUNT is the current era's 101 and is right for every generated
    mock, but an imported past paper can be a different shape — 7/2021 keys 72
    言語知識・読解 items, so the list read "0 / 101" for a 102-item paper. Falls
    back to the constant if the Markdown is unreadable.
    """
    try:
        gengo = len(ga.parse_gengo_keys(d / "言語知識・読解.md"))
        choukai = len(ga.parse_choukai_keys(d / "聴解.md"))
    except Exception:
        return QUESTION_COUNT
    return (gengo + choukai) or QUESTION_COUNT


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
        "total": question_count_of(d),
        "has_sheet": (d / SHEET).is_file(),
        "has_audio": (d / "聴解.mp3").is_file() or (d / "聴解_チャプター.json").is_file(),
        "has_explanation": (d / "模範解答.html").is_file(),
        "result": result,
    }


def all_tests() -> list[dict]:
    if not TESTS.is_dir():
        return []
    dirs = [d for d in TESTS.iterdir()
            if d.is_dir() and ((d / SHEET).is_file() or (d / "言語知識・読解.md").is_file())]
    return [progress_of(d) for d in sorted(dirs, key=lambda p: natural_key(p.name))]


# --------------------------------------------------------- screen 1: the list
# The list's CSS, cards and actions live in index_view.py — the SAME view the
# static GitHub Pages build renders. Here it is fed by GET /api/tests below
# (the disk), there by localStorage; nothing else differs.
def index_html() -> str:
    import importlib
    importlib.reload(app_style)
    importlib.reload(index_view)
    return index_view.index_html("server")


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
        # Screen 1 is rendered from /api/tests now, so this is the read that must
        # never be cached — progress and scores have to be live (see SKILL.md).
        self.send_header("Cache-Control", "no-store")
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
