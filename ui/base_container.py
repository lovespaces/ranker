import discord
from discord import ui
from utils.db.models import Users


class UserCont(ui.LayoutView):
    def __init__(self, user: Users, guild: discord.Guild) -> None:
        super().__init__()

        discord_user = guild.get_member(user.id)

        self.container = ui.Container()
        if user is None or discord_user is None:
            self.container.accent_color = 0xE74C3C
            self.container.add_item(ui.TextDisplay("## ❗ データが見つかりません"))
            return

        if user.game_username is None:
            avatar_url = discord_user.display_avatar.url
        else:
            avatar_url = f"https://mc-heads.net/avatar/{user.game_username}/100"

        self.container.add_item(
            ui.Section(
                f"# <@{user.id}>",
                f"points: `{user.points}`",
                f"minecraft: `{'未設定' if user.game_username is None else user.game_username}`",
                accessory=ui.Thumbnail(avatar_url),
            )
        )
        self.container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.large))
