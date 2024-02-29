from fastapi import HTTPException, APIRouter, Depends,Query
from motor.motor_asyncio import AsyncIOMotorClient
from core.schemas.item import Item
from core.models.database import Database

router = APIRouter()

@router.post("/items/", response_model=Item)
async def create_item(item: Item, db: AsyncIOMotorClient = Depends(Database.get_database)):
    result = await db.items.insert_one(item.dict())
    return {**item.dict(), "item_id": str(result.inserted_id)}

@router.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str, db: AsyncIOMotorClient = Depends(Database.get_database)):
    item = await db.items.find_one({"_id": item_id})
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item, db: AsyncIOMotorClient = Depends(Database.get_database)):
    result = await db.items.update_one({"_id": item_id}, {"$set": item.dict()})
    if result.modified_count == 1:
        return {**item.dict(), "item_id": item_id}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/items/{item_id}")
async def delete_item(item_id: str, db: AsyncIOMotorClient = Depends(Database.get_database)):
    result = await db.items.delete_one({"_id": item_id})
    if result.deleted_count == 1:
        return {"message": "Item deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@router.get("/items/", response_model=list[Item])
async def read_items(
    page: int = Query(1, ge=1),  # Default page number is 1, must be greater than or equal to 1
    per_page: int = Query(10, ge=1, le=100),  # Default items per page is 10, must be between 1 and 100
    db: AsyncIOMotorClient = Depends(Database.get_database)
):
    skip_count = (page - 1) * per_page
    items = await db.items.find().skip(skip_count).limit(per_page).to_list(length=None)
    return items