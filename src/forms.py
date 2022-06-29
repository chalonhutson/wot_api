from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, validators, RadioField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, AnyOf, Regexp

class RegisterForm(FlaskForm):
    first_name = StringField("First Name",
     validators=[Length(min=4, max=25)])
    last_name = StringField("Last Name",
    validators=[Length(min=4, max=25)])
    discord = StringField("Discord Tag",
    validators=[Length(min=4, max=25)])
    submit = SubmitField("Submit")
