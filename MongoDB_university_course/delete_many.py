# Get reference to 'bank' database
import pprint
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI) # Connect to MongoDB using the connection string from the .env file

db = client.bank

# Get a reference to the 'accounts' collection
accounts_collection = db.accounts

# Filter for accounts with balance less than $2000
documents_to_delete = {"balance": {"$lt": 2000}}

# Search for sample document before delete
print("Searching for sample target document before delete: ")
pprint.pprint(accounts_collection.find_one(documents_to_delete))

# Write an expression that deletes the target accounts.
result = accounts_collection.delete_many(documents_to_delete)

# Search for sample document after delete
print("Searching for sample target document after delete: ")
pprint.pprint(accounts_collection.find_one(documents_to_delete))

print("Documents deleted: " + str(result.deleted_count))

client.close()

# Output:
'''
Searching for sample target document before delete: 
None
Searching for sample target document after delete: 
None
Documents deleted: 0
'''

# Output is 0 because there are no documents with balance less than 2000 in the collection.
# You can modify the filter to target different documents for deletion.