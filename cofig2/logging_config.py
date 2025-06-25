import logging , os
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
from cofig2.config import LOG_DIRECTORY , LOG_NAME , LOG_SIZE , ENVIRONMENT as environment

print("===============================")
print(LOG_DIRECTORY)


LOG_DIRECTORY = "/home/user/FastAPI/CURD-FastApi--1/cofig2"
LOG_NAME = "app.log"


LOG_PATH = os.path.join(LOG_DIRECTORY, LOG_NAME)

def setup_logging():
    # Timed rotating file handler: rotates daily at midnight, keeps 7 backups
    file_handler = TimedRotatingFileHandler(
        filename=LOG_PATH,
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8",
        utc=True
    )

    # Log format
    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )
    file_handler.setFormatter(formatter)

    # Log level based on environment
    if environment == "development":
        file_handler.setLevel(logging.INFO)
        console_level = logging.INFO
    else:
        file_handler.setLevel(logging.ERROR)
        console_level = logging.ERROR

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(console_level)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)  # Capture all logs, handlers filter
    root_logger.handlers = []  # Clear existing handlers to prevent duplication
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)




# def setup_logging() -> None:
#     try:
#         os.makedirs(LOG_DIRECTORY, exist_ok=True)
#     except Exception as e:
#         logger.error(f"Error creating log directory at {LOG_DIRECTORY}: {e}")
#         return

#     try:
#         log_file = os.path.join(LOG_DIRECTORY, LOG_NAME)
#         log_rotation_size = LOG_SIZE * 1024 * 1024
#         log_rotation_time = datetime.time(0, 0, 0)
#         rotator = Rotator(size=log_rotation_size, at=log_rotation_time)
#     except Exception as e:
#         logger.error(f"Error setting up log rotation: {e}")
#         return

#     try:
#         log_format = (
#             "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
#             "<level>{level}</level> | "
#             "<cyan>{file}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
#             "<level>{message}</level> | "
#         )
#         logger.remove()
#         logger.add(sys.stdout, level="DEBUG", format=log_format)
#         logger.add(
#             log_file, rotation=rotator.should_rotate, level="DEBUG", format=log_format
#         )
#     except Exception as e:
#         logger.error(f"Error setting up loggers: {e}")
#         return
