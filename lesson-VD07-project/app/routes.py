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


def handle_form(form_class, form_action, success_message, password):
    form = form_class(request.form)
    if form.validate_on_submit():
        if password:
            if not current_user.check_password(form.current_password.data):
                flash('Current password is incorrect', 'danger')
                return form
        form_action(form)
        # db.session.commit()
        # flash(success_message, 'success')
        # return redirect(url_for('account'))
        try:
            db.session.commit()
            flash(success_message, 'success')
            return redirect(url_for('account'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
            return form
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {getattr(form, field).label.text}: {error}', 'danger')
    return form


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = None
    form_starters = {
        'change_name': ChangeNameForm,
        'change_email': ChangeEmailForm,
        'change_password': ChangePasswordForm
    }
    form_handlers = {
        'new_username': (ChangeNameForm, lambda form: setattr(current_user, 'username', form.new_username.data),
                         'Your username has been updated!', False),
        'new_email': (ChangeEmailForm, lambda form: setattr(current_user, 'email', form.new_email.data),
                      'Your email has been updated!', False),
        'current_password': (ChangePasswordForm, lambda form: current_user.set_password(form.new_password.data),
                             'Your password has been updated!', True)
    }
    if request.method == 'POST':
        for key, value in form_starters.items():
            if key in request.form:
                form = value()
                return render_template('account.html', form=form)
        for key, value in form_handlers.items():
            if key in request.form:
                form_class, form_action, success_message, password = value
                form = handle_form(form_class, form_action, success_message, password)
    return render_template('account.html', form=form)

    #     if 'change_name' in request.form:
    #         form = ChangeNameForm()
    #     elif 'change_email' in request.form:
    #         form = ChangeEmailForm()
    #     elif 'change_password' in request.form:
    #         form = ChangePasswordForm()
    #     elif 'new_username' in request.form:
    #         form = ChangeNameForm(request.form)
    #         if form.validate_on_submit():
    #             current_user.username = form.new_username.data
    #             db.session.commit()
    #             flash('Your username has been updated!', 'success')
    #             return redirect(url_for('account'))
    #     elif 'new_email' in request.form:
    #         form = ChangeEmailForm(request.form)
    #         if form.validate_on_submit():
    #             current_user.email = form.new_email.data
    #             db.session.commit()
    #             flash('Your email has been updated!', 'success')
    #             return redirect(url_for('account'))
    #     elif 'current_password' in request.form:
    #         form = ChangePasswordForm(request.form)
    #         if form.validate_on_submit():
    #             if current_user.check_password(form.current_password.data):
    #                 current_user.set_password(form.new_password.data)
    #                 db.session.commit()
    #                 flash('Your password has been updated!', 'success')
    #                 return redirect(url_for('account'))
    #             else:
    #                 flash('Current password is incorrect', 'danger')
    # return render_template('account.html', form=form)
