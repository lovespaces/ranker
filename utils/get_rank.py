from utils.db.connection import get_session
from utils.db.models import Ranks
from utils.db.schemas import RanksSc


def GetRank(rank_id: int) -> RanksSc | None:
    with get_session() as session:
        rank = session.query(Ranks).filter_by(id=rank_id).first()
        if rank is None:
            return None
        return RanksSc(id=rank.id, rank_name=rank.rank_name, role_id=rank.role_id, required_points=rank.required_points)


def GetRanks(rank_ids: list[int]) -> list[RanksSc | None]:
    with get_session() as session:
        ranks = session.query(Ranks).filter(Ranks.id.in_(rank_ids)).all()
        return [RanksSc(rank.id, rank.rank_name, rank.role_id, rank.required_points) for rank in ranks]
