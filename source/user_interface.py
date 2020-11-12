import discord
from discord.ext import commands
from source.stock_logger import SqlLogger
import yahoo_fin.stock_info as yf


class User_interface(commands.Cog, SqlLogger):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @staticmethod
    def get_live_price(stock_symbol):
        try:
            stock_price = yf.get_live_price(stock_symbol.upper())
        except AssertionError:
            return 0
        return stock_price

    @commands.command()
    async def buy(self, ctx, stock_symbol, amount: int):
        user = str(ctx.message.author)
        wallet = self.get_user_wallet(user)

        if (stock_price := self.get_live_price(stock_symbol)) > 0:
            total_price = amount * stock_price
            if total_price <= wallet:
                self.set_wallet(user, -total_price)
                self.update_portfolio(user, stock_symbol, amount)
                self.log_transaction(user, stock_symbol, 'buy', stock_price, amount)
                await ctx.send('{} {} stock(s) has been purchased for {:.2f}'.format(amount, stock_symbol, total_price))
            else:
                await ctx.send('Insufficient funds')
        else:
            await ctx.send('Invalid stock symbol')

    @commands.command()
    async def sell(self, ctx, stock_symbol, amount: int):
        user = str(ctx.message.author)
        current_amount = self.get_amount(user, stock_symbol)
        if (stock_price := self.get_live_price(stock_symbol)) > 0:
            if current_amount is not None:
                total_price = stock_price * amount
                if current_amount < amount:
                    self.update_portfolio(user, stock_symbol, -amount)
                    self.set_wallet(user, total_price)
                else:
                    await ctx.send('Only {} {} stock available in your portfolio'.format(current_amount, stock_symbol))
                    return 0
                await ctx.send('{} {} stock has been sold for {:.2f}'.format(current_amount, stock_symbol, total_price))
            else:
                await ctx.send('No {} stock(s) available in your portfolio'.format(stock_symbol))
        else:
            await ctx.send('Invalid stock symbol')

    @commands.command(name='wallet')
    async def view_wallet(self, ctx):
        user = str(ctx.message.author)
        wallet = self.get_user_wallet(user)
        await ctx.send('{:.2f}'.format(wallet))

    @commands.command(name='portfolio')
    async def view_portfolio(self, ctx):
        user = str(ctx.message.author)
        portfolio_list = self.get_user_portfolio(user)
        if len(portfolio_list) > 0:
            stock, amount = '', ''
            for d in portfolio_list:
                stock += d['stock_id'] + '\n'
                amount += str(d['amount']) + '\n'

            embed = discord.Embed(title=user.split('#')[0], description="*")
            embed.add_field(name='Stock', value=stock, inline=True)
            embed.add_field(name='Amount', value=amount, inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send('You have no stock in your portfolio')

    # @commands.command()
    def top_value_portfolio(self):
        # Get top 10 portfolios
        pass

    # @commands.command()
    def top_movers_portfolio(self):
        pass

    # @commands.command()
    def top_movers(self):
        pass

    @commands.command()
    async def transaction_history(self, ctx):
        user = str(ctx.message.author)
        transactions = self.get_transaction(user)
        trans = list(zip(*map(lambda x: list(x.values()), transactions)))

        embed = discord.Embed(title=user.split('#')[0], description='*')
        embed.add_field(name='Stock', value='\n'.join(trans[2]), inline=True)
        embed.add_field(name='Amount', value='\n'.join(trans[3]), inline=True)
        embed.add_field(name='Action', value='', inline=True)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(error)

    @commands.Cog.listener()
    async def on_ready(self):
        print('implement logger')
