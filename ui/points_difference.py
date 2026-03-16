from discord import ui


class PointsDiff(ui.TextDisplay):
    def __init__(
        self,
        *,
        old_points: int,
        new_points: int,
        id: int | None = None,
        killed_first: bool = False,
        is_last: bool = False,
        was_first: bool = False,
    ) -> None:
        super().__init__(content="", id=id)

        differences = new_points - old_points
        sign = ""
        if differences == 0:
            sign = "± 0"
        else:
            if killed_first:
                differences -= 15
                sign += "\n+ 15 (KILLED TOP PLAYER IN LEADERBOARD)"
            if is_last:
                differences += 5
                sign += "\n- 5 (BOTTOM PENALTY)"
            if was_first:
                differences += 3
                sign += "\n- 3 (RANKING LOSS PENALTY)"

            sign = f"\n+ HITS, KILLS: {abs(differences)}"
        self.content = f"## 🪙 ポイントの増減\n```diff\n{old_points} -> {new_points}\n{sign}\n```"
