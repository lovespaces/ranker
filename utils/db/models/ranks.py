from sqlalchemy import BigInteger, Text, Column, Integer
from sqlalchemy.orm import relationship, mapped_column, Mapped
from ..base import Base


class Ranks(Base):
    __tablename__ = "ranks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    rank_name: Mapped[str] = mapped_column(Text, nullable=False)
    role_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    required_points: Mapped[int] = mapped_column(nullable=True)

    user = relationship("Users", back_populates="rank")
