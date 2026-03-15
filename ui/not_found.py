from discord import ui


class NotFound(ui.TextDisplay):
    def __init__(self, *, id: int | None = None) -> None:
        super().__init__(content="## ❗ データが見つかりません", id=id)
