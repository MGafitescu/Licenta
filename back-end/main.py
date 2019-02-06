from flask import Flask, request, jsonify
import json
from PIL import Image
from io import BytesIO
import sys
import cv2
import base64
import numpy as np

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
    pixels = cv2.imdecode(np.fromstring(base64.b64decode(payload)), 0)
    np.save("pixels",pixels)
    originalImage.save(name)
    data = {
        "response": "Static response"
    }
    return jsonify(json.dumps(data)), 200


if __name__ == "__main__":
    app.run(debug=True)
