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

document_id_to_update = ObjectId("69a6ac0d85e8531292377d97") # Replace with the actual _id of the document you want to update
add_to_balance = {"$inc": {"balance": 1000}} # This will add 1000 to the existing balance

pprint.pprint(accounts_collection.find_one({"_id": document_id_to_update})) # Print the document before the update

result = accounts_collection.update_one({"_id": document_id_to_update}, add_to_balance)

client.close() # Close the connection to MongoDB

# execute UPDATE after performing INSERT operation to see the update reflected in the document
#Output:
'''
{'_id': ObjectId('69a6ac0d85e8531292377d97'),
 'account_holder': 'Vardhan Chilakamarri',
 'account_id': 'MBD123456789',
 'account_type': 'Checking',
 'balance': 6000.0, 
 'last_update': datetime.datetime(2026, 3, 3, 15, 8, 21, 759000)}
'''
# Balance got incremented by a 1000. So 5000 + 1000 = 6000.