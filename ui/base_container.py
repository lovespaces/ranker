from discord import ui


class UserCont(ui.LayoutView):
    row = ui.ActionRow()

    def __init__(self):
        super().__init__()
