from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

class my_handler(BaseHTTPRequestHandler):
    # GET request handler
    def do_GET(self):

        url = urlparse(self.path)
        print("request path is", url.path)
        query = parse_qs(url.query)
        print(f"request query is {query}")
        print(f"request user agent is {self.headers.get('User-Agent')}")
        if url.path == '/':
            req_dict = {"message" : "Hello world"}
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(req_dict).encode())

        elif url.path == '/users':
            user_dict = {'user_ID':query.get('id')[0]}
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(user_dict).encode())
        else:
            self.send_response(405)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write('Page not found'.encode())

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        j_data = self.rfile.read(content_len)
        data = json.loads(j_data)
        print('received: ', data)
        res = {"message": "user received", "data": data}
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(res, indent=4).encode())

server = HTTPServer(("localhost", 8080), my_handler)
print('Running server on http://localhost:8080')
server.serve_forever()




