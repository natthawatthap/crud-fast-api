from fastapi import FastAPI
from v1.api import router as api_router
from core.settings import PORT
from core.models.database import Database

# Create FastAPI instance
app = FastAPI()

# Include API router
app.include_router(api_router, prefix="/v1")

# Connect to MongoDB
@app.on_event("startup")
async def startup_event():
    await Database.connect_mongodb()

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
