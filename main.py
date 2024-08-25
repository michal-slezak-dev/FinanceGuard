from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap4
from forms import ContactForm
from datetime import date
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
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


@app.route("/contact")
def contact():
    contact_form = ContactForm()
    return render_template("contact.html", year=current_year, form=contact_form)


if __name__ == "__main__":
    app.run(debug=True)