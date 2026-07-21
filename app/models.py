from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from datetime import date

class JobApplication(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'), nullable=False)
    company: Mapped[str] = mapped_column(db.String(200), nullable=False)
    role: Mapped[str] = mapped_column(db.String(200), nullable=False)
    status: Mapped[str] = mapped_column(db.String(50), nullable=False)
    date_applied: Mapped[date] = mapped_column(db.Date(), nullable=False)
    date_updated: Mapped[date] = mapped_column(db.Date(), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(db.String(400))
    notes: Mapped[Optional[str]] = mapped_column(db.String(1000))
    url: Mapped[Optional[str]] = mapped_column(db.String(500))


class User(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(db.String(200), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(db.String(200), nullable=False)
