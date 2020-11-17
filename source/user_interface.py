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
        stock_symbol = stock_symbol.upper()
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
        stock_symbol = stock_symbol.upper()
        current_amount = self.get_amount(user, stock_symbol)
        if (stock_price := self.get_live_price(stock_symbol)) > 0:
            if current_amount is not None:
                total_price = stock_price * amount
                if current_amount >= amount:
                    self.update_portfolio(user, stock_symbol, -amount)
                    self.set_wallet(user, total_price)
                    self.log_transaction(user, stock_symbol, 'sell', total_price, amount)
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
            portfolio = list(zip(*portfolio_list))
            print(portfolio)
            current_price = [self.get_live_price(stock) for stock in portfolio[1]]
            total_stock_price = [current_price[i] * portfolio[2][i] for i in range(len(current_price))]

            embed = discord.Embed(title=ctx.message.author.nick)

            embed.add_field(name='Amount', value='\n'.join([str(i) for i in portfolio[2]]), inline=True)
            embed.add_field(name='Stock', value='\n'.join(portfolio[1]), inline=True)
            embed.add_field(name='Current price', value='\n'.join(['{:.2f}'.format(i) for i in current_price]))
            embed.add_field(name='Total price', value='\n'.join(['{:.2f}'.format(i) for i in total_stock_price]))
            embed.set_footer(text='Total portfolio value: {:.2f}'.format(sum(total_stock_price)))

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

    @commands.command(name='transactions')
    async def transaction_history(self, ctx):
        user = str(ctx.message.author)
        trans = list(zip(*self.get_transaction(user)))

        if len(trans[0]) > 0:
            embed = discord.Embed(title=ctx.message.author.nick)
            embed.add_field(name='Nr.', value='\n'.join([str(i) for i in trans[0]]))
            embed.add_field(name='Stock', value='\n'.join(trans[2]), inline=True)
            embed.add_field(name='Amount', value='\n'.join([str(i) for i in trans[5]]), inline=True)
            embed.add_field(name='Action', value='\n'.join(trans[3]), inline=True)
            embed.add_field(name='Price', value='\n'.join([str(i) for i in trans[4]]))
            embed.add_field(name='Date', value='\n'.join(trans[6]))
            await ctx.send(embed=embed)
        else:
            await ctx.send('No transactions has been made')

    @commands.command()
    async def test(self, ctx):
        await ctx.send(ctx.message.author.guild)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(error)

    @commands.Cog.listener()
    async def on_ready(self):
        print('implement logger')
