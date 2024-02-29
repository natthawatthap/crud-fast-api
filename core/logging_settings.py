import logging
import os
import time

class LoggingSettings:
    LOG_FILE: str = "app.log"
    LOG_LEVEL: int = logging.DEBUG
    LOG_FORMAT: str = "%(asctime)s - %(levelname)s - %(message)s"

    @staticmethod
    def setup_logging(app):
        # Set up logging
        logger = logging.getLogger(__name__)
        logger.setLevel(LoggingSettings.LOG_LEVEL)

        # Get the absolute path of the log file
        log_file_path = os.path.abspath(LoggingSettings.LOG_FILE)

        # Ensure the log directory exists
        log_dir = os.path.dirname(log_file_path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Create a file handler
        file_handler = logging.FileHandler(log_file_path, mode="a", encoding="utf-8")
        file_handler.setLevel(LoggingSettings.LOG_LEVEL)

        # Create a formatter and set it on the file handler
        formatter = logging.Formatter(LoggingSettings.LOG_FORMAT)
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger.addHandler(file_handler)

        # Middleware to log HTTP requests and responses
        @app.middleware("http")
        async def http_middleware(request, call_next):
            # Get the start time
            start_time = time.time()

            # Get the client's IP address
            client_ip = request.client.host

            # Log the request with the IP address
            logger.info(f"Request from {client_ip}: {request.method} {request.url}")

            # Call the next middleware
            response = await call_next(request)

            # Calculate the latency
            latency = time.time() - start_time

            # Log the response with the IP address and latency
            logger.info(f"Response to {client_ip}: {response.status_code} (Latency: {latency:.6f} seconds)")

            return response

        return logger
