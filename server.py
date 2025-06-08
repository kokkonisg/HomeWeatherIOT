# A simple temporary HTTP server to handle temperature data
# In the future, server will be running an the ESP8266 itself
#

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

dataStack = []

class TempHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/temperature':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                dataStack.append(data)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'ok'}).encode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path == '/temperature':
            if dataStack:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(dataStack[-1]).encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'No data'}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=TempHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Serving on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()