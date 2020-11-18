import sqlite3
from datetime import datetime
from source.stock_logger_base import StockLoggerBase


class SqlLogger(StockLoggerBase):
    def __init__(self):
        super().__init__()

    # Users
    def user_id(self, user, guild):
        user_id = self.get_user_id(user, guild)
        if user_id is None:
            self.add_user(user, guild)
            self.user_id(user, guild)
        return user_id

    def get_user_wallet(self, user, guild):
        user_id = self.user_id(user, guild)
        return self.get_wallet(user_id)

    def set_user_wallet(self, user, guild, amount):
        user_id = self.user_id(user, guild)
        current_amount = self.get_wallet(user_id)
        self.set_wallet(user_id, current_amount + amount)

    # Portfolio
    def update_portfolio(self, user, guild, stock, amount):
        user_id = self.user_id(user, guild)
        current_amount = self.get_amount(user_id, stock)

        if current_amount is None:
            self.add_portfolio(user_id, stock, amount)
        elif current_amount == 0:
            self.remove_portfolio(user_id, stock)
        else:
            self.set_amount(user_id, stock, current_amount + amount)

    # Transactions
    def log_transaction(self, user, guild, stock, action, price, amount):
        user_id = self.user_id(user, guild)
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.add_transaction(user_id, stock, action, price, amount, date)

    def get_user_transactions(self, user, guild, number=None):
        user_id = self.user_id(user, guild)
        self.get_transactions(user_id, number)

    # portfolio history
    # def log_portfolio_history(self):
        # Get all user_ids from users
        # Get all portfolios for each user
        # Calc total portfolio value
        # Insert portfolio value into portfolio_history under user_id
