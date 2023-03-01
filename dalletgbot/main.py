from flask import Flask, Response
from flask import request

from function import do_generate_images

app = Flask(__name__)


@app.route('/', methods=['POST'])
def handle_request():
    do_generate_images(request)
    return Response('ok', status=200)


if __name__ == '__main__':
    app.run(port=5002, debug=True)
