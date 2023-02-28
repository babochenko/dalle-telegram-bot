import os
import random

import openai
import requests
from flask import Flask
from flask import Response
from flask import request

openai.api_key = os.getenv("OPENAI_API_KEY")
tg_token = os.getenv("TG_TOKEN")

app = Flask(__name__)


@app.route('/', methods=['POST'])
def generate_images():
    msg = request.get_json()
    print('msg', msg)

    if 'message' in msg and 'text' in msg['message']:
        respond_message(msg)
    elif 'inline_query' in msg and 'query' in msg['inline_query']:
        respond_inline(msg)

    return Response('ok', status=200)


def respond_message(msg):
    query = msg['message']['text']
    chat_id = msg['message']['chat']['id']

    response = openai.Image.create(
        prompt=query,
        n=1,
        size="1024x1024"
    )

    images = [data['url'] for data in response['data']]
    for idx, image in enumerate(images):
        url = f'https://api.telegram.org/bot{tg_token}/sendPhoto'
        payload = {
            'chat_id': chat_id,
            'photo': image,
        }

        requests.post(url, json=payload)


def respond_inline(msg):
    query = msg['inline_query']['query']
    query_id = msg['inline_query']['id']

    if not query:
        return

    response = openai.Image.create(
        prompt=query,
        n=1,
        size="1024x1024"
    )

    rand = random.Random()
    images = [data['url'] for data in response['data']]
    url = f'https://api.telegram.org/bot{tg_token}/answerInlineQuery'
    payload = {
        'inline_query_id': query_id,
        'results': [{
            type: 'photo',
            id: rand.randint(0, 100_000),
            'photo_url': img,
            'thumb_url': img,
        } for img in images],
    }

    requests.post(url, json=payload)


if __name__ == '__main__':
    app.run(port=5002, debug=True)
