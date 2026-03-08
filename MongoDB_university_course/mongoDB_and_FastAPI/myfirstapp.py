from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import *
from fastapi import *

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

# READ operation
@app.get("/items/")
async def get_items():
    items = await collections.find().to_list(length = 10)
    return {"items": convert_doc_list(items)}

# UPDATE operation

@app.put("/items/{name}")
async def update_item(name:str, item: Item):
    updated_item = await collections.find_one_and_update(
        {"name": name},
        {"$set": item.model_dump()},
        return_document = ReturnDocument.AFTER,
    )
    if updated_item:
        return {"message": "Item updated", "item": convert_doc(updated_item)}
    raise HTTPException(status_code=404, detail=f"Item with name {name}not found")

# we have to perform the UPDATE only after entering the data in the database.
# if the update is successful, we can see the updated data in the Atlas Cluster as well
# error code 200 indicates the UPDATE is successful.

# DELETE operation
@app.delete("/items/{name}")
async def delete_item(name:str):
    result = await collections.delete_one({"name": name})
    if result.deleted_count == 1:
        return {"message": f"Item with name {name} deleted"}
    raise HTTPException(status_code=404, detail=f"Item with name {name} not found")
# we have to perform the DELETE only after entering the data in the database.
# if the delete is successful, we can see the deleted data in the Atlas Cluster as well
# if delete is successful, then error code 200 is shown, otherwise error code 404 is shown which indicates that the item with the given name is not found in the database.