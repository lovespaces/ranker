from discord import ui

from utils.db.schemas import UsersSc


class LeaderboardSec(ui.TextDisplay):
    def __init__(self, *, users: list[UsersSc], id: int | None = None) -> None:

        content = "## 🏆 総合ランキング"
        for i, user in enumerate(users):
            if i == len(users) - 1:
                content += f"{i + 1}位: <@{user.id}> - {user.points}P"
            else:
                content += f"{i + 1}位: <@{user.id}> - {user.points}P\n"
        super().__init__(content, id=id)
