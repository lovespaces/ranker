import discord
from discord.ext import commands
from discord import app_commands

from utils.get_user import GetUser
from utils.modify_points import AddPoints
from ui.base_container import UserCont

from dotenv import load_dotenv
import os

load_dotenv()
editable = os.getenv("DISCORD_EDITABLE_ROLE_ID")
if editable is None:
    raise ValueError("DISCORD_EDITABLE_ROLE_ID is unknown")


class ResultCmd(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="result", description="1Hit = a point, 1Kill = 5 points.")
    @app_commands.guild_only()
    async def result(
        self,
        interaction: discord.Interaction,
        leaderboard: int,
        selector: discord.User | discord.Member | None = None,
        hits: int = 0,
        kills: int = 0,
        is_last: bool = False,
    ):
        await interaction.response.defer(thinking=True, ephemeral=True)
        if not isinstance(interaction.user, discord.Member) or not isinstance(interaction.guild, discord.Guild):
            return
        if selector is None:
            selector = interaction.user
        user = GetUser(selector.id)
        view = UserCont(user, interaction.guild)

        await interaction.followup.send(view=view)


async def setup(bot):
    await bot.add_cog(ResultCmd(bot))
