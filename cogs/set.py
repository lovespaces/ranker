import discord
from discord.ext import commands
from discord import app_commands

# utils import
from utils.get_user import GetUser
from utils.set_mcid import SetMCID

from utils.types.log import LogType

# ui import
from ui.base_layout import BaseLayout
from ui.profile_container import UserSec
from ui.nofitication import Nofitication

from dotenv import load_dotenv
import os

load_dotenv()
editable = os.getenv("DISCORD_EDITABLE_ROLE_ID")
if editable is None:
    raise ValueError("DISCORD_EDITABLE_ROLE_ID is unknown")


class SetCmd(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="set", description="プレイヤーの登録／MCIDの設定")
    @app_commands.describe(selector="プレイヤーを選ばない場合は自分が対象になります")
    @app_commands.describe(mcid="他メンバーと同じMCIDの設定はできません")
    @app_commands.guild_only()
    async def set_(
        self,
        interaction: discord.Interaction,
        selector: discord.User | discord.Member | None = None,
        mcid: str | None = None,
    ):
        if selector is None:
            selector = interaction.user
        if selector.bot:
            await interaction.response.send_message(
                "ボットの情報は保存されていません。ユーザを選んでください。", ephemeral=True
            )
        if not isinstance(interaction.user, discord.Member) or not isinstance(interaction.guild, discord.Guild):
            return
        if selector != interaction.user:
            assert editable is not None
            editable_role = interaction.guild.get_role(int(editable))
            if editable_role not in interaction.user.roles:
                await interaction.response.send_message(
                    "❗ 他ユーザーの管理ができるロールを持っていません\n自分のMCIDのみ設定できます", ephemeral=True
                )
                return
        if not isinstance(selector, discord.Member) or not isinstance(interaction.guild, discord.Guild):
            return
        await interaction.response.defer(thinking=True)
        user, is_new = GetUser(selector.id)
        result, new_user = SetMCID(user.id, mcid)
        if not result:
            exist_user = interaction.guild.get_member(new_user.id)
            await interaction.followup.send(
                f"❗ 他のプレイヤーに同じMCIDの人がいます: {exist_user.mention if exist_user else f'ID: ({result})'}",
                ephemeral=True,
            )
            return
        view = BaseLayout()
        container = discord.ui.Container()
        container.add_item(UserSec(new_user, interaction.guild, True))
        if is_new:
            container.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.small))
            container.add_item(Nofitication(log=LogType.NEWUSER))
        else:
            container.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.small))
            container.add_item(Nofitication(log=LogType.CHANGED_MCID))
        view.add_item(container)

        await interaction.followup.send("✅ 設定が完了しました")
        await interaction.followup.send(view=view)


async def setup(bot):
    await bot.add_cog(SetCmd(bot))
