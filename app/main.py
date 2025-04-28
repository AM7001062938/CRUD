from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from .models import ItemInDB
from .schemas import ItemCreate, ItemUpdate
from .crud import CRUD
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS Middleware for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client.get_database()
crud = CRUD(db)

# Create item
@app.post("/items/", response_model=ItemInDB)
async def create_item(item: ItemCreate):
    return await crud.create_item(item)

# Get all items
@app.get("/items/", response_model=List[ItemInDB])
async def get_items():
    return await crud.get_items()

# Get single item
@app.get("/items/{item_id}", response_model=ItemInDB)
async def get_item(item_id: str):
    item = await crud.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Update item
@app.put("/items/{item_id}", response_model=ItemInDB)
async def update_item(item_id: str, item: ItemUpdate):
    updated_item = await crud.update_item(item_id, item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

# Delete item
@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    success = await crud.delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return JSONResponse(status_code=200, content={"message": "Item deleted"})
