import http.server
import urllib.parse as urlparse
from json import dumps
import requests
import socketserver
import random
from init_fl import FL

import cgi
import torch
from flask import request, Flask, send_file
from urllib.parse import parse_qs, urlparse
import json
from flask_classful import FlaskView, route

app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello, World!'


@app.route('/init', methods=['POST'])
def get_init():
    if request.method == 'POST':
        param = json.loads(request.get_data(), encoding='utf-8')
        # print(param)
        _ = client.initial(param)
        return 'Success Receive Model Argument'


@app.route('/download', methods=['POST'])
def get_download():
    if request.method == 'POST':

        file = request.files['model'].read()
        fname = request.files['json'].read()

        client.receive_weight(file, fname)
        tmp = client.update()
        torch.save(client.weight, "client_model.pth")

        return send_file(open("client_model.pth", "rb"), "client_model.pth")

    else:
        return "No file received!"


"""
class Client(FlaskView):

    def __init__(self):
        self.a = "A"
    def index(self):
        return 'Hello, World!'

    @app.route('/init', methods=['POST'])
    def get_init():
        print("IN" )
        if request.method == 'POST':
            param = json.loads(request.get_data(), encoding='utf-8')
            print(param)

            return 'Success Receive Model Argument'

    @app.route('/download', methods=['POST'])
    def get_agg_model():
        if request.method == 'POST':
            file = request.files['model'].read()
            fname = request.files['json'].read()
            fname = ast.literal_eval(fname.decode("utf-8"))
            fname = fname['file_name']

            wfile = open(fname, 'wb')
            wfile.write(file)
            wfile.close()

            initial = torch.load(fname)
            return "Model received!"
        else:
            return "No file received!"

    def receive(self):
        print(self.a)

"""
if __name__ == '__main__':
    client = FL()
    app.run(host='0.0.0.0', port='8585', debug=False)

    # Client.register(app, route_base='/')
"""
class RequestHandler(http.server.BaseHTTPRequestHandler):
    def __get_Parameter(self, key):

        if "?" in self.path:
            self.__param = dict(urlparse.parse_qsl(self.path.split("?")[1], True))
        else:
            self.__param = {'local_iter': 20}

        if key in self.__param:
            return self.__param[key]
        return None

    def do_POST(self):
        if self.path == "/FL_info":
            content_length = int(self.headers.get('Content-Length'))
            print("------------------")
            post_body = self.rfile.read(content_length)
            print(post_body)




    def do_GET(self):

        if "?" in self.path:
            urls = self.path.split("?")
            path = urls[0]
            # param = dict(urlparse.parse_qsl(urls[1], True))

            if path == "/FL_info":
                file = requests.files['model'].read()
                fname = requests.files['json'].read()

                # print(param)
                # fl = FL(param)
                # fl.print_param()
                # fname = ast.literal_eval(fname.decode("utf-8"))
                fname = fname['fname']
                print(fname)
                message = bytes("Receive", encoding='utf8')
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(message)

        else:
            if self.path == "/init":
                random_iter = random.randint(1, 10)
                print("Random Iter", random_iter)
                message = bytes(str(random_iter), encoding='utf8')

            if self.path =="/FL_info":
                file = request.files['model'].read()
                fname = request.files['json'].read()
                print(file)
                # print(self.rfile.read(1000))
                with open("global_model.pth", "wb") as file:
                    response = self.rfile.readline()
                    print(response)
                    file.write(response)

                w = torch.load("global_model.pth")
                print(w)
                ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
                if ctype == 'multipart/form-data':
                    form = cgi.FieldStorage(fp=self.rfile, headers=self.headers)
                print(torch.load(self.rfile.readlines()))
                # print(param)
                # fl = FL(param)
                # fl.print_param()
                # fname = ast.literal_eval(fname.decode("utf-8"))
                # fname = fname['fname']
                # print(fname)
                message = bytes("Receive", encoding='utf8')
                


            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(message)

        return


if __name__ == "__main__":
    try:
        port = 8585
        with socketserver.TCPServer(("", port), RequestHandler) as httpd:
            print("Server Start")
            httpd.serve_forever()

    except KeyboardInterrupt:
        pass
"""
