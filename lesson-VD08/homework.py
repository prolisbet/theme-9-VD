from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    pass


def get_quotes():
    url = 'https://favqs.com/api/quotes'
    response = requests.get(url)
    return response.json().get('quotes', [])
