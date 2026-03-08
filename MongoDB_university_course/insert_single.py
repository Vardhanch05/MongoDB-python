import datetime
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI) # Connect to MongoDB using the connection string from the .env file

db = client.bank  # get reference to the 'bank' database
accounts_collection = db.accounts  # get reference to the 'accounts' collection

new_account = {
    "account_holder": "Vardhan Chilakamarri",
    "account_id": "MBD123456789",
    "account_type": "Checking",
    "balance": 5000.00,
    "last_update": datetime.datetime.now()
}

result = accounts_collection.insert_one(new_account)

document_id = result.inserted_id
print(f"_id of inserted document: {document_id}")


client.close() # Close the connection to MongoDB