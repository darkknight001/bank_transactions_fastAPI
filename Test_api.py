import requests
import json

"""
This script can be used for testing valid and invalid transfer using the transfer API
Invalid transactions: contains a list of sample transactions that will be rejected by API.
Valid transactions: contains a list of sample transactions that can be processed by API.
"""

TRANSFER_URL = 'http://127.0.0.1:8000/transfer'
TRANSACTIONS_URL = 'http://127.0.0.1:8000/all_transactions'

invalid_transactions = [
    {   
        # Source Invalid
        "From": "0000", 
        "To": "4227",
        "amount": 500.5
    },
    {   
        # Destination Invalid
        "From": "1473", 
        "To": "9999",
        "amount": 200.0
    },
    {   
        # Same accounts
        "From": "0053", 
        "To": "0053",
        "amount": 100
    },
    {   
        # Insufficent Balance
        "From": "4227", 
        "To": "0026",
        "amount": 5000.0
    },
    {   
        # amount Invalid
        "From": "0026", 
        "To": "4227",
        "amount": 0
    },
    {   
        # amount Invalid
        "From": "1473", 
        "To": "0053",
        "amount": -500.0
    }]

valid_transactions = [
    {   
        "From": "0026", 
        "To": "4227",
        "amount": 50
    },
    {   
        "From": "1473", 
        "To": "3529",
        "amount": 75.0
    },
    {   
        "From": "0053", 
        "To": "0026",
        "amount": 30
    },
    {   
        "From": "4227", 
        "To": "0026",
        "amount": 15.0
    },
    {   
        "From": "0026", 
        "To": "9529",
        "amount": 10.0
    },
    {   
        "From": "1473", 
        "To": "0053",
        "amount": 100.0
    }]

def test_invalid_transfer(invalid_transactions):
    # Check initial transactions
    transactions1 = json.loads(requests.request("GET", TRANSACTIONS_URL).text)
    print("Initial Transactions: ", len(transactions1))
    
    # check all invalid cases
    for transactions in invalid_transactions:
        response = requests.request("POST", TRANSFER_URL, data=json.dumps(transactions))
        print(response, response.text, "\n")

    # Check for transaction update
    transactions2 = json.loads(requests.request("GET", TRANSACTIONS_URL).text)    
    print("Final Transactions: ", len(transactions2))
    
    # print new transactions
    print("Transactions due to invalid transfer: ")
    for t in transactions2:
        if t not in transactions1:
            print(t)
    print(".")

def test_valid_transfer(valid_transactions):
    # Check initial transactions
    transactions1 = json.loads(requests.request("GET", TRANSACTIONS_URL).text)
    print("Initial Transactions: ", len(transactions1))
    
    # complete transactions
    for transaction in valid_transactions:
        response = requests.request("POST", TRANSFER_URL, data=json.dumps(transaction))
        print(response, response.text, "\n")

    # Check for transaction update
    transactions2 = json.loads(requests.request("GET", TRANSACTIONS_URL).text)
    print("Final Transactions: ", len(transactions2))

    # print new transactions
    print("Transactions due to valid transfer: ")
    for t in transactions2:
        if t not in transactions1:
            print(t)
    print(".")



if __name__ == '__main__':
    print("\n\nTesting Invalid transactions:")
    test_invalid_transfer(invalid_transactions)
    print("\n\nTesting valid transactions:")
    test_valid_transfer(valid_transactions)