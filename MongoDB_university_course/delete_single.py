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

doc_to_delete = {"_id": ObjectId("69a3de5643f00063084715d7")} # Replace with the actual _id value of the document you want to delete

print("Target Document before deleting:")
pprint.pprint(accounts_collection.find_one(doc_to_delete)) # Print the document before deleting to confirm it exists

res = accounts_collection.delete_one(doc_to_delete)

print("Searching for Target Document after deleting:")
pprint.pprint(accounts_collection.find_one(doc_to_delete)) # Print the document after deleting to confirm it has been deleted

print(f"Deleted {res.deleted_count} document.")
client.close() # Close the connection to MongoDB

# Output:
'''
Target Document before deleting:
{'_id': ObjectId('69a3de5643f00063084715d7'),
 'account_holder': 'Vardhan Chilakamarri',
 'account_id': 'MBD123456789',
 'account_type': 'Checking',
 'balance': 5000.0,
 'last_update': datetime.datetime(2026, 3, 1, 12, 6, 6, 182000)}
Searching for Target Document after deleting:
None
Deleted 1 document.
'''