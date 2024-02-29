# main.py

import logging
from fastapi import FastAPI
from v1.api import router as api_router
from core.settings import PORT
from core.models.database import Database

# Create FastAPI instance
app = FastAPI()

# Include API router
app.include_router(api_router, prefix="/v1")

# Define startup event handler to connect to MongoDB
@app.on_event("startup")
async def startup_event():
    try:
        # Connect to MongoDB during application startup
        await Database.connect_mongodb()
        logging.info("Connected to MongoDB")
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB: {e}")

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
