from discord import ui


class ChangesRls(ui.TextDisplay):
    def __init__(
        self,
        *,
        id: int | None = None,
        old_role_id: int | None = None,
        new_role_id: int | None = None,
        is_changed: bool,
        is_new: bool = False,
        is_demote: bool = False,
    ) -> None:
        emoji = "📈"
        changed = "昇格"
        if is_demote:
            emoji = "📉"
            changed = "降格"
        if is_changed:
            if is_new:
                content = f"## 📍 ランク付与\n- <@&{new_role_id}> 付与"
            else:
                content = f"## {emoji} ランク{changed}\n- <@&{old_role_id}> 解除\n- <@&{new_role_id}> 付与"
        else:
            content = "__**ランク変化なし**__"

        super().__init__(content, id=id)
