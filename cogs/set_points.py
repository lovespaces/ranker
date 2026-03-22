import discord
from discord.ext import commands
from discord import app_commands

# utils import
from utils.get_user import GetUser, GetUserWithMCID
from utils.get_role import GetRole
from utils.modify_points import AddPoints
from utils.reset_points import ResetPoints

from utils.types.log import LogType

import os
from dotenv import load_dotenv

load_dotenv()
editable = os.getenv("DISCORD_EDITABLE_ROLE_ID")
if editable is None:
    raise ValueError("DISCORD_EDITABLE_ROLE_ID is unavailable")


class SetPointsCmd(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="points", description="プレイヤーのポイントを設定")
    @app_commands.describe(
        points="マイナスを付けることでポイント減少、0でポイントをリセット",
        selector="プレイヤーを選ばない場合は自分が対象になります",
    )
    @app_commands.guild_only()
    async def set_points(
        self,
        interaction: discord.Interaction,
        points: int,
        selector: discord.User | discord.Member | None = None,
        mcid: str | None = None,
    ):
        if selector is None:
            selector = interaction.user
        if (
            not isinstance(interaction.user, discord.Member)
            or not isinstance(interaction.guild, discord.Guild)
            or not isinstance(selector, discord.Member)
        ):
            return
        assert editable is not None
        editable_role = interaction.guild.get_role(int(editable))
        if editable_role not in interaction.user.roles:
            await interaction.response.send_message("❗ ランク管理ができるロールを持っていません")
            return
        await interaction.response.defer(thinking=True)
        is_new = False
        if mcid is None:
            old_user, is_new = GetUser(selector.id)
        else:
            old_user = GetUserWithMCID(mcid)
            if old_user is None:
                await interaction.followup.send(f"❗ {LogType.NOT_EXISTS.value}")
                return
        print((f"=== POINTS COMMAND ===\nUSER: {old_user.id}\nRANK: {old_user.rank_id}\nPOINTS: {old_user.points}"))
        if points == 0:
            new_user = ResetPoints(selector.id)
        else:
            new_user = AddPoints(selector.id, points)
        print(f"NEW POINTS: {new_user.points}\n")
        print(f"AFTER CALCULATE RANK: {new_user.rank_id}\n=== POINTS COMMAND ===")
        difference = new_user.points - old_user.points
        content = f"{selector.mention} のポイントを変更しました。\n```{old_user.points} -> {new_user.points} ({'+' if difference > 0 else '-' if difference < 0 else '±'} {abs(difference)})```"
        if is_new:
            content = f"\n❗ {LogType.NEWUSER.value}"
        if old_user.rank_id != new_user.rank_id:
            if old_user.rank_id == -1:
                old_role = None
                new_role = GetRole([new_user.rank_id], interaction.guild)[0]
            else:
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
        await interaction.followup.send(content, allowed_mentions=discord.AllowedMentions.none(), silent=True)


async def setup(bot):
    await bot.add_cog(SetPointsCmd(bot))
