import discord
from discord import ui


# memo.pngを参照


class UserCont(ui.LayoutView):
    def __init__(self):
        super().__init__()

        # For this example, we'll use multiple sections to organize the settings.
        container = ui.Container()
        container.add_item(
            ui.Section(
                "# <@305607244945293314>",
                "points: `500`",
                "user_name: `lovespaces`",
                accessory=ui.Thumbnail("https://mc-heads.net/avatar/lovespaces/100"),
            )
        )
        container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.large))
        container.add_item(ui.TextDisplay("### 🪙 ポイントの変更\n`500 -> 600`"))
        container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.small))
        container.add_item(
            ui.TextDisplay(
                "### ❗ 付与されているロールが変更されました\n- <@&1482392428169269501> 解除\n- <@&1482392461551865877> 付与"
            )
        )
        container.accent_color = discord.Color.blurple()
        self.add_item(container)
