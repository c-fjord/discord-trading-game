from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        await ctx.send('error')
