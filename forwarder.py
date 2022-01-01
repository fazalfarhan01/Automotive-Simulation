import json
from flask import Flask, request
import requests

app = Flask(__name__)



@app.route('/')
def index():
    return "<h1>Smart Car with Enhanced Safety System : Node<h1>"


@app.route('/forward/', methods=['POST'])
def forward():
    print('Received the following information')
    print(request.json.get('encrypted'))
    try:
        requests.post(
            url=f'http://localhost:8500/receive/',
            json=request.json
        )
        return {'status':True}
    except requests.exceptions.ConnectionError:
        return {'status':False}


@app.route('/getKeys/')
def get_keys():
    response = requests.get("http://localhost:8500/keys")
    return response.content.decode()


app.run(host='0.0.0.0', port=8502)
