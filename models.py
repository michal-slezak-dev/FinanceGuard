import datetime

from sqlalchemy import ForeignKey, String, Integer, DATE, BOOLEAN, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin
from app import db


# Users
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(256), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    budgets = relationship("Budget", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email}, pass_hash={self.password_hash}"


class Category(db.Model):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    category_name: Mapped[str] = mapped_column(String(16), nullable=False)
    budgets = relationship("Budget", back_populates="category")


class Type(db.Model):
    __tablename__ = "types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    type_name: Mapped[str] = mapped_column(String(8), nullable=False)
    transactions = relationship("Transaction", back_populates="transaction_type")


class Budget(db.Model):
    __tablename__ = "budgets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    user_id = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="budgets")
    category_id = mapped_column(ForeignKey("categories.id"))
    category = relationship("Category", back_populates="budgets")
    budget_name: Mapped[str] = mapped_column(String(128), nullable=False)
    limit_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    spent_amount: Mapped[int] = mapped_column(Integer, nullable=True)
    transactions = relationship("Transaction", back_populates="budgets")


class Transaction(db.Model):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    user_id = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="transactions")
    budget_id = mapped_column(ForeignKey("budgets.id"))
    budgets = relationship("Budget", back_populates="transactions")
    type_id = mapped_column(ForeignKey("types.id"))
    transaction_type = relationship("Type", back_populates="transactions")
    transaction_amount: Mapped[float] = mapped_column(Float, nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    transaction_date: Mapped[datetime.date] = mapped_column(DATE, nullable=False)
    is_recurring: Mapped[bool] = mapped_column(BOOLEAN, nullable=False)
    recurrence_pattern: Mapped[str] = mapped_column(String(2), nullable=True)
    recurrence_start: Mapped[datetime.date] = mapped_column(DATE, nullable=True)


