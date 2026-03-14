import discord
from discord.ext import commands
from discord import app_commands

from utils.modify_points import AddPoints

from dotenv import load_dotenv
import os

load_dotenv()
editable = os.getenv("DISCORD_EDITABLE_ROLE_ID")
if editable is None:
    raise ValueError("DISCORD_EDITABLE_ROLE_ID is unknown.")


class UserManage(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ランク管理", description="ユーザーのランクをいじる")
    @app_commands.guild_only()
    async def usr_mng(
        self,
        interaction: discord.Interaction,
        追加ポイント: int,
        対象ユーザー: discord.User | discord.Member | None = None,
    ):
        await interaction.response.defer(thinking=True, ephemeral=True)
        if not isinstance(interaction.user, discord.Member):
            return
        if 対象ユーザー is None:
            対象ユーザー = interaction.user
        if editable not in interaction.user.roles:
            await interaction.followup.send("❗ ランク管理ができるロールを持っていません")
            return

        user = AddPoints(対象ユーザー.id, 追加ポイント)

        await interaction.followup.send("✅ 登録が完了しました")


async def setup(bot):
    await bot.add_cog(UserManage(bot))
