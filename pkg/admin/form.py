from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, SelectField, TelField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from pkg.models import State, City

class AdminLoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()] )
    submit = SubmitField('Login')