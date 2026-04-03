import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# The Connection String (The Address)
MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI)
for db_name in client.list_database_names():
    print(db_name)

client.close()

# Output:
'''
sample_mflix
admin
local
'''