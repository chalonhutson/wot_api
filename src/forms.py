from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, validators, RadioField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, AnyOf, Regexp, EqualTo

class RegisterForm(FlaskForm):
    first_name = StringField("First Name",
     validators=[Length(min=4, max=25), DataRequired()])
    last_name = StringField("Last Name",
    validators=[Length(min=4, max=25), DataRequired()])
    discord = StringField("Discord Tag",
    validators=[Length(min=4, max=25)])
    submit = SubmitField("Submit")
