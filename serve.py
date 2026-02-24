#!/usr/bin/env python3
import http.server
import json
import os

PORT = int(os.environ.get("PORT", 8000))
COUNTER_FILE = os.path.join(os.path.dirname(__file__), "visits.json")


def _read_count():
    try:
        with open(COUNTER_FILE) as f:
            return json.load(f).get("count", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0


def _write_count(n):
    with open(COUNTER_FILE, "w") as f:
        json.dump({"count": n}, f)


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/visits":
            count = _read_count() + 1
            _write_count(count)
            body = json.dumps({"count": count}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
        else:
            super().do_GET()

    def log_message(self, fmt, *args):
        pass  # suppress per-request noise


with http.server.HTTPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
