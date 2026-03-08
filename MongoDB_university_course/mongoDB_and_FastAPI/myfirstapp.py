from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from serializer import convert_doc, convert_doc_list

from pydantic import BaseModel

mongo_uri = "mongodb+srv://vardhanchilakamarri4567_db_user:Xc5EWD1hacvSY1yF@cluster0.mbxignd.mongodb.net/?appName=Cluster0"

client = AsyncIOMotorClient(mongo_uri)
app = FastAPI()

@app.get("/")
async def root():
    collections = await client.list_database_names()
    return {"message": "Connected to MongoDB Atlas!!",
             "collections": collections}
database = client.get_database("mydatabase")
collections = database.get_collection("items")

class Item(BaseModel):
    name: str
    age: int

# CREATE operation
@app.post("/items/")
async def create_item(item: Item):
    await collections.insert_one(item.model_dump())
    return {"message": "Item created", "item": item}

# go into the local host running on http://127.0.0.1:8000"
'''
to enter into the swagger UI, go to http://127.0.0.1.8000/docs
to enter into the redoc UI, go to http://
there we can perform create_item get_items, get_item, update_item, delete_item. Basically CRUD operations
'''
# we can also view the data in the Atlas Cluster.
# Steps
# 1. Go to the Atlas Cluster and click on the " Data Explorer" tab.
# You can see the created clusters in it. Click on the cluster you want to view. 