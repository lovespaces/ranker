from utils.db.connection import get_session
from utils.db.models import Users
from utils.get_count import RanksCount
from sqlalchemy import select, func


def IsFourth(rankid: int) -> bool:
    count = RanksCount() - 1

    if rankid == count:
        with get_session() as session:
            query = select(func.count()).select_from(Users).where(Users.rank_id == count)
            user_count = session.execute(query).scalar_one()
            if user_count < 4:
                return True

    return False
