from utils.db.connection import get_session
from utils.db.models import Users
from utils.db.schemas import UsersSc


def GetUser(userid: int) -> UsersSc:
    with get_session() as session:
        user = session.query(Users).filter_by(id=userid).first()

        if not user:
            user = Users(id=userid, points=0, rank_id=-1)
            session.add(user)

        return UsersSc(id=user.id, points=user.points, rank_id=user.rank_id, game_username=user.game_username)
