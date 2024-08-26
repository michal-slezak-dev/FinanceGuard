from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, email


# Contact Form
class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), email()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Submit")
