import discord
from discord.ext import commands
from discord import app_commands

# utils import
from utils.whois_top import GetLeaderboard

# ui import
from ui.base_layout import BaseLayout
from ui.leaderboard import LeaderboardSec


class LeaderboardCmd(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # TODO: ページ機能の追加（だるい）
    @app_commands.command(name="top", description="総合ポイントのランキングを表示")
    @app_commands.guild_only()
    async def top(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True, ephemeral=True)

        view = BaseLayout()
        container = discord.ui.Container()
        container.add_item(LeaderboardSec(users=GetLeaderboard(), userid=interaction.user.id))
        container.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.small))
        container.add_item(discord.ui.TextDisplay("### 未プレイのプレイヤーは表示されません。"))
        view.add_item(container)

        await interaction.followup.send(view=view, silent=True)


async def setup(bot):
    await bot.add_cog(LeaderboardCmd(bot))
