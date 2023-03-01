from flask import Flask, Response
from flask import request

from main import generate_images

app = Flask(__name__)


@app.route('/', methods=['POST'])
def handle_request():
    generate_images(request)
    return Response('ok', status=200)


if __name__ == '__main__':
    app.run(port=5002, debug=True)
