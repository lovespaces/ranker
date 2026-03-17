from enum import Enum


class LogType(Enum):
    NEWUSER = "データベースに存在しないユーザーのため、新規作成しました。"
    CHANGED_MCID = "このユーザーのマインクラフトのIDが変更されました。"
