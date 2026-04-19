from sqlalchemy import BigInteger, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str | None] = mapped_column(Text, nullable=True)

    users = relationship("User", back_populates="department")
