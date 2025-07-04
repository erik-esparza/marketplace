from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User

class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user=User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists...')
        
    def validate_email_address(self, email_address_to_check):
        email_address=User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email has been already registered...')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email: ', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password: ', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm your Password: ', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password: ', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class PurchaseItemForm(FlaskForm):
        submit = SubmitField(label='Purchase now')

class SellItemForm(FlaskForm):
        submit = SubmitField(label='Sell now')

# Password reset

class RequestResetForm(FlaskForm):
    email = StringField(label='Your Email', validators=[DataRequired(), Email()])
    submit = SubmitField(label='Send Reset Link')

class ResetPasswordForm(FlaskForm):
    password = PasswordField(label='New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(label='Confirm New Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='Reset Password')
