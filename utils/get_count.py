from utils.db.connection import get_session
from utils.db.models import Ranks, Users


def RanksCount() -> int:
    with get_session() as session:
        return session.query(Ranks).count()


def UsersCount() -> int:
    with get_session() as session:
        return session.query(Users).count()
