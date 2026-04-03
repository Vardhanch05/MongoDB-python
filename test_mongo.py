import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI)
db = client["mydatabase"]
collection = db["users"]

# 1. Update: Change Vardhan's age to 22
# Syntax: update_one({filter}, {"$set": {new_data}})
collection.update_one(
    {"name": "Vardhan"}, 
    {"$set": {"age": 22}}
)
print("Updated Vardhan's age.")

# 2. Delete: Remove a specific document
collection.delete_one({"name": "Vardhan"})
print("Deleted Vardhan from the collection.")

# 3. Count: See how many documents are left
count = collection.count_documents({})
print(f"Documents remaining: {count}")

client.close()