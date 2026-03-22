from sqlalchemy import BigInteger, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from utils.db.base import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    points: Mapped[int] = mapped_column(nullable=False)
    rank_id: Mapped[int] = mapped_column(ForeignKey("ranks.id"), nullable=False)
    game_username: Mapped[str | None] = mapped_column(Text, unique=True, nullable=True)
    is_bedrock: Mapped[bool] = mapped_column(Boolean, nullable=False)

    rank = relationship("Ranks", back_populates="user")
