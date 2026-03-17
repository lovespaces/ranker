import discord
from discord.ext import commands
from discord import app_commands

# utils import
from utils.get_user import GetUser
from utils.get_rank import GetRanks
from utils.get_count import RanksCount

# ui import
from ui.base_layout import BaseLayout
from ui.profile_container import UserSec
from ui.rank_progress import RankProgSec
from ui.new_user import NewUserNofitication


class ProfileCmd(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="profile", description="aha")
    @app_commands.guild_only()
    async def profile(self, interaction: discord.Interaction, selector: discord.User | discord.Member | None = None):
        if selector is None:
            selector = interaction.user
        if selector.bot:
            await interaction.response.send_message(
                "ボットの情報は保存されていません。ユーザを選んでください。", ephemeral=True
            )
            return
        if not isinstance(selector, discord.Member) or not isinstance(interaction.guild, discord.Guild):
            return
        await interaction.response.defer(thinking=True)
        user, new_user = GetUser(selector.id)
        rank_count = RanksCount()
        is_non = False
        rank = None
        new_rank = None
        if user.rank_id == -1:
            is_non = True
        elif user.rank_id + 1 == rank_count:
            rank = GetRanks([user.rank_id])[0]
        else:
            rank, new_rank = GetRanks([user.rank_id, user.rank_id + 1])
        view = BaseLayout()
        container = discord.ui.Container()
        container.add_item(UserSec(user, interaction.guild))
        container.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.large))
        container.add_item(RankProgSec(is_non=is_non, rank=rank, next_rank=new_rank, points=user.points))
        if new_user == -1:
            container.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.large))
            container.add_item(NewUserNofitication())
        view.add_item(container)
        await interaction.followup.send(view=view, allowed_mentions=discord.AllowedMentions.none())


async def setup(bot):
    await bot.add_cog(ProfileCmd(bot))
