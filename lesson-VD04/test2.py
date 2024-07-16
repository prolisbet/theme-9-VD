from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def heroes():
    context = {
        "caption": "Герои",
        "poem": ["Я так давно родился,",
                 "Что слышу иногда,",
                 "Как надо мной проходит",
                 "Зеленая вода."]
    }
    return render_template('base.html', **context)


@app.route('/shablon/')
def heroes2():
    context = {
        "caption": "Люди",
        "link": "Отправить сообщение"
    }
    return render_template('index.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
