from utils.db.connection import get_session
from utils.db.models import Ranks
from utils.db.schemas import RanksSc


def GetRank(rank_id: int) -> RanksSc | None:
    with get_session() as session:
        rank = session.query(Ranks).filter_by(id=rank_id).first()
        if rank is None:
            return None
        return RanksSc(id=rank.id, rank_name=rank.rank_name, role_id=rank.role_id, required_points=rank.required_points)
