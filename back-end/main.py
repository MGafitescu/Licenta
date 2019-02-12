from flask import Flask, request, jsonify
import json
from PIL import Image
from io import BytesIO
import sys
import base64
from prediction import predict

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/addImage', methods=['POST', 'OPTIONS'])
def addImage():
    sys.setrecursionlimit(2000000)
    name = request.json['name']
    payload = request.json['payload']
    originalImage = Image.open(BytesIO(base64.b64decode(payload)))
    originalImage.save(name)
    label = predict.predict(originalImage)
    data = {
        "label": label
    }
    return jsonify(json.dumps(data)), 200


if __name__ == "__main__":
    app.run(threaded = False)
