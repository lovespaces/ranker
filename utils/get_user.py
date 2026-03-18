from utils.db.connection import get_session
from utils.db.models import Users
from utils.db.schemas import UsersSc
from sqlalchemy import select


def GetUser(userid: int) -> tuple[UsersSc, bool]:
    with get_session() as session:
        query = select(Users).where(Users.id == userid)
        user = session.execute(query).scalar()
        new_user = False

        if not user:
            user = Users(id=userid, points=0, rank_id=-1)
            session.add(user)
            new_user = True

        return UsersSc(user.id, user.points, user.rank_id, user.game_username), new_user


# 新規登録、でけません。
def GetUsers(userids: list[int]) -> list[UsersSc] | None:
    with get_session() as session:
        query = select(Users).where(Users.id.in_(userids))
        users = session.execute(query).scalars().all()
        if users is None:
            return None
        return [UsersSc(user.id, user.points, user.rank_id, user.game_username) for user in users]


def GetUserWithoutCreation(userid: int) -> UsersSc | None:
    with get_session() as session:
        query = select(Users).where(Users.id == userid)
        user = session.execute(query).scalar()
        if user is None:
            return None
        return UsersSc(user.id, user.points, user.rank_id, user.game_username)
