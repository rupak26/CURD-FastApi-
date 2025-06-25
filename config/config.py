import yaml
import urllib.parse
from pathlib import Path

##############################
ENVIRONMENT = "development"
#ENVIRONMENT = "production"
##############################

BASE_DIR = Path(__file__).resolve().parent


def load_config(file_path, environment=None):
    try:
        with open(file_path, "r") as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing the YAML configuration file: {e}")

    if environment not in config:
        raise ValueError(f"Environment '{environment}' not found in the config file.")

    return config[environment]


CONFIG = load_config(BASE_DIR / "config.yaml", ENVIRONMENT)

# Database Configuration
DB_NAME = CONFIG["DATABASE"]["NAME"]
DB_HOST = CONFIG["DATABASE"]["HOST"]
DB_PORT = CONFIG["DATABASE"]["PORT"]
DB_USERNAME = CONFIG["DATABASE"]["USERNAME"]
DB_PASSWORD = CONFIG["DATABASE"]["PASSWORD"]
PRIMARY_DB_URL = f"postgresql+asyncpg://{DB_USERNAME}:{urllib.parse.quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SECONDARY_DB_URL = "sqlite+aiosqlite:///./hfm.db"

# RabbiMQ Configuration
RABBITMQ_URL = CONFIG["RABBITMQ"]["URL"]
EXCHANGE_NAME = CONFIG["RABBITMQ"]["NAME"]
ROUTING_KEY = CONFIG["RABBITMQ"]["KEY"]

# MQTT Configuration
MQTT_HOST = CONFIG["MQTT_BROKER"]["HOST"]
MQTT_PORT = CONFIG["MQTT_BROKER"]["PORT"]
MQTT_USERNAME = CONFIG["MQTT_BROKER"]["USERNAME"]
MQTT_PASSWORD = CONFIG["MQTT_BROKER"]["PASSWORD"]
MQTT_TOPIC = CONFIG["MQTT_BROKER"]["TOPIC"]

# Log Configuration
LOG_DIRECTORY = CONFIG["LOG"]["DIRECTORY"]
LOG_NAME = CONFIG["LOG"]["NAME"]
LOG_SIZE = CONFIG["LOG"]["SIZE"]




# import datetime
# import os
# import sys
# from loguru import logger
# class Rotator:
#     def __init__(self, *, size, at) -> None:
#         try:
#             now = datetime.datetime.now()

#             self._size_limit = size
#             self._time_limit = now.replace(
#                 hour=at.hour, minute=at.minute, second=at.second
#             )

#             if now >= self._time_limit:
#                 self._time_limit += datetime.timedelta(days=1)
#         except Exception as e:
#             logger.error(f"Error initializing Rotator: {e}")
#             raise

#     def should_rotate(self, message, file) -> bool:
#         try:
#             file.seek(0, 2)
#             if file.tell() + len(message) > self._size_limit:
#                 return True
#             excess = message.record["time"].timestamp() - self._time_limit.timestamp()
#             if excess >= 0:
#                 elapsed_days = datetime.timedelta(seconds=excess).days
#                 self._time_limit += datetime.timedelta(days=elapsed_days + 1)
#                 return True
#             return False
#         except Exception as e:
#             logger.error(f"Error during rotation check: {e}")
#             return False


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
