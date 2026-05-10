"""Local helper for the Tarot Learning Lab static site.

Run this script from the project root to verify the homepage exists or to
preview the site through a simple localhost HTTP server.
"""

from __future__ import annotations

import argparse
import http.server
from functools import partial
import socketserver
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
INDEX_FILE = PROJECT_ROOT / "index.html"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5500


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def ensure_index_exists() -> None:
    if not INDEX_FILE.exists():
        raise FileNotFoundError(f"Missing homepage: {INDEX_FILE}")


def show_status() -> None:
    ensure_index_exists()
    size_kb = INDEX_FILE.stat().st_size / 1024
    print("Tarot Learning Lab")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Homepage: {INDEX_FILE.name} ({size_kb:.1f} KB)")
    print(f"Preview URL: http://{DEFAULT_HOST}:{DEFAULT_PORT}/")


def serve(host: str, port: int) -> None:
    ensure_index_exists()
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=PROJECT_ROOT)

    with ReusableTCPServer((host, port), handler) as httpd:
        print(f"Serving {PROJECT_ROOT}")
        print(f"Open http://{host}:{port}/")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Static site helper.")
    parser.add_argument(
        "--serve",
        action="store_true",
        help="Start a local HTTP server for index.html.",
    )
    parser.add_argument("--host", default=DEFAULT_HOST, help="Server host.")
    parser.add_argument("--port", default=DEFAULT_PORT, type=int, help="Server port.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.serve:
        serve(args.host, args.port)
    else:
        show_status()


if __name__ == "__main__":
    main()
