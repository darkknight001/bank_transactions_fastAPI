from pydantic import BaseModel
from typing import Optional
from datetime import datetime

"""
Describe request Payload schema for APIs
"""

class Balance(BaseModel):
    account_no : str
    balance : float 

class Transaction(BaseModel):
    From: str
    To: str
    amount : float

