import http.server
import socketserver
import os
import json
from urllib.parse import urlparse, parse_qs

# Set the port
PORT = 8000

# Custom request handler


class BugFixerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse URL
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        # Serve the requested file or default to index.html
        if path == '/':
            self.path = '/index.html'

        # Intentional bug: missing file extension check
        # This will try to serve any file, even if it doesn't exist

        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def log_message(self, format, *args):
        # Print with color for better visibility
        print(f"\033[92m[SERVER] {format % args}\033[0m")

# Start the server


def start_server():
    with socketserver.TCPServer(("", PORT), BugFixerHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.shutdown()


if __name__ == "__main__":
    # Change to the directory where this script is located
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Start the server
    start_server()
