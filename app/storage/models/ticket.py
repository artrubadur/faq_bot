from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.storage.base import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    author_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id"))
    responder_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.telegram_id"), nullable=True
    )

    question_text: Mapped[str] = mapped_column(String(384))
    answer_text: Mapped[str] = mapped_column(String(384), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    answered_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
