import sqlite3
from datetime import datetime
from source.stock_logger_base import StockLoggerBase


class SqlLogger(StockLoggerBase):
    def __init__(self):
        super().__init__()

    def get_user_wallet(self, user):
        wallet = self.get_wallet(user)
        if wallet is None:
            self.add_user(user)
            wallet = self.get_wallet(user)
        return wallet

    def update_portfolio(self, user, stock, amount):
        current_amount = self.get_amount(user, stock)
        if current_amount is None:
            self.add_stock(user, stock, amount)
        elif current_amount == amount:
            self.remove_portfolio(user, stock)
        else:
            self.set_amount(user, stock, current_amount + amount)

    def remove_portfolio(self, user, stock):
        with self.conn:
            self.c.execute('DELETE FROM portfolio WHERE user_id=? AND stock_id=?', (user, stock))

    def check_portfolio(self, user, stock):
        with self.conn:
            self.c.execute('SELECT * from portfolio WHERE user_id=? and stock_id=?', (user, stock))
            row = self.c.fetchone()
        return row

    def get_user_portfolio(self, user):
        with self.conn:
            self.c.execute('SELECT * FROM portfolio WHERE user_id=?', (user,))
            rows = self.c.fetchall()
        return rows

    def log_transaction(self, user, stock, action, price, amount):
        with self.conn:
            self.c.execute('INSERT INTO transactions(user_id, stock_id, action, price, amount, date)'
                           'VALUES(?, ?, ?, ?, ?, ?)',
                           (user, stock, action, price, amount, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    def get_transaction(self, user):
        with self.conn:
            self.c.execute('SELECT * FROM transactions WHERE user_id=?', (user,))
            rows = self.c.fetchall()
        return rows


if __name__ == '__main__':
    db = SqlLogger()
    print(db.get_wallet('Fjord'))
    # db.set_user('Fjord#100')
