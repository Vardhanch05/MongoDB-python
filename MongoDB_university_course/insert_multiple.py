import datetime
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI) # Connect to MongoDB using the connection string from the .env file

db = client.bank  # get reference to the 'bank' database
accounts_collection = db.accounts  # get reference to the 'accounts' collection

new_accounts = [
    {
    "account_holder": "Vardhan Chilakamarri",
    "account_id": "MBD123456789",
    "account_type": "Checking",
    "balance": 5000.00,
    "last_update": datetime.datetime.now()
    },
    {
    "account_holder": "John Doe",
    "account_id": "MBD987654321",
    "account_type": "Savings",
    "balance": 10000.00,
    "last_update": datetime.datetime.now()
    }
    ]

result = accounts_collection.insert_many(new_accounts)

document_id = result.inserted_ids # inserted_ids is a list of the _id values of the inserted documents, in the same order as the input documents
print(f"_id of inserted document: {document_id}")

print(result.acknowledged) # returns True if the insert was acknowledged by the server, False otherwise

client.close()

# Output:
'''
_id of inserted document: [ObjectId('69a6ac0d85e8531292377d97'), ObjectId('69a6ac0d85e8531292377d98')]
True
'''