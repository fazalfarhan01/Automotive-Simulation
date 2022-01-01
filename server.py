from flask import Flask, request
import rsa
import base64
import json


import rsa
publicKey, privateKey = rsa.newkeys(1024)

received_data = {'info': []}

app = Flask(__name__)


@app.route('/')
def index():
    return f"""<h1>Smart Car with Enhanced Safety System : Server</h1><br><a href="/viewData">Click here to view received data</a>"""


@app.route('/keys/')
def keys():
    return str(publicKey.n)


@app.route('/viewData')
def view():
    return received_data


@app.route('/receive/', methods=['POST'])
def forward():
    try:
        print('Received the following information')
        received = request.json.get('encrypted')
        decrypted = rsa.decrypt(base64.b64decode(
            received.encode()), privateKey)
        orignal_sent_data = json.loads(decrypted)
        print(json.dumps(orignal_sent_data, indent=2))
        received_data['info'].append(orignal_sent_data)
        return {'status': True}
    except:
        return {'status': False}


app.run(host='0.0.0.0', port=8500)
