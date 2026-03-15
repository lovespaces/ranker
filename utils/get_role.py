import discord
from utils.db.connection import get_session
from utils.db.models import Ranks


def GetRole(rank_ids: list[int], guild: discord.Guild) -> list[discord.Role | None]:

    with get_session() as session:
        rank_role_ids = session.query(Ranks.role_id).filter(Ranks.id.in_(rank_ids)).scalar()

    return [guild.get_role(rank_role_id) for rank_role_id in rank_role_ids]
