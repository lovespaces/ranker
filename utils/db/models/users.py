from sqlalchemy import BigInteger, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..base import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    points: Mapped[int] = mapped_column(nullable=False)
    rank_id: Mapped[int] = mapped_column(ForeignKey("ranks.id"), nullable=False)
    game_username: Mapped[str] = mapped_column(Text, unique=True)

    rank = relationship("Ranks", back_populates="user")
