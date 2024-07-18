from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=35)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=35)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=35)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Old Password', validators=[DataRequired(), Length(min=6, max=35)])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6, max=35)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')


class ChangeNameForm(FlaskForm):
    new_username = StringField('New Username', validators=[DataRequired(), Length(min=2, max=35)])
    submit = SubmitField('Change Name')

    def validate_new_username(self, new_username):
        user = User.query.filter_by(username=new_username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')


class ChangeEmailForm(FlaskForm):
    new_email = StringField('New Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Change Email')

    def validate_new_email(self, new_email):
        email = User.query.filter_by(email=new_email.data).first()
        if email:
            raise ValidationError('That email is taken. Please choose a different one.')

