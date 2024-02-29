from motor.motor_asyncio import AsyncIOMotorClient
from core.settings import settings


class Database:
    client: AsyncIOMotorClient = None
    db_name: str = None

    @classmethod
    async def connect_mongodb(cls):
        cls.client = AsyncIOMotorClient(settings.MONGODB_URI)
        cls.db_name = settings.MONGODB_DB_NAME

    @classmethod
    def get_database(cls) -> AsyncIOMotorClient:
        if cls.client is None:
            raise Exception("MongoDB client is not connected.")
        return cls.client[cls.db_name]
