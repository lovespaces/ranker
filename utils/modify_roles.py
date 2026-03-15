import discord


async def ModifyRoles(
    old_role: discord.Role, new_role: discord.Role, guild: discord.Guild, user: discord.Member
) -> None:
    await user.remove_roles(old_role)
    await user.add_roles(new_role)
