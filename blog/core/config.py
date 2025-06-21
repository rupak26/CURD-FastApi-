import logging
from pydantic import BaseSettings , Field
from functools import lru_cache
import os


class Settings(BaseSettings):
    env: str = Field("development" , env="ENV")
    debug: bool = Field(True , env="DEBUG")
    app_name: str = Field("BlogManagement_App",env="App_Name")
    allowed_hosts: str =  Field("*", env="ALLOWED_HOSTS") 

    # db_host: str
    # db_port: int
    # db_user: str
    # db_password: str
    # db_name: str

    secret_key: str
    access_token_expire_minutes: int
    log_level: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    settings = Settings()

    # Override or customize behavior based on ENV
    if settings.env == "production":
        settings.debug = False
        settings.log_level = "info"
        settings.db_user = "prod_user"
        settings.db_password = "prod_pass"
        settings.db_name = "prod_db"
        settings.db_host = "prod-db-host"

    elif settings.env == "development":
        settings.debug = True
        settings.log_level = "debug"
        # Use default .env values for DB in dev

    return settings


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)
