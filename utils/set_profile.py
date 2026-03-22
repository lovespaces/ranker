from utils.db.connection import get_session
from utils.db.models import Users
from utils.db.schemas import UsersSc
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError


def SetProfile(userid: int, mcid: str | None, is_bedrock: bool) -> tuple[bool, UsersSc]:
    was_valid = True

    with get_session() as session:
        try:
            with session.begin_nested():
                query = select(Users).where(Users.id == userid)
                user = session.execute(query).scalar()
                if user is None:
                    raise ValueError("User was not found")
                user.game_username = mcid
                user.is_bedrock = is_bedrock
        except IntegrityError:
            was_valid = False
            user = session.execute(select(Users).where(Users.game_username == mcid)).scalar()
            if user is None:
                raise ValueError("literally how?")

        return was_valid, UsersSc(user.id, user.points, user.rank_id, user.game_username, user.is_bedrock)
