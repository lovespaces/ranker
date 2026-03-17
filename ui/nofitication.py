from discord import ui
from utils.types.log import LogType


class Nofitication(ui.TextDisplay):
    def __init__(self, *, log: LogType, id: int | None = None) -> None:
        super().__init__(f"✨ {log.value}", id=id)
