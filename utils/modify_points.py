from utils.db.connection import get_session
from utils.db.models import Ranks
from utils.get_user import GetUser


def AddPoints(userid: int, incr_points: int):
    with get_session() as session:
        user = GetUser(userid)

        user.points += incr_points
        rank = session.query(Ranks.id).filter(Ranks.required_points < user.points).scalar()

        if rank is not None:
            if user.rank_id != rank:
                user.rank_id = rank

    return user
