import sqlite3


class StockLoggerBase:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.c = self.conn.cursor()
        self.create_database()
        # self.c.row_factory = self.dict_factory

    def __del__(self):
        self.c.close()

    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def create_database(self):
        with self.conn:
            self.c.execute('CREATE TABLE IF NOT EXISTS users ('
                           'user_id INTEGER PRIMARY KEY,'
                           'name varchar(100),'
                           'guild varchar(100),'
                           'wallet FLOAT NOT NULL);')

        with self.conn:
            self.c.execute('CREATE TABLE IF NOT EXISTS portfolio ('
                           'user_id VARCHAR(100),'
                           'stock VARCHAR(50),'
                           'amount INT,'
                           'FOREIGN KEY(user_id) REFERENCES users(name))')

        with self.conn:
            self.c.execute('CREATE TABLE IF NOT EXISTS portfolio_history ('
                           'user_id VARCHAR(100),'
                           'price FLOAT,'
                           'FOREIGN KEY(user_id) REFERENCES users(name))')

        with self.conn:
            self.c.execute('CREATE TABLE IF NOT EXISTS transactions ('
                           'transaction_id INTEGER PRIMARY KEY,'
                           'user_id VARCHAR(100),'
                           'stock VARCHAR(50),'
                           'action VARCHAR(10),'
                           'price FLOAT,'
                           'amount INT,'
                           'date TIMESTAMP,'
                           'FOREIGN KEY(user_id) REFERENCES users(name))')

    # Users
    def add_user(self, user, guild):
        with self.conn:
            self.c.execute('INSERT INTO users(name, guild, wallet)'
                           'VALUES(?,?,?)', (user, guild, 500))

    def get_user(self, user_id):
        with self.conn:
            self.c.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
            user = self.c.fetchone()
        return user

    def get_user_id(self, user, guild):
        with self.conn:
            self.c.execute('SELECT user_id FROM users WHERE name=? AND guild=?', (user, guild))
            user_id = self.c.fetchone()
        return user_id if user_id is None else user_id[0]

    def get_wallet(self, user_id):
        with self.conn:
            self.c.execute('SELECT wallet FROM users WHERE user_id=?', (user_id,))
            wallet = self.c.fetchone()
        return wallet if wallet is None else wallet[0]

    def set_wallet(self, user_id, amount):
        with self.conn:
            self.c.execute('UPDATE users SET wallet=? WHERE user_id=?', (amount, user_id))

    # Portfolio
    def add_portfolio(self, user_id, stock, amount):
        with self.conn:
            self.c.execute('INSERT INTO portfolio(user_id, stock, amount)'
                           'VALUES(?,?,?)', (user_id, stock, amount))

    def get_portfolio(self, user_id):
        with self.conn:
            self.c.execute('SELECT * FROM portfolio WHERE user_id=?', (user_id,))
            portfolio = self.c.fetchall()
        return portfolio

    def remove_portfolio(self, user_id, stock):
        with self.conn:
            self.c.execute('DELETE FROM portfolio WHERE user_id=? AND stock=?', (user_id, stock))

    def get_amount(self, user_id, stock):
        with self.conn:
            self.c.execute('SELECT amount FROM portfolio WHERE user_id=? AND stock=?', (user_id, stock))
            amount = self.c.fetchone()
        return amount if amount is None else amount[0]

    def set_amount(self, user_id, stock, amount):
        with self.conn:
            self.c.execute('UPDATE portfolio SET amount=? WHERE user_id=? AND stock=?', (amount, user_id, stock))

    # Portfolio history
    def add_portfolio_history(self, user_id, price):
        with self.conn:
            self.c.execute('INSERT INTO portfolio_history(user_id, price)'
                           'VALUES(?,?)', (user_id, price))

    def get_portfolio_history(self, user_id):
        with self.conn:
            self.c.execute('SELECT * FROM portfolio_history WHERE user_id=?', (user_id,))
            history = self.c.fetchall()
        return history

    # Transactions
    def add_transaction(self, user_id, stock, action, price, amount, date):
        with self.conn:
            self.c.execute('INSERT INTO transactions (user_id, stock, action, price, amount, date)'
                           'VALUES(?,?,?,?,?,?)', (user_id, stock, action, price, amount, date))

    def get_transactions(self, user_id, number):
        with self.conn:
            self.c.execute('SELECT * FROM transactions WHERE user_id=? ORDER BY date DESC', (user_id,))
            transactions = self.c.fetchall() if number is None else self.c.fetchmany(number)
        return transactions
