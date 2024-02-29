# v1/endpoints/endpoint.py

from fastapi import HTTPException, APIRouter
from core.schemas.item import Item
from core.models.database import Database

router = APIRouter()

@router.post("/items/", response_model=Item)  # Specify response_model as Item
async def create_item(item: Item):
    if Database.client is None:
        raise HTTPException(status_code=500, detail="MongoDB client is not connected.")
    
    # Connect to the database if not already connected
    if Database.client is None:
        await Database.connect_mongodb()

    result = await Database.get_database().items.insert_one(item.dict())
    # Return the created item with the inserted_id
    return {**item.dict(), "item_id": str(result.inserted_id)}

@router.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    if Database.client is None:
        raise HTTPException(status_code=500, detail="MongoDB client is not connected.")
    
    # Connect to the database if not already connected
    if Database.client is None:
        await Database.connect_mongodb()
    
    item = await Database.get_database().items.find_one({"_id": item_id})
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    if Database.client is None:
        raise HTTPException(status_code=500, detail="MongoDB client is not connected.")
    
    # Connect to the database if not already connected
    if Database.client is None:
        await Database.connect_mongodb()
    
    result = await Database.get_database().items.update_one({"_id": item_id}, {"$set": item.dict()})
    if result.modified_count == 1:
        return {**item.dict(), "item_id": item_id}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/items/{item_id}")
async def delete_item(item_id: str):
    if Database.client is None:
        raise HTTPException(status_code=500, detail="MongoDB client is not connected.")
    
    # Connect to the database if not already connected
    if Database.client is None:
        await Database.connect_mongodb()
    
    result = await Database.get_database().items.delete_one({"_id": item_id})
    if result.deleted_count == 1:
        return {"message": "Item deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@router.get("/items/", response_model=list[Item])
async def read_items():
    if Database.client is None:
        raise HTTPException(status_code=500, detail="MongoDB client is not connected.")
    
    # Connect to the database if not already connected
    if Database.client is None:
        await Database.connect_mongodb()
    
    items = []
    async for item in Database.get_database().items.find():
        items.append(item)
    return items
