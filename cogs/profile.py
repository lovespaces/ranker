import discord
from discord.ext import commands
from discord import app_commands

# utils import
from utils.get_user import GetUser, GetUserWithoutCreation, GetUserWithMCID
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
    @app_commands.describe(
        selector="プレイヤーを選ばない場合は自分が対象になります", mcid="MCIDで検索する場合はこちらをご利用ください"
    )
    @app_commands.guild_only()
    async def profile(
        self,
        interaction: discord.Interaction,
        selector: discord.User | discord.Member | None = None,
        mcid: str | None = None,
    ):
        new_user = False
        await interaction.response.defer(thinking=True, ephemeral=True)
        if not isinstance(interaction.guild, discord.Guild):
            return
        if mcid is not None:
            user = GetUserWithMCID(mcid)
            if user is None:
                await interaction.followup.send(f"❗ {LogType.NOT_EXISTS.value}")
                return
        else:
            if selector is None:
                selector = interaction.user
            if selector.bot:
                await interaction.followup.send(
                    "ボットの情報は保存されていません。ユーザを選んでください。", ephemeral=True
                )
                return
            if not isinstance(selector, discord.Member):
                return
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
        is_highest = False
        is_fourth = False
        is_non = False
        rank = None
        new_rank = None
        if user.rank_id == -1:
            is_non = True
        elif user.rank_id == rank_count - 1:
            is_fourth = True
        elif user.rank_id == rank_count - 2:
            is_highest = True
        else:
            rank, new_rank = GetRanks([user.rank_id, user.rank_id + 1])
        rank = GetRank(user.rank_id)
        view = BaseLayout()
        container = discord.ui.Container()
        container.add_item(UserSec(user, interaction.guild))
        container.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.large))
        container.add_item(
            RankProgSec(
                is_non=is_non,
                rank=rank,
                next_rank=new_rank,
                points=user.points,
                is_highest=is_highest,
                is_fourth=is_fourth,
            )
        )
        if new_user:
            container.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.small))
            container.add_item(Nofitication(log=LogType.NEWUSER))
        view.add_item(container)
        await interaction.followup.send(view=view, allowed_mentions=discord.AllowedMentions.none())


async def setup(bot):
    await bot.add_cog(ProfileCmd(bot))
