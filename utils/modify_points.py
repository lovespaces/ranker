from utils.db.connection import get_session
from utils.db.models import Ranks, Users
from utils.get_user import GetUser
from utils.db.schemas import UsersSc


def AddPoints(userid: int, points: int) -> UsersSc:
    GetUser(userid)

    with get_session() as session:
        user = session.query(Users).filter_by(id=userid).first()
        if user is None:
            raise ValueError("User was not found.")
        user.points += points
        print(user.points)
        rank = (
            session.query(Ranks.id)
            .filter(Ranks.required_points <= user.points)
            .order_by(Ranks.required_points.asc())
            .limit(1)
            .scalar()
        )
        if rank is not None:
            if user.rank_id != rank:
                user.rank_id = rank

        return UsersSc(id=user.id, points=user.points, rank_id=user.rank_id, game_username=user.game_username)
