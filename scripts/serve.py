#!/usr/bin/env python3
"""Serve this folder so Atomify can load your examples while you edit them.

    python3 scripts/serve.py            # http://localhost:8000
    python3 scripts/serve.py 9000       # another port
    python3 scripts/serve.py --atomify http://localhost:5173/atomify/

Then open the printed link. Edits show up when you reload Atomify; nothing is
cached. Only the Python standard library is needed.
"""

import argparse
import functools
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_ATOMIFY = "https://andeplane.github.io/atomify/"


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Atomify runs on another origin, so it needs CORS. The private
        # network header lets an https page reach this localhost server in
        # Chromium browsers.
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("port", nargs="?", type=int, default=8000)
    parser.add_argument(
        "--atomify",
        default=DEFAULT_ATOMIFY,
        help="Atomify to open, e.g. a local dev server (default: %(default)s)",
    )
    args = parser.parse_args()

    examples_url = f"http://localhost:{args.port}/examples.json"
    handler = functools.partial(Handler, directory=ROOT)
    server = ThreadingHTTPServer(("localhost", args.port), handler)
    print(f"Serving {ROOT} at http://localhost:{args.port}/")
    print()
    print("Open your examples in Atomify:")
    print(f"  {args.atomify}?examplesUrl={quote(examples_url, safe='')}")
    print()
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
