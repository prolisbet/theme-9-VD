from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Создание приложения Flask
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Создание объекта SQLAlchemy
db = SQLAlchemy(app)


# Определяем модель (таблицу в базе данных)
class User(db.Model):  # В скобках указываем модель, чтобы в дальнейшем создать именно базу данных
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unigue=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


# Создание таблицы в базе данных
with app.app_context():
    db.create_all()


# Добавление данных в таблицу
@app.route('/add_user')
def add_user():
    new_user = User(username='JohnDoe')
    db.session.add(new_user)
    db.session.commit()
    return 'User added!'


# Получение данных из таблицы
@app.route('/users')
def get_users():
    users = User.query.all()
    return str(users)


# Удаление данных из таблицы
@app.route('/delete_user')
def delete_user():
    user = User.query.first()
    db.session.delete(user)
    db.session.commit()
    return 'User deleted!'


if __name__ == '__main__':
    app.run(debug=True)
