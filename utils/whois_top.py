from utils.db.connection import get_session
from utils.db.models import Users
from utils.db.schemas import UsersSc
from sqlalchemy import select


def GetLeaderboard(limit: int = -1) -> list[UsersSc]:
    with get_session() as session:
        if limit == -1:
            query = select(Users).where(Users.points > 0, Users.rank_id >= 1).order_by(Users.points.desc())
        else:
            query = (
                select(Users)
                .where(Users.points > 0, Users.rank_id >= 1)
                .order_by(Users.points.desc())
                .limit(limit=limit)
            )
        users = session.execute(query).scalars().all()
        if not users:
            return []
        return [UsersSc(user.id, user.points, user.rank_id, user.game_username, user.is_bedrock) for user in users]
