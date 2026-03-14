from utils.db.connection import get_session
from utils.db.models import Ranks, Users


def AddPoints(userid: int, incr_points: int):
    with get_session() as session:
        user = session.query(Users).filter_by(id=userid).first()

        if not user:
            user = Users(id=userid, points=0, rank_id=1)
            session.add(user)
            session.flush()

        user.points += incr_points
        rank = session.query(Ranks.id).filter(Ranks.required_points < user.points).scalar()

        if rank is not None:
            if user.rank_id != rank:
                user.rank_id = rank

    return user
