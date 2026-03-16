from utils.db.connection import get_session
from utils.db.models import Users
from utils.db.schemas import UsersSc


# UsersScに対応
def GetLeaderboard(limit: int = -1) -> list[UsersSc]:
    with get_session() as session:
        if limit == -1:
            users = session.query(Users).order_by(Users.points.desc()).all()
        else:
            users = session.query(Users).order_by(Users.points.desc()).limit(limit).all()
        if not users:
            return []
        return [
            UsersSc(id=user.id, points=user.points, rank_id=user.rank_id, game_username=user.game_username)
            for user in users
        ]
