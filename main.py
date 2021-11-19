from fastapi import FastAPI, Depends, status, Response, HTTPException
from database import Database
from datetime import datetime
import schemas
app = FastAPI()
db = Database()


# Creation APIs
@app.post('/create_account', status_code=201)
async def create_account(request: schemas.Balance):
    new_account = db.create_account(request)
    
    return await db.get_balance(request.account_no)

# # Debug APIs : Not to be used
# @app.get('/accounts')
# def get_accounts(db: Session=Depends(get_db)):
#     account_details = db.query(models.Balance).all()
#     return account_details

@app.get('/get_balance')
def get_balance(account):
    account_details = db.get_balance(account)
    if not account_details:
        raise HTTPException(status_code=404, detail=f"Account {account} not in database.")
    return account_details



# Transaction API
@app.post('/transfer')
async def transfer(transaction:schemas.Transaction):
    
    # Check if src account present
    from_account = db.cursor.execute(f"SELECT * FROM balances WHERE account_no='{transaction.source}'").fetchone()
    if not from_account:
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail=f"Source account({transaction.source}) not in database.")
    to_account = db.cursor.execute(f"SELECT * FROM balances WHERE account_no='{transaction.destination}'").fetchone()
    if not to_account:
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail=f"Destination account({transaction.destination}) not in database.")

    # Check if src account has sufficient balance
    if from_account["balance"]<transaction.amount:
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail=f"Insufficient amount in source account({transaction.destination}).")

    # Initiate Transaction
    new_src_bal = from_account["balance"]-transaction.amount
    new_dest_bal = to_account["balance"]+transaction.amount
    from_account = await db.update_balance(transaction.source, new_src_bal)
    to_account = await db.update_balance(transaction.destination, new_dest_bal)

    # Add Transaction to DB
    curr_transaction = db.add_transaction(transaction.source, transaction.amount)

    response = dict()
    response["id"] = curr_transaction["id"]
    response["transfered"] = transaction.amount
    response["source"] = from_account
    response["destination"] = to_account
    response["created_datetime"] = datetime.strptime(curr_transaction["created_datetime"], "%Y-%m-%d %H:%M:%S.%f")
    return response





    