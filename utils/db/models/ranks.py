from sqlalchemy import BigInteger, Text, Identity, Integer
from sqlalchemy.orm import relationship, mapped_column, Mapped
from utils.db.base import Base


class Ranks(Base):
    __tablename__ = "ranks"

    id: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True)
    rank_name: Mapped[str] = mapped_column(Text, nullable=False)
    role_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    required_points: Mapped[int] = mapped_column(nullable=False)

    user = relationship("Users", back_populates="rank")
