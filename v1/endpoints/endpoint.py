from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, Any
from pymongo import ASCENDING, DESCENDING
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

from core.schemas.item import Item
from core.models.database import Database

router = APIRouter()

@router.post("/items/", response_model=Item, status_code=201)
async def create_item(item: Item, db: AsyncIOMotorClient = Depends(Database.get_database)):
    result = await db.items.insert_one(item.dict())
    created_item = await db.items.find_one({"_id": result.inserted_id})
    return created_item

@router.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str, db: AsyncIOMotorClient = Depends(Database.get_database)):
    item = await db.items.find_one({"_id": ObjectId(item_id)})
    if item:
        return item
    raise HTTPException(status_code=404, detail="Item not found")

@router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item, db: AsyncIOMotorClient = Depends(Database.get_database)):
    result = await db.items.update_one({"_id": ObjectId(item_id)}, {"$set": item.dict()})
    if result.modified_count == 1:
        updated_item = await db.items.find_one({"_id": ObjectId(item_id)})
        return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/items/{item_id}")
async def delete_item(item_id: str, db: AsyncIOMotorClient = Depends(Database.get_database)):
    result = await db.items.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 1:
        return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

@router.get("/items/", response_model=dict)
async def read_items(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: AsyncIOMotorClient = Depends(Database.get_database)
) -> Dict[str, Any]:
    # Calculate skip count for pagination
    skip_count = (page - 1) * per_page
    
    # Fetch items from the database with pagination
    items = await db.items.find().skip(skip_count).limit(per_page).to_list(length=None)
    
    # Convert ObjectId to string for each item
    for item in items:
        item["_id"] = str(item["_id"])

    # Count total number of items
    total_items = await db.items.count_documents({})
    
    # Calculate total number of pages
    total_pages = (total_items + per_page - 1) // per_page
    
    # Construct response payload with items and pagination metadata
    response_data = {
        "items": items,
        "pagination": {
            "total_items": total_items,
            "total_pages": total_pages,
            "page": page,
        }
    }
    
    return response_data