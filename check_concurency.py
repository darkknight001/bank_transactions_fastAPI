from Test_api import TRANSFER_URL,TRANSACTIONS_URL
import requests
import json
import time
from threading import Thread
"""
    This code will check the affect of concurrent requests to the API.
    This will also test the API in case of multiple accidental clicks by user
    To check this, please uncomment asyncio.sleep line(transfer API) in main.py file(To simulate delay in query processing)
"""

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
    },

    {   
        "From": "4227", 
        "To": "0026",
        "amount": 25
    },
    {   
        "From": "3529", 
        "To": "1473",
        "amount": 37.50
    },
    {   
        "From": "0026", 
        "To": "0053",
        "amount": 15
    },
    {   
        "From": "0026", 
        "To": "4227",
        "amount": 7.50
    },
    {   
        "From": "9529", 
        "To": "0026",
        "amount": 5.0
    },
    {   
        "From": "0053", 
        "To": "1473",
        "amount": 50.0
    }]

def complete_transaction(transfer_req, print_response=False):
    
    response = requests.request("POST", TRANSFER_URL, data=json.dumps(transfer_req))
    if print_response:
        print(f"{response}|{response.text}\n") 
    return f"{response}|{response.text}\n"

def do_transactions(transactions, responses=None):
    if responses is None:
        responses = []
    for transfer_req in transactions:
        responses.append(complete_transaction(transfer_req))
    return responses

def do_concurrent_transactions(nthreads, transactions):
    resArray = []
    threads = []

    for i in range(nthreads):
        transaction_chunk = transactions[i::nthreads]
        t = Thread(target=do_transactions, args=(transaction_chunk, resArray))
        threads.append(t)
    
    # Start threads
    [t.start() for t in threads]

    # Join threads
    [t.join() for t in threads]

    return resArray

# checks for accidental API calls during short duration
def do_multiple_transfer(transfer_req):

    # checks if the user has accidently clicked on "send money/transfer" button twice
    print("\n\nChecking Accidental API requests scenario:")
    # Creating multiple threads to simulate multiple clicks
    t1 = Thread(target=complete_transaction, args=(transfer_req, True))
    t2 = Thread(target=complete_transaction, args=(transfer_req, True))
    t3 = Thread(target=complete_transaction, args=(transfer_req, True))
    t1.start()
    t2.start()
    t3.start()
    t3.join()
    t1.join()
    t2.join()


def check_concurrency(valid_transactions):
    print("Checking affect of concurrent requests to API\n\n")

    # sequential call
    print("Sequential Call")
    start_time1 = time.time()
    result1 = do_transactions(valid_transactions, [])
    # print(*result1)
    elapsed1 = (time.time()-start_time1)
    print(f"Time taken sequnetial requests: {elapsed1:.2f} seconds")

    # concurrent call
    print("Concurrent Call")
    start_time2 = time.time()
    result2 = do_concurrent_transactions(4, valid_transactions)
    # print(*result2)
    elapsed2 = (time.time()-start_time2)
    print(f"Time taken concurrent requests: {elapsed2:.2f} seconds")

if __name__ == '__main__':
    # Concurrency check
    check_concurrency(valid_transactions)
    
    # Check for multiple API requests by same user at a time
    do_multiple_transfer(valid_transactions[0])

