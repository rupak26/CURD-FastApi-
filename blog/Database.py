from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_USER = "root"
DB_PASSWORD = "12345678"
DB_HOST = "localhost"
DB_NAME = "blog"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

#SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:12345678@localhost:3306/blog"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine , autocommit=False , autoflush=False)

Base = declarative_base()

def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()