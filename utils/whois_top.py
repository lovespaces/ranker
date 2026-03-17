from utils.db.connection import get_session
from utils.db.models import Users
from utils.db.schemas import UsersSc
from sqlalchemy import select


# UsersScに対応
def GetLeaderboard(limit: int = -1) -> list[UsersSc]:
    with get_session() as session:
        if limit == -1:
            query = select(Users).where(Users.points < 0, Users.rank_id <= 1).order_by(Users.points.desc())
        else:
            query = select(Users).where(Users.points < 0, Users.rank_id <= 1).order_by(Users.points.desc()).limit(limit)
        users = session.execute(query).scalars().all()
        if not users:
            return []
        return [
            UsersSc(id=user.id, points=user.points, rank_id=user.rank_id, game_username=user.game_username)
            for user in users
        ]
