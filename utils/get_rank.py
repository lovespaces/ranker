from utils.db.connection import get_session
from utils.db.models import Ranks
from utils.db.schemas import RanksSc
from sqlalchemy import select


def GetRank(rank_id: int) -> RanksSc | None:
    with get_session() as session:
        query = select(Ranks).where(Ranks.id == rank_id)
        rank = session.execute(query).scalar()
        if rank is None:
            return None
        return RanksSc(id=rank.id, rank_name=rank.rank_name, role_id=rank.role_id, required_points=rank.required_points)


def GetRanks(rank_ids: list[int]) -> list[RanksSc]:
    with get_session() as session:
        query = select(Ranks).where(Ranks.id.in_(rank_ids))
        ranks = session.execute(query).scalars().all()
        rank_map = {rank.id: rank for rank in ranks}
        return [
            RanksSc(rank.id, rank.rank_name, rank.role_id, rank.required_points)
            for id in rank_ids
            if (rank := rank_map.get(id))
        ]
