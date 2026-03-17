from discord import ui

from utils.db.schemas import RanksSc


class RankProgSec(ui.TextDisplay):
    def __init__(
        self,
        *,
        is_non: bool = False,
        rank: RanksSc | None,
        next_rank: RanksSc | None,
        points: int,
        id: int | None = None,
    ) -> None:
        content = "## 📊 ランク進捗"
        if is_non:
            content += "```まだ試合をしていません！```"
        elif rank is not None:
            if next_rank is None:
                if rank == 0:
                    content += f"```{rank.rank_name} ... 最高ランク\n{points}P```"
                else:
                    raise ValueError("Next rank is 'None' and current rank is not the highest.")
            else:
                require = next_rank.required_points - points
                content += f"\n```{rank.rank_name} -> {next_rank.rank_name}\n{points}P , 次ランクまで: {require}P```"
        else:
            raise ValueError("Current rank is unavailable")
        super().__init__(content, id=id)
