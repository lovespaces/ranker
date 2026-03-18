from utils.db.connection import get_session
from utils.db.models import Users
from utils.get_user import GetUser
from utils.db.schemas import UsersSc
from sqlalchemy import select


def ResetPoints(userid: int) -> UsersSc:
    GetUser(userid)

    with get_session() as session:
        query = select(Users).where(Users.id == userid)
        user = session.execute(query).scalar()
        if user is None:
            raise ValueError("User was not found.")
        user.points = 0
        user.rank_id = 0

        return UsersSc(id=user.id, points=user.points, rank_id=user.rank_id, game_username=user.game_username)
