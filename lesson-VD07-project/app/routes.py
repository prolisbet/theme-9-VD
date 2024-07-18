from flask import Flask, render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, bcrypt
from app.models import User
from app.forms import RegistrationForm, LoginForm, ChangePasswordForm, ChangeNameForm, ChangeEmailForm


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('home'))
            # next_page = request.args.get('next')
            # return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = None
    if request.method == 'POST':
        if 'change_name' in request.form:
            form = ChangeNameForm()
        elif 'change_email' in request.form:
            form = ChangeEmailForm()
        elif 'change_password' in request.form:
            form = ChangePasswordForm()
        elif 'new_username' in request.form:
            form = ChangeNameForm(request.form)
            if form.validate_on_submit():
                current_user.username = form.new_username.data
                db.session.commit()
                flash('Your username has been updated!', 'success')
                return redirect(url_for('account'))
        elif 'new_email' in request.form:
            form = ChangeEmailForm(request.form)
            if form.validate_on_submit():
                current_user.email = form.new_email.data
                db.session.commit()
                flash('Your email has been updated!', 'success')
                return redirect(url_for('account'))
        elif 'current_password' in request.form:
            form = ChangePasswordForm(request.form)
            if form.validate_on_submit():
                if current_user.check_password(form.current_password.data):
                    current_user.set_password(form.new_password.data)
                    db.session.commit()
                    flash('Your password has been updated!', 'success')
                    return redirect(url_for('account'))
                else:
                    flash('Current password is incorrect', 'danger')
    return render_template('account.html', form=form)
