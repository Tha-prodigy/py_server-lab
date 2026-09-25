# My first http server with python
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # print('Request path is ',self.path)
        print('Client address is ',self.client_address)
        print('Header is ',self.headers)
        url= urlparse(self.path)
        print('url path is', url.path)
        param1 = parse_qs(url.query).get('id', [None])
        param2 = parse_qs(url.query).get('name')
        print(f'user1 ID are {param1} and {param2}' )
        # print('query parameter is ', url.query)
        self.send_response(200, 'OK')
        self.send_header("Content-Type","text/plain")
        self.end_headers()
        self.wfile.write(b'hello world!!!')

       

    def do_POST(self):
        content_lenght = int(self.headers.get("Content-Length",0))
        body = self.rfile.read(content_lenght)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        cl_dict = {"status":"Received", "error": 'None'}
        res = json.dumps(cl_dict)
        self.wfile.write(res.encode())
        # self.rfile.read(content_lenght)
        print(f"client's name is ", json.loads(body).get('name'))


# Create a server object
server = HTTPServer(("localhost", 8080), MyHandler)
# print(MyHandler().headers.get('Host'))
print('Server running on http://localhost:8080 ')
server.serve_forever()