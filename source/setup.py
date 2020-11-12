from discord.ext import commands
from source.user_interface import User_interface
from source.error import ErrorHandler

if __name__ == '__main__':

    with open(r'..\source\token.txt') as f:
        TOKEN = f.read()

    bot = commands.Bot('?')
    bot.add_cog(User_interface(bot))
    bot.add_cog(ErrorHandler(bot))
    bot.run(TOKEN)
