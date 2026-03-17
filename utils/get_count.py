from utils.db.connection import get_session
from utils.db.models import Ranks, Users
from sqlalchemy import select, func


def RanksCount() -> int:
    with get_session() as session:
        return session.execute(select(func.count()).select_from(Ranks)).scalar_one()


def UsersCount() -> int:
    with get_session() as session:
        return session.execute(select(func.count()).select_from(Users)).scalar_one()
