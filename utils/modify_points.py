from utils.db.connection import get_session
from utils.db.models import Ranks, Users
from utils.get_user import GetUser


def AddPoints(userid: int, points: int) -> Users:
    user = GetUser(userid)
    user.points = points

    with get_session() as session:
        user = session.merge(user)
        rank = session.query(Ranks.id).filter(Ranks.required_points < user.points).scalar()

        if rank is not None:
            if user.rank_id != rank:
                user.rank_id = rank

    return user
