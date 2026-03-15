from discord import ui


class ChangesRls(ui.TextDisplay):
    def __init__(
        self, *, id: int | None = None, old_role_id: int | None = None, new_role_id: int | None = None, is_changed: bool
    ) -> None:
        if is_changed:
            content = f"## ランク変化\n- <@&{old_role_id}> 解除\n- <@&{new_role_id}> 付与"
        else:
            content = "__**ランク変化無し**__"

        super().__init__(content, id=id)
