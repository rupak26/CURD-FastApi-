import logging , os , shutil 
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
import datetime
from cofig2.env_config import (
    LOG_DIRECTORY , LOG_NAME , LOG_SIZE , ENVIRONMENT as environment ,
    EMAIL_HOST , EMAIL_PASSWORD , EMAIL_PORT , EMAIL_USERNAME
   )
from logging.handlers import SMTPHandler


LOG_PATH = os.path.join(LOG_DIRECTORY, LOG_NAME)
ARCHIVE_DIR = os.path.join(LOG_DIRECTORY, "archive")


def setup_email_logging():

    mail_handler = SMTPHandler(
        mailhost=(EMAIL_HOST, EMAIL_PORT),
        fromaddr=EMAIL_USERNAME,
        toaddrs=EMAIL_USERNAME,
        subject="🚨 FastAPI Error Alert",
        credentials=(EMAIL_USERNAME, EMAIL_PASSWORD),
        secure=()  # Enables TLS; Gmail requires it
    )
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    ))
    return mail_handler
   

class ArchiveTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, when='midnight', interval=1, backupCount=7,
                 encoding=None, utc=False, archive_dir=None, **kwargs):
        if archive_dir is None:
            raise ValueError("archive_dir must be provided")

        self.archive_dir = archive_dir
        os.makedirs(self.archive_dir, exist_ok=True)
        super().__init__(filename, when, interval, backupCount, encoding, utc, archive_dir , **kwargs)

    
    def doRollover(self):
        super().doRollover() 
        if self.backupCount > 0:
            logs = sorted([
                f for f in os.listdir(os.path.dirname(self.baseFilename))
                      if f.startswith(os.path.basename(self.baseFilename))
            ])
        for old_log in logs[:-self.backupCount]:
            try:
                src_path = os.path.join(os.path.dirname(self.baseFilename), old_log)
                dst_path = os.path.join(self.archive_dir, old_log)
                shutil.move(src_path, dst_path)
            except Exception as e:
                print(f"Failed to archive log file {old_log}: {e}")



def setup_logging():

    file_handler = ArchiveTimedRotatingFileHandler(
        filename=LOG_PATH,
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8",
        utc=True,
        archive_dir=ARCHIVE_DIR,
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )
    file_handler.setFormatter(formatter)

    if environment == "development":
        file_handler.setLevel(logging.INFO)
        console_level = logging.INFO
    else:
        mail_handler = setup_email_logging()
        file_handler.setLevel(logging.ERROR)
        console_level = logging.ERROR
        

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(console_level)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)  
    root_logger.handlers = []  
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(mail_handler)
    


# import datetime
# import os
# import sys
# import shutil
# from loguru import logger
# from cofig2.env_config import LOG_DIRECTORY , LOG_NAME , LOG_SIZE , ENVIRONMENT as environment

# LOG_PATH = os.path.join(LOG_DIRECTORY, LOG_NAME)
# ARCHIVE_DIR = os.path.join(LOG_DIRECTORY, "archive")

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


# def archive_rotated_logs(rotated_file_path):
#     try:
#         filename = os.path.basename(rotated_file_path)
#         date_prefix = datetime.datetime.utcnow().strftime("%Y-%m-%d")
#         archived_name = f"{date_prefix}-{filename}"
#         dst_path = os.path.join(ARCHIVE_DIR, archived_name)
#         shutil.move(rotated_file_path, dst_path)
#         logger.info(f"Archived {rotated_file_path} → {dst_path}")
#     except Exception as e:
#         logger.error(f"Error archiving log: {e}")


# def setup_logging() -> None:
#     try:
#         os.makedirs(LOG_DIRECTORY, exist_ok=True)
#     except Exception as e:
#         logger.error(f"Error creating log directory at {LOG_DIRECTORY}: {e}")
#         return

#     try:
#         log_file = LOG_PATH
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
#             log_file, 
#             rotation=rotator.should_rotate, 
#             level="DEBUG", 
#             on_rotation=archive_rotated_logs ,
#             format=log_format
#         )
#     except Exception as e:
#         logger.error(f"Error setting up loggers: {e}")
#         return