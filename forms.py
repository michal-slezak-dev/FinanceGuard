from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, DateField, BooleanField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from app import app, db
from models import Category

with app.app_context():
    available_categories = db.session.execute(db.select(Category.category_name)).all()


def chek_if_non_negative_num(form, field):
    if field.data <= 0:
        raise ValidationError("Limit Amount must be a non-negative number!")


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Submit")


class DeleteForm(FlaskForm):
    delete = SubmitField("Delete Account")


class AddCategory(FlaskForm):
    category_name = StringField("Category Name", validators=[DataRequired()])
    add_category = SubmitField("Add Category")


class DeleteCategory(FlaskForm):
    delete_category = SubmitField("Delete", render_kw={"class": "btn btn-danger"})


class BudgetPopup(FlaskForm):
    add_budget = SubmitField("Add Budget", render_kw={"class": "mb-2 btn btn-lg rounded-3 btn-primary"})


class AddBudget(FlaskForm):
    budget_name = StringField("Budget Name", validators=[DataRequired()], render_kw={"for": "floatingInput", "class": "form-control rounded-3", "id": "floatingInput", "novalidate": True})
    limit_amount = IntegerField("Limit Amount", validators=[DataRequired(), chek_if_non_negative_num], render_kw={"for": "floatingInput", "class": "form-control rounded-3", "id": "floatingInput", "novalidate": True})
    category_choice = SelectField("Choose a Category", choices=[("", "Category")] + [(category_name[0], category_name[0]) for category_name in available_categories], validators=[DataRequired()], render_kw={"novalidate": True})
    add_budget = SubmitField("Add Budget", render_kw={"class": "w-100 mb-2 btn btn-lg rounded-3 btn-primary"})


class EditBudgetPopup(FlaskForm):
    edit_budget = SubmitField("Edit", render_kw={"class": "btn btn-primary"})


class EditBudget(FlaskForm):
    budget_name = StringField("Budget Name", validators=[DataRequired()], render_kw={"for": "floatingInput", "class": "form-control rounded-3", "id": "floatingInput", "novalidate": True})
    limit_amount = IntegerField("Limit Amount", validators=[DataRequired(), chek_if_non_negative_num], render_kw={"for": "floatingInput", "class": "form-control rounded-3", "id": "floatingInput", "novalidate": True})
    category_choice = SelectField("Choose a Category", choices=[("", "Category")] + [(category_name[0], category_name[0]) for category_name in available_categories], validators=[DataRequired()], render_kw={"novalidate": True})
    save_changes = SubmitField("Save Changes", render_kw={"class": "w-100 mb-2 btn btn-lg rounded-3 btn-primary"})


class DeleteBudget(FlaskForm):
    delete_budget = SubmitField("Delete", render_kw={"class": "btn btn-danger"})


class TransactionPopup(FlaskForm):
    add_budget = SubmitField("Add Transaction", render_kw={"class": "mb-2 btn btn-lg rounded-3 btn-primary"})


class AddTransaction(FlaskForm):
    transaction_name = StringField("Transaction Name", validators=[DataRequired()], render_kw={"for": "floatingInput", "class": "form-control rounded-3", "id": "floatingInput", "novalidate": True})
    transaction_date = DateField("Date", validators=[DataRequired(), ], render_kw={"for": "floatingInput", "class": "form-control rounded-3", "id": "floatingInput", "novalidate": True})
    is_recurring = BooleanField("Is it recurring?", render_kw={"for": "flexCheckDefault", "class": "form-check-input rounded-3", "id": "flexCheckDefault", "novalidate": True})
    recurrence_pattern = StringField("How often is it renewed?", render_kw={"for": "floatingInput", "class": "form-control rounded-3", "id": "floatingInput", "novalidate": True, "value": "W - weekly, M - monthly, Y - yearly, D - daily"})
    recurrence_start = DateField("Start Date", render_kw={"for": "floatingInput", "class": "form-control rounded-3", "id": "floatingInput", "novalidate": True, "value": "000-00-00"})
    add_transaction = SubmitField("Add Transaction", render_kw={"class": "w-100 mb-2 btn btn-lg rounded-3 btn-primary"})


class EditTransaction(FlaskForm):
    budget_name = StringField("Budget Name", validators=[DataRequired()], render_kw={"for": "floatingInput", "class": "form-control rounded-3", "id": "floatingInput", "novalidate": True})
    limit_amount = IntegerField("Limit Amount", validators=[DataRequired(), chek_if_non_negative_num], render_kw={"for": "floatingInput", "class": "form-control rounded-3", "id": "floatingInput", "novalidate": True})
    category_choice = SelectField("Choose a Category", choices=[("", "Category")] + [(category_name[0], category_name[0]) for category_name in available_categories], validators=[DataRequired()], render_kw={"novalidate": True})
    save_changes = SubmitField("Save Changes", render_kw={"class": "w-100 mb-2 btn btn-lg rounded-3 btn-primary"})


class DeleteTransaction(FlaskForm):
    delete_budget = SubmitField("Delete", render_kw={"class": "btn btn-danger"})

