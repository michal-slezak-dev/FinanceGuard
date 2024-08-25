from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, email


# Contact Form
class ContactForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()], render_kw={"class": "form-control"})
    email = StringField("email", validators=[DataRequired(), email()], render_kw={"class": "form-control"})
    message = TextAreaField("message", validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField("submit", render_kw={"class": "form-control"})
