import discord
from discord.ext import commands
from discord import app_commands

# utils import
from utils.get_user import GetUser, GetUserWithMCID
from utils.modify_points import AddPoints
from utils.calculate_points import Calc
from utils.whois_top import GetLeaderboard
from utils.get_role import GetRole
from utils.get_count import RanksCount

from utils.types.log import LogType

# ui import
from ui.base_layout import BaseLayout
from ui.profile_container import UserSec
from ui.points_difference import PointsDiff
from ui.roles_changes import ChangesRls
from ui.command_user import Commander
from ui.game_result import GameResult
from ui.nofitication import Nofitication

from dotenv import load_dotenv
import os

load_dotenv()
editable = os.getenv("DISCORD_EDITABLE_ROLE_ID")
if editable is None:
    raise ValueError("DISCORD_EDITABLE_ROLE_ID is unknown")


class ResultCmd(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="result", description="試合結果を記録")
    @app_commands.describe(
        leaderboard="プレイヤーの試合順位を入力",
        selector="プレイヤーを選ばない場合は自分が対象になります",
        hits="プレイヤーのヒット数を入力",
        kills="プレイヤーのキル数を入力",
        killed_first="総合ランキングのトップをキルした場合はTrue",
        is_last="最下位の場合はTrue",
    )
    @app_commands.guild_only()
    async def result(
        self,
        interaction: discord.Interaction,
        leaderboard: int,
        selector: discord.User | discord.Member | None = None,
        mcid: str | None = None,
        hits: int = 0,
        kills: int = 0,
        killed_first: bool = False,
        is_last: bool = False,
    ):
        if selector is None:
            selector = interaction.user
        if (
            not isinstance(interaction.user, discord.Member)
            or not isinstance(interaction.guild, discord.Guild)
            or not isinstance(selector, discord.Member)
        ):
            return
        await interaction.response.defer(thinking=True, ephemeral=True)
        assert editable is not None
        editable_role = interaction.guild.get_role(int(editable))
        if editable_role not in interaction.user.roles:
            await interaction.followup.send("❗ ランク管理ができるロールを持っていません")
            return
        was_first = False
        was_king = False
        is_new = False
        if mcid is not None:
            old_user = GetUserWithMCID(mcid)
            if old_user is None:
                await interaction.followup.send(f"❗ {LogType.NOT_EXISTS.value}")
                return
        else:
            old_user, is_new = GetUser(selector.id)
        try:
            top_user = GetLeaderboard(1)[0]
            if selector.id == top_user.id and leaderboard > 1:
                was_first = True
        except IndexError:
            pass
        if old_user.rank_id >= RanksCount() - 1:
            was_king = True
        points = Calc(hits, kills, killed_first, is_last, was_king, was_first)
        new_user = AddPoints(selector.id, points)

        view = BaseLayout()
        container = discord.ui.Container()
        container.add_item(UserSec(old_user, interaction.guild))
        container.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.large))
        container.add_item(GameResult(leaderboard=leaderboard, hits=hits, kills=kills))
        container.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.large))
        container.add_item(
            PointsDiff(
                old_points=old_user.points,
                new_points=new_user.points,
                killed_first=killed_first,
                is_last=is_last,
                was_king=was_king,
                was_first=was_first,
            )
        )
        container.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.large))
        is_demote = False
        if old_user.rank_id != new_user.rank_id:
            if old_user.rank_id == -1:
                old_role = None
                new_role = GetRole([new_user.rank_id], interaction.guild)[0]
            else:
                if old_user.rank_id > new_user.rank_id:
                    is_demote = True
                old_role, new_role = GetRole([old_user.rank_id, new_user.rank_id], interaction.guild)
            if (old_role is None and old_user.rank_id != -1) or new_role is None:
                await interaction.followup.send(
                    "❗ ロールを付与できませんでした。\nランク用のロールが削除されているか、存在しません。"
                )
                return
            try:
                if old_role is not None:
                    await selector.remove_roles(old_role)
                await selector.add_roles(new_role)
            except discord.Forbidden:
                await interaction.followup.send(
                    "❗ ロールを付与できませんでした。\n付与するランクロールがボットのロールの下にあることを確認してください。"
                )
                return
            except discord.HTTPException:
                await interaction.followup.send("❗ ロールを付与できませんでした。\n通信に失敗しました。")
                return
            if old_role is None:
                container.add_item(
                    ChangesRls(new_role_id=new_role.id, is_new=True, is_changed=True, is_demote=is_demote)
                )
            else:
                container.add_item(
                    ChangesRls(old_role_id=old_role.id, new_role_id=new_role.id, is_new=False, is_changed=True)
                )
        else:
            container.add_item(ChangesRls(is_changed=False))
        if is_new:
            container.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.small))
            container.add_item(Nofitication(log=LogType.NEWUSER))
        container.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.small))
        container.add_item(Commander(interaction.user.mention))
        view.add_item(container)
        await interaction.followup.send("✅ リザルトを登録しました")
        if not isinstance(interaction.channel, discord.abc.Messageable):
            await interaction.followup.send(view=view, allowed_mentions=discord.AllowedMentions.none(), silent=True)
        else:
            await interaction.channel.send(view=view, allowed_mentions=discord.AllowedMentions.none(), silent=True)


async def setup(bot):
    await bot.add_cog(ResultCmd(bot))
