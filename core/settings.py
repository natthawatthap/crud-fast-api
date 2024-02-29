from dotenv import load_dotenv
import os

# Load environment variables from .env file if it exists
load_dotenv()

class Settings:
    HOST: str = os.getenv("HOST")
    PORT: int = int(os.getenv("PORT"))
    MONGODB_URI: str = os.getenv("MONGODB_URI")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME")

# Instantiate settings
settings = Settings()
