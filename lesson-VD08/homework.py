from flask import Flask, render_template, request
import requests
from config8 import api_key_theysaidso

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    quotes = {}
    if request.method == 'POST':
        for site, value in quote_sites.items():
            quote_data = get_quote(value['url'])
            if quote_data:
                quote_text = eval(value['quote'])
                author = eval(value['author'])
                quotes[site] = (quote_text, author)
    return render_template('quotes.html', quotes=quotes)


quote_sites = {
    'Fav Quotes': {'url': 'https://favqs.com/api/qotd',
                   'quote': 'quote_data["quote"]["body"]',
                   'author': 'quote_data["quote"]["author"]'},
    'Zen Quotes': {'url': 'https://zenquotes.io/api/random',
                   'quote': 'quote_data[0]["q"]',
                   'author': 'quote_data[0]["a"]'},
    'They Said So': {'url': f'http://quotes.rest/qod.json?api_key={api_key_theysaidso}',
                     'quote': 'quote_data["contents"]["quotes"][0]["quote"]',
                     'author': 'quote_data["contents"]["quotes"][0]["author"]'},
               }


def get_quote(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except (requests.exceptions.HTTPError, requests.exceptions.RequestException, ValueError) as e:
        print(f"Error fetching data from {url}: {e}")
        return None


if __name__ == '__main__':
    app.run(debug=True)
