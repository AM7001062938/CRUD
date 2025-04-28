from motor.motor_asyncio import AsyncIOMotorClient

# Global MongoDB client variable
client: AsyncIOMotorClient = None

# Updated MongoDB URI
MONGO_URI = "mongodb+srv://amartya:amartya123@amartya.ce3pa84.mongodb.net/Auth_Crud"

# Initialize the MongoDB client and set up the connection
def init_db():
    global client
    client = AsyncIOMotorClient(MONGO_URI)  # Connect using the new URI

def get_db():
    return client.get_database()  # Access the new database "Auth_Crud"
