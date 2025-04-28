from pydantic import BaseModel
from typing import Optional
from bson import ObjectId

# Helper to convert ObjectId to string
def str_id(id):
    if isinstance(id, ObjectId):
        return str(id)
    return id

# Pydantic schema for item
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool

# Response schema for MongoDB with ObjectId
class ItemInDB(Item):
    id: str

    class Config:
        orm_mode = True
