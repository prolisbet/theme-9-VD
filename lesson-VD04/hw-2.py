from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index_page():
    return render_template('index_page.html')


@app.route('/blog/')
def blog_page():
    return render_template('blog_page.html')


@app.route('/contacts/')
def contacts_page():
    return render_template('contacts_page.html')


if __name__ == '__main__':
    app.run(debug=True)
