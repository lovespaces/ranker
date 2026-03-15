def Calc(hits: int, kills: int, kill_first: bool, is_last: bool, was_first: bool):
    points = 0
    points += hits + kills
    if kill_first:
        points += 15
    if is_last:
        points -= 5
    if was_first:
        points -= 3

    return points
