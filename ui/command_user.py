from discord import ui


class Commander(ui.TextDisplay):
    def __init__(self, mention: str, *, id: int | None = None) -> None:
        content = mention + " による実行"
        super().__init__(content, id=id)
