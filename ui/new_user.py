from discord import ui


class NewUserNofitication(ui.TextDisplay):
    def __init__(self, *, id: int | None = None) -> None:
        super().__init__("❗ データベースに存在しないユーザーのため、新規作成しました。", id=id)
