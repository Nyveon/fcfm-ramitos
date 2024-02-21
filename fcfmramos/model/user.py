from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from fcfmramos.model import db


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    username: Mapped[str] = mapped_column(String(24), unique=True)
    email_verified: Mapped[bool] = mapped_column(default=False)
    registration_date: Mapped[datetime]
