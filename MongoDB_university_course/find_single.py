import datetime
import os
import pprint
from dotenv import load_dotenv
from pymongo import MongoClient

from bson.objectid import ObjectId

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI) # Connect to MongoDB using the connection string from the .env file

db = client.bank  # get reference to the 'bank' database
accounts_collection = db.accounts  # get reference to the 'accounts' collection

doc_to_find = {"_id": ObjectId("69a3de5643f00063084715d7")} # Replace with the actual _id value of the document you want to find

res = accounts_collection.find_one(doc_to_find)
print("Document found:")
pprint.pprint(res)

client.close() # Close the connection to MongoDB