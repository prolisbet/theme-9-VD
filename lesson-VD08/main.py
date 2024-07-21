from flask import Flask, render_template, request
import requests
from config8 import api_key_weather, api_key_news

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    news = None
    if request.method == 'POST':
        city = request.form['city']
        weather = get_weather(city)
        news = get_news()
    return render_template('index.html', weather=weather, news=news)


def get_weather(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key_weather}&units=metric'
    response = requests.get(url)
    return response.json()


def get_news():
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key_news}'
    response = requests.get(url)
    return response.json().get('articles', [])


if __name__ == '__main__':
    app.run(debug=True)
