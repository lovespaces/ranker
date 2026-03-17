import discord
from discord import ui
from utils.db.schemas import UsersSc
from utils.get_rank import GetRank


class UserSec(ui.Section):
    def __init__(self, user: UsersSc, guild: discord.Guild, id: int | None = None) -> None:
        discord_user = guild.get_member(user.id)
        assert discord_user is not None
        rank = GetRank(user.rank_id)
        print(rank)
        if rank is None:
            rank_name = "存在しないランク"
        else:
            rank_name = rank.rank_name
        if user.game_username is None:
            avatar_url = discord_user.display_avatar.url
        else:
            avatar_url = f"https://mc-heads.net/avatar/{user.game_username}/100"
        accessory = ui.Thumbnail(avatar_url)
        name = "未設定" if user.game_username is None else user.game_username
        content = f"# <@{user.id}>\npoints: `{user.points}`\nrank: `{rank_name}`\nminecraft: `{name}`"

        super().__init__(content, accessory=accessory, id=id)
