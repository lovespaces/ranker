from discord import ui


class GameResult(ui.TextDisplay):
    def __init__(
        self,
        *,
        leaderboard: int,
        hits: int,
        kills: int,
        id: int | None = None,
    ) -> None:

        super().__init__(
            content=f"## ⚔️ 試合結果\n```順位: {leaderboard}位, ヒット数: {hits}, キル数: {kills}```", id=id
        )
