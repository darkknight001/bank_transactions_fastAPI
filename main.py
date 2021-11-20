from fastapi import FastAPI, status, HTTPException
from database import Database
from datetime import datetime
import asyncio
import hashlib
import uuid
import schemas
import time

app = FastAPI()
db = Database()

# Implement HashSet for locking subsequent API calls
throttle_requests = set()

# Close database connection on exit
@app.on_event("shutdown")
def disconnect_db():
    db.conn.close()


# Account Creation API
@app.post('/create_account', status_code=201)
def create_account(request: schemas.Balance):
    try:
        db.create_account(request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account number already in database.")
    
    return db.get_balance(request.account_no)

# Debug API: Not to be used
@app.get('/accounts')
def get_accounts():
    account_details = db.cursor.execute("select * from balances").fetchall()
    return account_details
    
# Debug API: Not to be used
@app.get('/transactions')
def get_transactions(account):
    transactions = db.cursor.execute(f"select * from transactions WHERE account_no='{account}'").fetchall()
    if not transactions:
        raise HTTPException(status_code=404, detail=f"No transactions found!")
    return transactions

# Debug API: Not to be used
@app.get('/all_transactions')
def get_all_transactions():
    transactions = db.cursor.execute(f"select * from transactions").fetchall()
    # if not transactions:
    #     raise HTTPException(status_code=404, detail=f"No transactions found!")
    return transactions

# Debug API: Not to be used
@app.get('/get_balance')
def get_balance(account):
    account_details = db.get_balance(account)
    if not account_details:
        raise HTTPException(status_code=404, detail=f"Account {account} not in database.")
    return account_details



# Transaction API
@app.post('/transfer')
async def transfer(transaction:schemas.Transaction):

    # Check if accounts are present
    from_account = db.cursor.execute(f"SELECT * FROM balances WHERE account_no='{transaction.From}'").fetchone()
    if not from_account:
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail={
            "response":f"Source account({transaction.From}) not in database.",
            "status": "failed"})

    to_account = db.cursor.execute(f"SELECT * FROM balances WHERE account_no='{transaction.To}'").fetchone()
    if not to_account:
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail={
            "response":f"Destination account({transaction.To}) not in database.",
            "status": "failed"})
    
    # Check if "From" and "To" account are same:
    if transaction.From == transaction.To:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
            "response":"Source and destination account can't be same!",
            "status": "failed"})

    # Check if src account has sufficient balance
    if from_account["balance"]<transaction.amount:
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail={
            "response":f"Insufficient amount in source account({transaction.From}).",
            "status": "failed"})
    
    # Amount is zero on negative
    if transaction.amount<=0:
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail={
            "response":"Invalid amount, minimum amount to transfer should be greater than 0.",
            "status": "failed"})

    
    # add current transaction to Hash set(To throttle additional requests)
    throttle_transaction = hashlib.md5((transaction.From+transaction.To).encode()).hexdigest()
    
    # Check if throttling condition exists
    if throttle_transaction in throttle_requests:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail={
            "response":"Request was throttled, please wait for previous request to complete.",
            "status": "failed"})

    # lock the current request until it processes
    throttle_requests.add(throttle_transaction)

    # Generated random transaction ID and adding transaction to DB
    transaction_id = uuid.uuid4().hex[:8]
    curr_transaction = db.add_transaction(transaction_id, transaction.From, transaction.amount)

    # Delay to check affect of concurrent requests, uncomment to mimic processing time on large database
    # await asyncio.sleep(2)
    
    # Initiate Transaction
    new_src_bal = from_account["balance"]-transaction.amount
    new_dest_bal = to_account["balance"]+transaction.amount

    # update new balance on database
    from_account = db.update_balance(transaction.From, new_src_bal)
    to_account = db.update_balance(transaction.To, new_dest_bal)

    # revoke lock, so that other requests from same account can be processed
    throttle_requests.remove(throttle_transaction)

    response = dict()
    response["id"] = curr_transaction["id"]
    response["transfered"] = transaction.amount
    response["from"] = from_account
    response["to"] = to_account
    response["created_datetime"] = datetime.strptime(curr_transaction["created_datetime"], "%Y-%m-%d %H:%M:%S.%f")
    return response





    