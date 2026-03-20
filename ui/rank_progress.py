from discord import ui

from utils.db.schemas import RanksSc


class RankProgSec(ui.TextDisplay):
    def __init__(
        self,
        *,
        is_non: bool = False,
        is_highest: bool = False,
        is_fourth: bool = False,
        rank: RanksSc | None,
        next_rank: RanksSc | None,
        points: int,
        id: int | None = None,
    ) -> None:
        content = "## 📊 ランク進捗"
        if is_non:
            content += "```まだ試合をしていません！```"
        elif rank is not None:
            if is_highest:
                content += f"\n```{rank.rank_name}\n{points}P , ✨最高ランク✨```"
            elif is_fourth:
                content += f"\n```{rank.rank_name}\n{points}P , ⚡四皇の一人です⚡```"
            if next_rank is not None:
                require = next_rank.required_points - points
                content += f"\n```{rank.rank_name} -> {next_rank.rank_name}\n{points}P , 次ランクまで: {require}P```"
        else:
            raise ValueError("Current rank is unavailable")
        super().__init__(content, id=id)
