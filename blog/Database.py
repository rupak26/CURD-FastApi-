from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os , logging
from dotenv import load_dotenv
from cofig2.env_config import PRIMARY_DB_URL as DATABASE_URL

logger = logging.getLogger("database")
load_dotenv()


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine , autocommit=False , autoflush=False)

Base = declarative_base()

def get_db():
    db = SessionLocal() 
    try:
        logger.info("DB session opened")
        yield db
    except Exception as e:
        logger.error(f"DB session error: {e}")
        raise
    finally:
        db.close()
        logger.info("DB session closed")