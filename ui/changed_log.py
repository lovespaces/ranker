from discord import ui


class ChangeLog(ui.TextDisplay):
    def __init__(self, content: str, *, id: int | None = None) -> None:
        super().__init__(content, id=id)
