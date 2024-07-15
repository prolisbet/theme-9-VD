from flask import Flask

app = Flask(__name__)


@app.route('/')
@app.route('/<password>')
def hello_world(password=None):
    if password == '1234':
        return f'Доступ разрешен'
    else:
        return f'Доступ запрещен'


@app.route('/new/')
@app.route('/newpage/')
@app.route('/новаястраница/')
def new():
    return 'New page!'


if __name__ == '__main__':
    app.run()
