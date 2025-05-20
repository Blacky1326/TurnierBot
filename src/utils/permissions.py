def is_admin(ctx):
    return ctx.author.guild_permissions.administrator

def check_admin_permissions():
    async def predicate(ctx):
        if not is_admin(ctx):
            await ctx.send("You do not have permission to use this command.")
            return False
        return True
    return commands.check(predicate)