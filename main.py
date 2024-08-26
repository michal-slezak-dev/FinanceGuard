from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap4
from flask_wtf import CSRFProtect
from forms import ContactForm
from contact import send_mail
from datetime import date
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
csrf = CSRFProtect(app)
Bootstrap4(app)

current_year = date.today().year


@app.route("/login")
def login():
    return "hej"


@app.route("/register")
def register():
    return "hej"


@app.route("/")
def home():
    return render_template("index.html", year=current_year)


@app.route("/features")
def features():
    return render_template("features.html", year=current_year)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    contact_form = ContactForm()

    if contact_form.validate_on_submit():
        username = contact_form.name.data
        user_email = contact_form.email.data
        message = contact_form.message.data

        my_email, my_pass = os.getenv('EMAIL'), os.getenv('EMAIL_APP_PASS')
        send_mail(username, message, user_email, my_email, my_email, my_pass)

    return render_template("contact.html", year=current_year, form=contact_form)


if __name__ == "__main__":
    app.run(debug=True)