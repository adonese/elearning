from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import validators
from wtforms.fields.html5 import EmailField
from wtforms import SubmitField
from wtforms import PasswordField
from wtforms import BooleanField

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[validators.DataRequired("Please Enter your name")])
    email = EmailField("Email", validators=[validators.DataRequired("Please Enter your email"),
                                             validators.Email("Enter a valid email.")])
    password = PasswordField("You password", validators=[validators.Required()])
    subject = StringField("Better to write a subject?")
    message = TextAreaField("Do you want to register, or <strong>just</strong> chat?",
                          validators=[validators.DataRequired("Don't you have any message? That's odd.")])
    submit = SubmitField("Hooray!")


class RegisterationForm(FlaskForm):
    username = StringField("Username", validators=[validators.Length(min=4, max=20)])
    email = EmailField("Email", validators=[validators.Length(min=4, max=50), validators.Email("Enter a valid email.")])
    password = PasswordField("Password", validators=[validators.Required(), validators.EqualTo("confirm", message="Password must match.")])
    confirm = PasswordField("Repeat Password.")
    accept_tos = BooleanField("I accept the terms of service and the privacy notice.", validators=[validators.Required()])
    submit = SubmitField("Good!")


