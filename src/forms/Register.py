from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])

    fullname = StringField("Full name",validators=[DataRequired()])

    password = PasswordField("Password",validators=[DataRequired()])

    submit = SubmitField("Register")
