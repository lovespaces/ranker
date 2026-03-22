from utils.db.connection import get_session
from utils.db.models import Ranks, Users
from utils.get_user import GetUser
from utils.db.schemas import UsersSc
from utils.is_fourth import IsFourth
from utils.get_count import RanksCount
from sqlalchemy import select, func


def AddPoints(userid: int, points: int) -> UsersSc:
    print("== ADD POINTS ==")
    GetUser(userid)

    with get_session() as session:
        query = select(Users).where(Users.id == userid)
        user = session.execute(query).scalar()
        if user is None:
            raise ValueError("User was not found.")
        print(f"> ADDING {points} POINTS ...")
        user.points += points
        print(f"> USER CURRENT POINTS: {user.points}")
        if user.points < 0:
            print("> RESETTING USERS POINTS ...")
            user.points = 0

        query = select(func.max(Ranks.id)).where(Ranks.required_points <= user.points, Ranks.id != -1)
        rank = session.execute(query).scalar()
        count = RanksCount() - 1
        if rank is not None:
            if user.rank_id != rank:
                print("> RANK IS DIFFERENT")
                if rank == count:
                    if IsFourth(rank):
                        user.rank_id = rank
                else:
                    user.rank_id = rank

        print("== ADD POINTS ==")
        return UsersSc(user.id, user.points, user.rank_id, user.game_username, user.is_bedrock)
