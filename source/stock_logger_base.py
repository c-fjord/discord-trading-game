import sqlite3


class StockLoggerBase:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.c = self.conn.cursor()
        self.create_database()
        self.c.row_factory = self.dict_factory

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
                           'user_name varchar(100) PRIMARY KEY,'
                           'wallet FLOAT NOT NULL);')

        with self.conn:
            self.c.execute('CREATE TABLE IF NOT EXISTS portfolio ('
                           'user_id VARCHAR(100),'
                           'stock_id VARCHAR(50),'
                           'amount INT NOT NULL,'
                           'FOREIGN KEY(user_id) REFERENCES users(user_name))')

        with self.conn:
            self.c.execute('CREATE TABLE IF NOT EXISTS transactions ('
                           'transaction_id INTEGER PRIMARY KEY,'
                           'user_id VARCHAR(100),'
                           'stock_id VARCHAR(50),'
                           'action VARCHAR(100) NOT NULL,'
                           'price FLOAT NOT NULL,'
                           'amount INT NOT NULL,'
                           'date TIMESTAMP,'
                           'FOREIGN KEY(user_id) REFERENCES users(user_name))')

    def add_user(self, user):
        with self.conn:
            self.c.execute('INSERT INTO users(user_name, wallet)'
                           'VALUES(?,?)', (user, 500))

    def get_user(self, user):
        pass

    def get_wallet(self, user):
        with self.conn:
            self.c.execute('SELECT wallet FROM users WHERE user_name=?', (user,))
            wallet = self.c.fetchone()
        return wallet

    def set_wallet(self, user, amount):
        wallet = self.get_wallet(user)['wallet']
        current_value = wallet + amount
        with self.conn:
            self.c.execute('UPDATE users SET wallet=? WHERE user_name=?', (current_value, user))

    def get_stock(self, user, stock):
        pass

    def add_stock(self, user, stock, amount):
        with self.conn:
            self.c.execute('INSERT INTO portfolio(user_id, stock_id, amount)'
                           'VALUES(?,?,?)', (user, stock, amount))

    def get_amount(self, user, stock):
        with self.conn:
            self.c.execute('SELECT amount FROM portfolio WHERE user_id=? AND stock_id=?', (user, stock))
            amount = self.c.fetchone()
        return amount if amount is None else amount['amount']

    def set_amount(self, user, stock, amount):
        with self.conn:
            self.c.execute('UPDATE portfolio SET amount=? WHERE user_id=? AND stock_id=?', (amount, user, stock))

