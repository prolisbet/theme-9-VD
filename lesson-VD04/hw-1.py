from flask import Flask
import datetime

app = Flask(__name__)


@app.route('/')
def show_time():
    return f'Дата и время: {datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}'


if __name__ == '__main__':
    app.run(debug=True)
