from utils.db.connection import get_session
from utils.db.models import Users


def GetUser(userid: int):
    with get_session() as session:
        user = session.query(Users).filter_by(id=userid).first()

        if not user:
            user = Users(id=userid, points=0, rank_id=1)
            session.add(user)

        return user
