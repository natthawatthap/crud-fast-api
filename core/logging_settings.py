import logging


class LoggingSettings:
    LOG_FILE: str = "app.log"
    LOG_LEVEL: int = logging.DEBUG
    LOG_FORMAT: str = "%(asctime)s - %(levelname)s - %(message)s"

    @staticmethod
    def setup_logging(app):
        # Set up logging
        logger = logging.getLogger(__name__)
        logger.setLevel(LoggingSettings.LOG_LEVEL)

        # Create a file handler
        file_handler = logging.FileHandler(LoggingSettings.LOG_FILE)
        file_handler.setLevel(LoggingSettings.LOG_LEVEL)

        # Create a formatter and set it on the file handler
        formatter = logging.Formatter(LoggingSettings.LOG_FORMAT)
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger.addHandler(file_handler)

        # Middleware to log HTTP requests and responses
        @app.middleware("http")
        async def http_middleware(request, call_next):
            # Log the request
            logger.info(f"Request: {request.method} {request.url}")

            # Call the next middleware
            response = await call_next(request)

            # Log the response
            logger.info(f"Response: {response.status_code}")

            return response

        return logger
