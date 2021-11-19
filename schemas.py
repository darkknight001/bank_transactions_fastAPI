from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Balance(BaseModel):
    account_no : str
    balance : float 

class Transaction(BaseModel):
    source: str
    destination: str
    amount : float

"""
{
  "id": "transaction_id",
  "from":{
    "id": "account_no",
    "balance": "current_balance"
  },
  "to":{
    "id": "account_no",
    "balance": "current_balance"
  },
  "transfered": "transfer_amount"
  "created_datetime": "transaction created time"
}
"""

class Transaction_status(BaseModel):
    id : str
    source: Balance
    destination: Balance
    transfered: float
    created_datetime: datetime