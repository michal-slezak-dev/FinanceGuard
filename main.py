from flask import render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap4
from flask_wtf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from models import User, Category, Type, Budget
from forms import ContactForm, LoginForm, RegisterForm, DeleteForm, AddCategory, DeleteCategory, AddBudget, EditBudget, EditBudgetPopup, DeleteBudget, BudgetPopup
from contact import send_mail
from datetime import date
from dotenv import load_dotenv
import os

load_dotenv()

csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)
Bootstrap4(app)

# create our database
# with app.app_context():
#     db.create_all()
current_year = date.today().year


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        email = login_form.email.data
        raw_password = login_form.password.data

        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if not user:
            flash("User doesn't exist! Register first 😊")
            return redirect(url_for('register'))
        elif not check_password_hash(user.password_hash, raw_password):
            flash("Password incorrect, please try again.")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('platform_homepage'))

    return render_template("login.html", form=login_form)


@app.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        username = register_form.name.data
        user_email = register_form.email.data
        raw_password = register_form.password.data

        user = db.session.execute(db.select(User).where(User.email == user_email)).scalar()
        if user:
            flash("You already have an account! Log In 😊")
            return redirect(url_for('login'))

        hashed_password = generate_password_hash(password=raw_password, method="pbkdf2:sha256", salt_length=8)
        new_user = User(
            name=username,
            email=user_email,
            password_hash=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for('platform_homepage', current_user=current_user))

    return render_template("register.html", form=register_form)


@app.route("/dashboard")
@login_required
def platform_homepage():
    return render_template("platform_homepage.html")


@app.route("/transactions", methods=["GET", "POST"])
@login_required
def show_transactions():
    return render_template("transactions.html")


@app.route("/budgets", methods=["GET", "POST"])
@login_required
def show_budgets():
    page = request.args.get("page", 1, type=int)
    per_page = 6

    modal_add = False
    # modal_edit = False
    add_budget = AddBudget()
    add_budget_popup = BudgetPopup()
    edit_budget_popup = EditBudgetPopup()
    delete_budget = DeleteBudget()

    available_budgets = Budget.query.filter_by(user_id=current_user.id).paginate(page=page, per_page=per_page, error_out=False)
    # print(available_budgets.items())
    if not available_budgets.items:
        flash("You don't have any budgets set 😔")

    if add_budget_popup.validate_on_submit():
        modal_add = True

    # if edit_budget_popup.validate_on_submit():
    #     return redirect(url_for("edit_budgets"))

    if add_budget.validate_on_submit():
        budget_name = add_budget.budget_name.data
        budget_category = db.session.query(Category).filter_by(category_name=add_budget.category_choice.data).first()
        limit_amount = add_budget.limit_amount.data

        result = db.session.execute(db.select(Budget).where(Budget.budget_name == budget_name)).scalar()
        if result:
            flash("There already is a budget with this name!")
            return redirect(url_for('show_budgets'))

        new_budget = Budget(
            user=current_user,
            category=budget_category,
            budget_name=budget_name,
            limit_amount=limit_amount,
            spent_amount=0
        )

        db.session.add(new_budget)
        db.session.commit()
        return redirect(url_for("show_budgets"))

    return render_template("budgets.html", budgets=available_budgets, form_add=add_budget, form_del=delete_budget, popup_form_add=add_budget_popup, popup_form_edit=edit_budget_popup, modal_add=modal_add)


@app.route("/edit-budget", methods=["GET", "POST"])
@login_required
def edit_budgets():
    # edit_budget = EditBudget()
    #
    # return redirect(url_for("show_budgets", form_edit=edit_budget))
    ...


@app.route("/delete-budget/<int:budget_id>", methods=["GET", "POST"])
@login_required
def delete_budget(budget_id):
    budget = db.get_or_404(Budget, budget_id)

    db.session.delete(budget)
    db.session.commit()

    return redirect(url_for("show_budgets"))


@app.route("/categories", methods=["GET", "POST"])
@login_required
def show_categories():
    # TODO: Add/Delete categories [user's option]
    # add_category_form = AddCategory()
    # delete_category = DeleteCategory()

    result = db.session.execute(db.select(Category.category_name)).all()
    if not result:
        flash("You don't have any categories 😔")

    # return render_template("categories.html", form_add=add_category_form, categories=result, form_delete=delete_category)
    return render_template("categories.html", categories=result)


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    delete_form = DeleteForm()

    if delete_form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email == current_user.email)).scalar()

        logout_user()

        db.session.delete(user)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template("settings.html", form=delete_form)


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

        to_email = os.getenv('EMAIL')
        from_email = os.getenv('EMAIL')

        send_mail(username, message, from_email, user_email, to_email)
        return render_template("success.html", option="contact")  # contact/login/register

    return render_template("contact.html", year=current_year, form=contact_form)


if __name__ == "__main__":
    app.run(debug=True)
