from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime

from fcfmramos.model import db


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    username: Mapped[str] = mapped_column(String(24), unique=True)
    email_verified: Mapped[bool] = mapped_column(default=False)
    registration_date: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )

    departamento_id: Mapped[int] = mapped_column(
        ForeignKey("departamento.id", name="fk_user_departamento")
    )
