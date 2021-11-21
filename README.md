# Transactions at the bank

## Context 

This is a sample transaction API implementation using Python(3.6+) with Fastapi framework.

## Structure
Here, I've used SQLITE as relational DB

DB structure used:

```
TABLE transactions
  - id (unique)
  - amount
  - account_no
  - created_datetime
```

```
TABLE balances
  - account_no (unique)
  - balance
```
## How to use this repository
- Clone the repository from github.
- move to repository folder
- Create a virtualenv and install required packages
  ```bash
  $ python3 -m venv virtualenv
  $ source virtualenv/bin/activate
  $ pip3 install -r requirements.txt
  ```
- start uvicorn server:
  ```bash
  $ uvicorn main:app
  ```

## APIs 

1. ### Create Account
   ```
   Method: POST
   Path: "/create_account"
   Desciption: Adds new entry to balances table
   ```


   - Request Payload:
   ```python
   {
     "account_no": "account_no",   #string
     "balance": "money"            #float
   }
   ```


   - Response Data:
   ```python
   {
     "account_no": "account_no",   #string
     "balance": "money"            #float
   }
   ```


2. ### Get Accounts
    ```
    Method: GET
    Path: "/accounts"
    Desciption: returns details of accounts present in database(for debug purpose)
    ```
    - Request Payload:
    ```python
    None
    ```
    - Response Data:
    ```python
    [
      {
        "account_no": "account_no1",   #string
        "balance": "money1"            #float
      },
      {
        "account_no": "account_no2",  
        "balance": "money2"           
      }
    ]
    ```


3. ### Get Balance
    ```
    Method: GET
    Path: "/get_balance?account=account_no"
    Desciption: returns details of given account(for debug purpose)
    Query Parameter: account
    ```
    - Request Payload:
    ```python
    None
    ```
    - Response Data:
    ```python
    {
      "account_no": "account_no",   #string
      "balance": "money"            #float
    }
    ```


4. ### Get Transactions
    ```
    Method: GET
    Path: "/transactions?account=account_no"
    Desciption: returns all transactions for given account(for debug purpose)
    Query Parameter: account
    ```
    - Request Payload:
    ```python
    None
    ```
    - Response Data:
    ```python
    [
      {
        "id": "transaction_id1",
        "account_no": "account_no",
        "amount": "money",
        "created_datetime": "datetime.datetime"
      },
      {
        "id": "transaction_id2",
        "account_no": "account_no",
        "amount": "money",
        "created_datetime": "datetime.datetime"    
      },
    ]
    ```


5. ### Get All Transactions
    ```
    Method: GET
    Path: "/all_transactions"
    Desciption: returns all transactions from database(for debug purpose)
    ```
    - Request Payload:
    ```python
    None
    ```
    - Response Data:
    ```python
    [
      {
        "id": "transaction_id1",
        "account_no": "account_no",
        "amount": "money",
        "created_datetime": "datetime.datetime"
      },
      {
        "id": "transaction_id2",
        "account_no": "account_no",
        "amount": "money",
        "created_datetime": "datetime.datetime"    
      },
    ]
    ```
    
    
6. ### Transfer :star:
    ```
    Method: POST
    Path: "/transfer"
    Desciption: transfer a given amount from one account to another.
    ```
    - Request Payload:
    ```python
    {
      "from": "account_no",   #string
      "to": "account_no",     #string 
      "amount": "money"       #float
    }
    ```
    - Response Data:
    ```python
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
    ``` 
    
    
## Testing the API 
1. ### Option 1: Using Swagger UI
    - As the API is built using Fastapi, we can use Swagger UI to test the above APIs
    - Start the uvicorn server
    - Open (http://127.0.0.1:8000/docs) in your browser.
    - Explore all the APIs

2. ### Option 2: Using automated python script
    - Automated Python scripts are present in this repository to test the APIs with sample data.
    ```
    create_accounts.py        --> To populate database with sample accounts
    test_api.py               --> To test the API for valid and invalid request payloads
    check_concurrency.py      --> To check efficiency of API for concurrent API calls
    ```


## Scope of Improvements
- Using Redis caching
- Adding more workers to achieve high scalablity
- Adding asynchronous database driver(Async ORM/ encode's Database library)
