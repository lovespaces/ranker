from utils.db.connection import get_session
from utils.db.models import Users


# UsersScに対応
def GetLeaderboard(limit: int = -1) -> list[Users]:
    with get_session() as session:
        if limit == -1:
            users = session.query(Users).order_by(Users.points.desc()).all()
        else:
            users = session.query(Users).order_by(Users.points.desc()).limit(limit).all()
        if not users:
            return []
        return users
