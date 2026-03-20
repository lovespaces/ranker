def Calc(hits: int, kills: int, kill_first: bool, is_last: bool, was_king: bool, was_first: bool) -> int:
    points = 0
    points += kills * 5 + hits
    if kill_first:
        points += 15
    if is_last:
        points -= 5
    if was_first:
        points -= 3
    if was_king:
        points -= 15

    return points
