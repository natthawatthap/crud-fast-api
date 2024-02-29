from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from v1.api import router as api_router
from core.logging_settings import LoggingSettings
from core.settings import settings
from core.models.database import Database

# Create FastAPI instance
app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to specific origins if needed
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

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

    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
