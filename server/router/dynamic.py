# creating routers that can handle dynamic paths e.g /user, /user/1, /user/2, 
from urllib.parse import parse_qs
import json

class Router:

    routes = {}

    def get(self, path, handler):
        self.routes[('GET', path)] = handler

    def post(self, path, handler):
        self.routes[('POST', path)] = handler

    def match_paths(self, route_path, req_path):
        param = {}
        route_parts = route_path.strip('/').split('/')
        req_parts = req_path.strip('/').split('/')
        # print(f'part list is {route_parts}{req_parts}')
        
        if len(route_parts) != len(req_parts):
            return None

        for route_part, req_part in zip(route_parts, req_parts):
            
            if route_part.startswith(":"):
                param_key = route_part[1:]
                param[param_key] = req_part

            elif route_part != req_part:
                return None

        return param

    def match(self, method, req_path):
        for (route_method, route_path), handler in self.routes.items():
            if route_method != method:
                continue

            param =self.match_paths(route_path, req_path)

            if param is not None:
                return param, handler

        return None


class Request:
    def __init__(self, handler):
        self.method = handler.command
        self.path = handler.path
        self.headers = handler.headers
        # self.rfile = handler.rfile
        self.handler = handler
        self.lenght = 0

        if self.method == 'POST':
            content_length = handler.headers['Content-Length']
            self.lenght = int(content_length)
            # if content_length is not None:
            #     body = handler.rfile.read(int(content_length)).decode()
            #     self.form = parse_qs(body)

    def json_parsing(self): 
        body = self.handler.rfile.read(self.lenght).decode()
        return json.loads(body)

         
            
    


class Response:

    def __init__(self, handler):
        self.handler = handler

    def send(self, response_body, status =200, content_type='text/plain', ):
        self.handler.send_response(status)
        self.handler.send_header('Content-Type', content_type)
        self.handler.end_headers()
        self.handler.wfile.write(response_body.encode())

    def send_html(self, body):
        self.send(body, content_type='text/html')

    def render_file(self, file_path, status=200):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()

        except:
            print('unable to parse html file')
            return None

    def parse_to_json(self, res):
        resp_dict = {}
        resp_dict['result'] = res
        return json.dumps(resp_dict)


    def json_response(self, body):
        self.send(body, content_type="application/json")

        


    


    

