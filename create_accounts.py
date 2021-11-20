import requests
import json


"""
This script can be used to generate sample data to test the API.
"""

TEST_URL = 'http://127.0.0.1:8000/create_account'


accounts = [
    {
        "account_no": "0053",
        "balance": 500
    },
    {
        "account_no": "0026",
        "balance": 5000
    },
    {
        "account_no": "4227",
        "balance": 100
    },
    {
        "account_no": "3529",
        "balance": 1000
    },
    {
        "account_no": "9529",
        "balance": 800
    },
    {
        "account_no": "1473",
        "balance": 1200
    }]

def create_account(accounts):
    for account in accounts:
        print(account)
        response = requests.request("POST", TEST_URL, data=json.dumps(account))
        print(response, response.text, "\n")

if __name__ == '__main__':
    create_account(accounts)