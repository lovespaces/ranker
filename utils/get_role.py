import discord
from utils.db.connection import get_session
from utils.db.models import Ranks


def GetRole(rank_ids: list[int], guild: discord.Guild) -> list[discord.Role | None]:
    with get_session() as session:
        rank_role_ids = session.query(Ranks.role_id).filter(Ranks.id.in_(rank_ids)).all()
        return [guild.get_role(role.role_id) for role in rank_role_ids]
