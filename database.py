import sqlite3
from datetime import datetime

class Database:
    def __init__(self):

        # connect to Database
        self.conn = sqlite3.connect('accounts.db', check_same_thread=False)

        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        # This will convert the query return type to dictionary
        self.conn.row_factory=dict_factory
        self.cursor = self.conn.cursor()
 
        # Create balances DB
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS balances (
                    account_no TEXT PRIMARY KEY NOT NULL,
                    balance REAL DEFAULT 100.0 NOT NULL
                    )""")
        self.conn.commit()

        # Creates transactions DB
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS transactions (
                    id TEXT PRIMARY KEY,
                    account_no TEXT NOT NULL,
                    amount REAL,
                    created_datetime TEXT NOT NULL
                    )""")
        self.conn.commit()

    # Add new account to balance table
    def create_account(self, user):
        self.cursor.execute(f"INSERT INTO balances VALUES ('{user.account_no}', {user.balance})")
        self.conn.commit()

    # Returns account balance with account no.
    def get_balance(self, account_no):
        self.cursor.execute(f"SELECT * FROM balances WHERE account_no='{account_no}'")
        return self.cursor.fetchone()
    
    # Updates the balance for given account no.
    def update_balance(self, account, new_balance):
        self.cursor.execute(f"UPDATE balances SET balance={new_balance} WHERE account_no='{account}'")
        self.conn.commit()
        return self.get_balance(account)

    # adds new transaction to Database
    def add_transaction(self, transaction_id, account, amount):
        currentTime = datetime.now()
        self.cursor.execute(f"INSERT INTO transactions VALUES ('{transaction_id}','{account}', {amount}, '{str(currentTime)}')")
        self.conn.commit()
        return self.__get_transaction(transaction_id)

    # return transaction details for given transaction ID
    def __get_transaction(self, transaction_id):
        self.cursor.execute(f"SELECT * FROM transactions WHERE id='{transaction_id}'")
        return self.cursor.fetchone()