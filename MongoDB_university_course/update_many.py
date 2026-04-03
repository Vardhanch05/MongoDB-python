import pprint
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from bson.objectid import ObjectId

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

try:
    client = MongoClient(MONGODB_URI)
    client.admin.command('ping')

    db = client.bank  # get reference to the 'bank' database
    accounts_collection = db.accounts  # get reference to the 'accounts' collection

    selected_accounts = {"account_type": "Savings"}
    set_field = {"$set": {"minimum_balance": 1000}} # This will set the minimum_balance field to 1000 for all documents that match the selected_Accounts filter

    result = accounts_collection.update_many(selected_accounts, set_field)
    print(f"Documents matched: {result.matched_count}")
    print(f"Documents modified: {result.modified_count}")

    pprint.pprint(accounts_collection.find_one(selected_accounts)) # Print one of the documents that were updated to see the changes

except ConnectionFailure as e:
    print(f"Failed to connect to MongoDB: {e}")
except OperationFailure as e:
    print(f"Update operation failed: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client.close()
