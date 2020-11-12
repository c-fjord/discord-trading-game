from discord.ext import commands
from source.user_interface import User_interface
from source.error import ErrorHandler

TOKEN = "NzYzNDU0MDYyMTM2OTE4MDM3.X338AA.6cUqicxu72sbWw0xrIYMtM1ajyI"

if __name__ == '__main__':
    bot = commands.Bot('?')
    bot.add_cog(User_interface(bot))
    bot.add_cog(ErrorHandler(bot))
    bot.run(TOKEN)
