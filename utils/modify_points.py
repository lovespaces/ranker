from utils.db.connection import get_session
from utils.db.models import Ranks
from utils.get_user import GetUser


def AddPoints(userid: int, hits: int, kills: int, kill_first: bool):
    user = GetUser(userid)
    incr_points = 0
    incr_points += hits + kills

    user.points += incr_points

    with get_session() as session:
        user = session.merge(user)
        rank = session.query(Ranks.id).filter(Ranks.required_points < user.points).scalar()

        if rank is not None:
            if user.rank_id != rank:
                user.rank_id = rank
    return user
