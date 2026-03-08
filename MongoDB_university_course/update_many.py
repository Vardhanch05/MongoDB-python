import pprint
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI) # Connect to MongoDB using the connection string from the .env file

db = client.bank  # get reference to the 'bank' database
accounts_collection = db.accounts  # get reference to the 'accounts' collection

selected_accounts = {"account_type": "Savings"}
set_field = {"$set": {"minimum_balance": 1000}} # This will set the minimum_balance field to 1000 for all documents that match the selected_Accounts filter

result = accounts_collection.update_many(selected_accounts, set_field)
print("Documents matched:" + str( result.matched_count))
print("Documents modified:" + str( result.modified_count))

pprint.pprint(accounts_collection.find_one(selected_accounts)) # Print one of the documents that were updated to see the changes
client.close() # Close the connection to MongoDB
