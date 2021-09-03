from init_fl import FL
import torch
from flask import request, Flask, send_file
import json

app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello, World!'


@app.route('/init', methods=['POST'])
def get_init():
    print("ININ")
    if request.method == 'POST':
        param = json.loads(request.get_data(), encoding='utf-8')
        print(param)
        _ = client.initial(param)
        return 'Success Receive Model Argument'


@app.route('/download', methods=['POST'])
def get_download():
    if request.method == 'POST':

        file = request.files['model'].read()
        fname = request.files['json'].read()
        print("Start Trinaing")
        client.receive_weight(file, fname)
        train_loss = client.update()
        print(train_loss)
        torch.save(client.weight, "client_model.pth")

        # print(torch.load('client_model.pth'))

        return str(train_loss)

    else:
        return "No file received!"


@app.route('/update', methods=['POST'])
def get_update():
    if request.method == 'POST':
        torch.save(client.weight, "client_model.pth")

        # print(torch.load('client_model.pth'))

        return send_file(open("client_model.pth", "rb"), "client_model.pth")

    else:
        return "No file received!"


if __name__ == '__main__':
    client = FL()
    app.run(host='0.0.0.0', port='8585', debug=False)

    # Client.register(app, route_base='/')