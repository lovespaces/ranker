from utils.db.connection import get_session
from utils.db.models import Ranks, Users
from utils.get_user import GetUser
from utils.db.schemas import UsersSc
from utils.is_fourth import IsFourth
from sqlalchemy import select, func


def AddPoints(userid: int, points: int) -> UsersSc:
    GetUser(userid)

    with get_session() as session:
        query = select(Users).where(Users.id == userid)
        user = session.execute(query).scalar()
        if user is None:
            raise ValueError("User was not found.")
        user.points += points
        if user.points < 0:
            user.points = 0

        query = select(func.max(Ranks.id)).where(
            Ranks.required_points <= user.points, Ranks.id != user.rank_id, Ranks.id != -1
        )
        rank = session.execute(query).scalar()
        if rank is not None:
            if IsFourth(rank):
                if user.rank_id != rank:
                    user.rank_id = rank

        return UsersSc(id=user.id, points=user.points, rank_id=user.rank_id, game_username=user.game_username)
