from dataclasses import dataclass


@dataclass
class UsersSc:
    id: int
    points: int
    rank_id: int
    game_username: str | None
    is_bedrock: bool


@dataclass
class RanksSc:
    id: int
    rank_name: str
    role_id: int
    required_points: int
