import sqlite3
from sqlite3.dbapi2 import Cursor
from datetime import datetime
import uuid

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('accounts.db', check_same_thread=False)

        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        self.conn.row_factory=dict_factory
        self.cursor = self.conn.cursor()
 
        # Create balances DB
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS balances (
                    account_no TEXT PRIMARY KEY NOT NULL,
                    balance REAL DEFAULT 100.0 NOT NULL
                    )""")
        self.conn.commit()

        # # Creates transactions DB
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS transactions (
                    id TEXT PRIMARY KEY,
                    account_no TEXT NOT NULL,
                    amount REAL,
                    created_datetime TEXT NOT NULL
                    )""")
        self.conn.commit()


    def create_account(self, user):
        self.cursor.execute(f"INSERT INTO balances VALUES ('{user.account_no}', {user.balance})")
        self.conn.commit()

    def get_balance(self, account_no):
        self.cursor.execute(f"SELECT * FROM balances WHERE account_no='{account_no}'")
        return self.cursor.fetchone()
    
    def update_balance(self, account, new_balance):
        self.cursor.execute(f"UPDATE balances SET balance={new_balance} WHERE account_no='{account}'")
        self.conn.commit()
        return self.get_balance(account)

    def add_transaction(self, account, amount):
        currentTime = datetime.now()
        id = uuid.uuid4().hex
        self.cursor.execute(f"INSERT INTO transactions VALUES ('{id}','{account}', {amount}, '{str(currentTime)}')")
        self.conn.commit()
        return self.get_transaction(id)

    def get_transaction(self, transaction_id):
        self.cursor.execute(f"SELECT * FROM transactions WHERE id='{transaction_id}'")
        return self.cursor.fetchone()