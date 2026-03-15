from discord import ui


class PointsDiff(ui.TextDisplay):
    def __init__(self, *, old_points: int, new_points: int, id: int | None = None) -> None:
        super().__init__(content="", id=id)

        differences = new_points - old_points
        sign = "+" if differences > 0 else "±" if differences == 0 else "-"
        self.content = f"## 🪙 ポイントの増減\n```diff\n{old_points} -> {new_points}\n{sign} {abs(differences)}\n```"
