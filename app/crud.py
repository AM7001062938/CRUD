from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from .models import ItemInDB
from .schemas import ItemCreate, ItemUpdate
from typing import List

class CRUD:
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = db["Auth_Crud"]["books"]  # Direct access to collection

    async def create_item(self, item: ItemCreate) -> ItemInDB:
        try:
            doc = item.dict()
            result = await self.collection.insert_one(doc)
            doc['id'] = str(result.inserted_id)  # Convert _id to id
            return ItemInDB(**doc)
        except Exception as e:
            # Handle error (e.g., log it, re-raise, etc.)
            raise ValueError(f"Error creating item: {e}")

    async def get_item(self, item_id: str) -> ItemInDB:
        try:
            document = await self.collection.find_one({"_id": ObjectId(item_id)})
            if document:
                document['id'] = str(document['_id'])
                return ItemInDB(**document)
            return None
        except Exception as e:
            raise ValueError(f"Error retrieving item with id {item_id}: {e}")

    async def get_items(self) -> List[ItemInDB]:
        try:
            items = []
            async for document in self.collection.find():
                document['id'] = str(document['_id'])
                items.append(ItemInDB(**document))
            return items
        except Exception as e:
            raise ValueError(f"Error retrieving items: {e}")

    async def update_item(self, item_id: str, item: ItemUpdate) -> ItemInDB:
        try:
            update_data = {k: v for k, v in item.dict(exclude_unset=True).items()}
            await self.collection.update_one({"_id": ObjectId(item_id)}, {"$set": update_data})
            return await self.get_item(item_id)
        except Exception as e:
            raise ValueError(f"Error updating item with id {item_id}: {e}")

    async def delete_item(self, item_id: str) -> bool:
        try:
            result = await self.collection.delete_one({"_id": ObjectId(item_id)})
            return result.deleted_count > 0
        except Exception as e:
            raise ValueError(f"Error deleting item with id {item_id}: {e}")
