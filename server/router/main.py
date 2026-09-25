from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from dynamic import Router, Request, Response
import json

# user_dict = {'id':{'1':'John', '2':'Dave'}}

router = Router()

def calculator(num1, num2, operator):

    if operator == '+':
        result = num1 + num2

    elif operator == '-':
        result = num1 - num2
    elif operator == '*':
        result = num1 * num2
    elif operator == '/':
        result = num1 / num2

    return result

def home_handler(param, request, response):
    print(f'The request path is {request.path}')
    # response.send('This is the home page')

    html = response.render_file('template/index.html')
    response.send_html(html)

def users_handler(param, request, response):
    # response.send('This is the user general page')
    html = response.render_file('template/users.html')
    response.send_html(html)


def user_handler(param, request, response):
    user_id = param['id']
    response.send(f"This is user {user_id}'s home page")

def calc_handler(param, request, response):
    html = response.render_file('template/calculator.html')
    response.send_html(html)

def calculate(param, request, response):
    
    # num1 = int(request.form['number1'][0])
    # num2 = int(request.form['number2'][0])
    # operator = request.form['operator'][0]
    req_dict = request.json_parsing()
    num1 = req_dict['num1']
    num2 = req_dict['num2']
    operator = req_dict['opera']


    res = calculator(num1, num2, operator)
    body = response.parse_to_json(res)
   

    response.json_response(body)



    
    

    

# def create_user(request, param):
#     url = urlparse(request.path)
#     name = parse_qs(url.query).get('name')[0]
#     request.send_response(200)
#     request.send_header('Content-Type', 'text/plain')
#     request.end_headers()
#     request.wfile.write(f'{name} your account had been successfully created\n'.encode())


    


    

router.get("/", home_handler)
router.get('/users', users_handler)
# router.post('/users', create_user)
router.get('/users/:id', user_handler)
router.get('/calc', calc_handler)
router.post('/calc', calculate)


class my_handler(BaseHTTPRequestHandler):

    def handle_req(self):
        url = urlparse(self.path)

        # print('The users name is ',parse_qs(url.query).get('name'))
        request = Request(self)
        response = Response(self)
        
        result =router.match(self.command, url.path)
        if result is None:
    
            print('None value')
            response.send('page not found', 404)
            return
           
        param, handler = result
        
        handler(param, request, response)

    def do_GET(self):
        self.handle_req()


        

    def do_POST(self):
        self.handle_req()

       
    

server = HTTPServer(('localhost', 8080), my_handler)
print('Server runing on http://localhost:8080')
server.serve_forever()



        
        

