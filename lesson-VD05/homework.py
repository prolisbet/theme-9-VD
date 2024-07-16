from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    context = {
        "active_home": "active",
        "active_about": "",
    }
    return render_template('home.html', **context)


@app.route('/about/')
def about():
    context = {
        "active_home": "",
        "active_about": "active",
    }
    return render_template('about.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
