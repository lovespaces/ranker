import discord
from discord.ext import commands
from discord import app_commands

# utils import
from utils.get_user import GetUser, GetUserWithoutCreation
from utils.get_rank import GetRank, GetRanks
from utils.get_count import RanksCount

from utils.types.log import LogType

# ui import
from ui.base_layout import BaseLayout
from ui.profile_container import UserSec
from ui.rank_progress import RankProgSec
from ui.nofitication import Nofitication


class ProfileCmd(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="profile", description="自分／他プレイヤーのプロフィールを表示")
    @app_commands.describe(selector="プレイヤーを選ばない場合は自分が対象になります")
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
        await interaction.response.defer(thinking=True, ephemeral=True)
        new_user = False
        if interaction.user == selector:
            user, new_user = GetUser(selector.id)
        else:
            user = GetUserWithoutCreation(selector.id)
            if user is None:
                await interaction.followup.send(
                    "❗ 選択したプレイヤーの情報が取得できませんでした。\nデータベースに登録されていません。"
                )
                return
        rank_count = RanksCount()
        is_non = False
        rank = None
        new_rank = None
        if user.rank_id == -1:
            is_non = True
        elif user.rank_id + 1 == rank_count:
            rank = GetRank(user.rank_id)
        else:
            rank, new_rank = GetRanks([user.rank_id, user.rank_id + 1])
        view = BaseLayout()
        container = discord.ui.Container()
        container.add_item(UserSec(user, interaction.guild))
        container.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.large))
        container.add_item(RankProgSec(is_non=is_non, rank=rank, next_rank=new_rank, points=user.points))
        if new_user:
            container.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.small))
            container.add_item(Nofitication(log=LogType.NEWUSER))
        view.add_item(container)
        await interaction.followup.send(view=view, allowed_mentions=discord.AllowedMentions.none())


async def setup(bot):
    await bot.add_cog(ProfileCmd(bot))
