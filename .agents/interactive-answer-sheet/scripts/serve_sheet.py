#!/usr/bin/env python3
"""
Serve interactive answer sheets via a local HTTP server and automatically save
submitted results (採点結果.md and user_answers.json) directly into tests/<test_id>/.

Usage:
    python3 .agents/interactive-answer-sheet/scripts/serve_sheet.py tests/1
    # or: make serve 1
"""
import argparse
import json
import sys
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


class AnswerSheetHandler(SimpleHTTPRequestHandler):

    def __init__(self, *args, test_dir=None, **kwargs):
        self.test_dir = test_dir
        super().__init__(*args, directory=str(test_dir), **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path == "/api/submit":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode("utf-8"))
                saved_files = []

                # Write Markdown report if provided
                md_name = data.get("filename", "採点結果.md")
                md_content = data.get("content")
                if md_name and md_content:
                    target = self.test_dir / Path(md_name).name
                    target.write_text(md_content, encoding="utf-8")
                    saved_files.append(target.name)

                # Write JSON answers if provided
                json_name = data.get("json_filename", "user_answers.json")
                json_data = data.get("json_data")
                if json_name and json_data is not None:
                    target_json = self.test_dir / Path(json_name).name
                    target_json.write_text(json.dumps(json_data, indent=2, ensure_ascii=False),
                                           encoding="utf-8")
                    saved_files.append(target_json.name)

                resp = {
                    "success": True,
                    "message": f"Saved {', '.join(saved_files)} directly to {self.test_dir.name}/",
                    "saved_files": saved_files
                }
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(resp, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                err_resp = {"success": False, "error": str(e)}
                self.wfile.write(json.dumps(err_resp, ensure_ascii=False).encode("utf-8"))
        else:
            self.send_error(404, "Not Found")


def run_server(test_dir: Path, port: int = 8765, open_browser: bool = True):
    test_dir = test_dir.resolve()
    if not test_dir.is_dir():
        sys.exit(f"Error: test directory '{test_dir}' does not exist.")

    def handler(*args, **kwargs):
        return AnswerSheetHandler(*args, test_dir=test_dir, **kwargs)

    HTTPServer.allow_reuse_address = True
    httpd = HTTPServer(("127.0.0.1", port), handler)
    print("==========================================================================")
    print(f" Answer Sheet Server running for: {test_dir.name} ({test_dir})")
    print(f" URL: http://127.0.0.1:{port}/解答.html")
    print(" Submitting answers will automatically save directly into this directory!")
    print(" Press Ctrl+C to stop the server.")
    print("==========================================================================")

    sheet = test_dir / "解答.html"

    if open_browser and sheet.is_file():
        webbrowser.open(f"http://127.0.0.1:{port}/{sheet.name}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")


def main():
    parser = argparse.ArgumentParser(description="Serve answer sheet with direct file saving.")
    parser.add_argument("test_dir", help="Path to test directory (e.g. tests/1)")
    parser.add_argument("--port", type=int, default=8765, help="Port to serve on (default: 8765)")
    parser.add_argument("--no-open", action="store_true", help="Do not automatically open browser")
    args = parser.parse_args()

    run_server(Path(args.test_dir), port=args.port, open_browser=not args.no_open)


if __name__ == "__main__":
    main()
