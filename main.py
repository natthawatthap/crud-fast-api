from fastapi import FastAPI
from v1.api import router as api_router
from core.logging_settings import LoggingSettings
from core.settings import settings
from core.models.database import Database

# Create FastAPI instance
app = FastAPI()

# Include API router
app.include_router(api_router, prefix="/v1")

# Set up logging
logger = LoggingSettings.setup_logging(app)

# Connect to MongoDB
@app.on_event("startup")
async def startup_event():
    await Database.connect_mongodb()
    logger.info("Connected to MongoDB")

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
