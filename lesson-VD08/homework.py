from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    qotd = None
    random_quote = None
    if request.method == 'POST':
        qotd = get_qotd()
        random_quote = get_random()
    return render_template('quotes.html', qotd=qotd, random_quote=random_quote)


def get_qotd():
    url = 'https://favqs.com/api/qotd'
    response = requests.get(url)
    return response.json()


def get_random():
    url = 'https://zenquotes.io/api/random'
    response = requests.get(url)
    return response.json()


if __name__ == '__main__':
    app.run(debug=True)
