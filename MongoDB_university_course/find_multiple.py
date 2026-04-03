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

docs_to_find = {"balance" : {"$gt": 5000}} # Find documents where the balance is greater than 5000

res = accounts_collection.find(docs_to_find)
num_docs = 0
print("Documents found:")
for doc in res:
    pprint.pprint(doc)
    num_docs += 1
print(f"Total number of documents found: {num_docs}")

client.close() # Close the connection to MongoDB