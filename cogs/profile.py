import discord
from discord.ext import commands
from discord import app_commands

# utils import
from utils.get_user import GetUser

# ui import
from ui.base_layout import BaseLayout
from ui.profile_container import UserSec
from ui.new_user import NewUserNofitication


class ProfileCmd(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="profile", description="aha")
    @app_commands.guild_only()
    async def profile(self, interaction: discord.Interaction, selector: discord.User | discord.Member | None = None):
        if selector is None:
            selector = interaction.user
        if not isinstance(selector, discord.Member) or not isinstance(interaction.guild, discord.Guild):
            return
        await interaction.response.defer(thinking=True)
        user = GetUser(selector.id)
        view = BaseLayout()
        container = discord.ui.Container()
        container.add_item(UserSec(user, interaction.guild))
        if user.rank_id == -1:
            container.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.large))
            container.add_item(NewUserNofitication())
        view.add_item(container)
        await interaction.followup.send(view=view, allowed_mentions=discord.AllowedMentions.none())


async def setup(bot):
    await bot.add_cog(ProfileCmd(bot))
