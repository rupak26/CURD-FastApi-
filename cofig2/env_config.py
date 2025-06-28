import yaml
import urllib.parse
from pathlib import Path

##############################
#ENVIRONMENT = "development"
ENVIRONMENT = "production"
##############################

BASE_DIR = Path(__file__).resolve().parent

def load_config(file_path , environment = None):
    try:
        with open(file_path,"r") as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing the YAML configuration file: {e}")
    
    if environment not in config:
        raise ValueError(f"Environment '{environment}' not found in the config file.")
    
    return config[environment]


CONFIG = load_config(BASE_DIR / "config.yaml", ENVIRONMENT)

DB_NAME = CONFIG["DATABASE"]["NAME"]
DB_HOST = CONFIG["DATABASE"]["HOST"]
DB_PORT = CONFIG["DATABASE"]["PORT"]
DB_USERNAME = CONFIG["DATABASE"]["USERNAME"]
DB_PASSWORD = CONFIG["DATABASE"]["PASSWORD"]


PRIMARY_DB_URL = f"postgresql+psycopg2://{DB_USERNAME}:{urllib.parse.quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

LOG_DIRECTORY = CONFIG["LOG"]["DIRECTORY"]
LOG_NAME = CONFIG["LOG"]["NAME"]
LOG_SIZE = CONFIG["LOG"]["SIZE"]

EMAIL_HOST = CONFIG["EMAIL"]["HOST"]
EMAIL_USERNAME = CONFIG["EMAIL"]["USERNAME"]
EMAIL_PASSWORD = CONFIG["EMAIL"]["PASSWORD"]
EMAIL_PORT = CONFIG["EMAIL"]["PORT"]


