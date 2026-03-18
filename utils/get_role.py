import discord
from utils.get_rank import GetRanks


def GetRole(rank_ids: list[int], guild: discord.Guild) -> list[discord.Role | None]:
    ranks = GetRanks(rank_ids)
    if ranks is None:
        return []
    for item in ranks:
        print(item)
    return [guild.get_role(rank.role_id) for rank in ranks]
