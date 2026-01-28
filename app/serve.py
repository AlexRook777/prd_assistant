
import http.server
import socketserver
import requests
import json
import os
from datetime import datetime

WEBHOOKS = []

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class ProxyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path == '/api/webhooks':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(WEBHOOKS).encode('utf-8'))
        else:
            super().do_GET()

    def do_DELETE(self):
        if self.path == '/api/webhooks':
            WEBHOOKS.clear()
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_error(404, "File not found")

    def do_POST(self):
        if self.path == '/proxy':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                target_url = data.get('url')
                method = data.get('method', 'GET')
                headers = data.get('headers', {})
                body = data.get('body', None)

                if not target_url:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'Missing "url" in payload')
                    return

                # Forward the request
                print(f"Proxying {method} to {target_url}")
                
                # Filter out headers that might cause issues or should be recreated
                headers_to_send = {k: v for k, v in headers.items() if k.lower() not in ['host', 'content-length']}
                
                response = requests.request(
                    method=method,
                    url=target_url,
                    headers=headers_to_send,
                    json=body,  # Assuming JSON body for this integration
                    timeout=30
                )

                # Send back response
                self.send_response(200) # Always return 200 from proxy, handle actual status in body
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()

                proxy_response = {
                    'status': response.status_code,
                    'headers': dict(response.headers),
                    'body': response.text
                }
                
                self.wfile.write(json.dumps(proxy_response).encode('utf-8'))

            except Exception as e:
                print(f"Error: {e}")
                self.send_response(500)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {'error': str(e)}
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
        elif self.path == '/webhook':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Attempt to parse body as JSON, fall back to string
                try:
                    body = json.loads(post_data.decode('utf-8'))
                except:
                    body = post_data.decode('utf-8')

                webhook_entry = {
                    'timestamp': datetime.now().isoformat(),
                    'method': 'POST',
                    'headers': dict(self.headers),
                    'body': body
                }
                WEBHOOKS.append(webhook_entry)
                print(f"Received webhook: {body}")

                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(b'OK')
            except Exception as e:
                print(f"Error processing webhook: {e}")
                self.send_response(500)
                self.end_headers()

        else:
            # Default behavior for other POST requests (if any) or 404
            self.send_error(404, "File not found")

    def do_OPTIONS(self):
        # Handle CORS preflight for the proxy endpoint itself
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), ProxyHTTPRequestHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        print(f"Proxy endpoint at http://localhost:{PORT}/proxy")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
