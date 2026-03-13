import os
import pprint

from dotenv import load_dotenv
from pymongo import MongoClient
load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGO_URI)

db = client.bank
accounts_collection = db.accounts
# to calculate the balance in GBP, divide the original balance by the conversion rate
conversion_rate_usd_to_gbp = 1.3 # GBP means British Pound Sterling

# select checking accounts with balances of more than $1500.
select_accounts = {"$match": {"account_type": "checking", "balance": {"$gt": 1500}}}

# Organize documents in order from highest balance to lowest (Default is ascending order, so we specify -1 for descending order).
organize_by_original_balane = {"$sort": {"balance": -1}}

# Return the account type, original balance, and balance in GBP for each document. Exclude the _id field from the results.
return_specified_fields = {
    "$project":{
        "account_type": 1,
        "balance": 1,
        "gbp_balance":{"$divide": ["$balance", conversion_rate_usd_to_gbp]}, # calculate the balance in GBP by dividing the original balance by the conversion rate
        "_id": 0,
    }
}


# Create an Aggregation Pipeline.
pipeline = [
    select_accounts,
    organize_by_original_balane,
    return_specified_fields,
]

results = accounts_collection.aggregate(pipeline)

print(
    "Account type, original balance, and balance in GBP for checking accounts with balances of more than $1500:",
    "in order from highest balance to lowest:", "\n"
)

for item in results:
    pprint.pprint(item)

client.close()

'''
1. The Syntax StructureThe $divide operator always takes an array containing exactly two expressions:
${ "$divide": [ {dividend}, {divisor} ] }
$Dividend: The number to be divided (in your case, the field "$balance").
Divisor: The number to divide by (in your case, the variable conversion_rate_usd_to_gbp).
'''

# Output:
# Account type, original balance, and balance in GBP for checking accounts with balances of more than $1500: in order from highest balance to lowest:
# {'account_type': 'checking', 'balance': 2000, 'gbp_balance': 1538.4615384615384}
# {'account_type': 'checking', 'balance': 1800, 'gbp_balance': 1384.6153846153845}
