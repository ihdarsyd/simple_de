from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

SOURCE_DB_USERNAME = os.getenv("SOURCE_DB_USERNAME")
SOURCE_DB_PASSWORD = os.getenv("SOURCE_DB_PASSWORD")
SOURCE_DB_HOST = os.getenv("SOURCE_DB_HOST")
SOURCE_DB_PORT = os.getenv("SOURCE_DB_PORT")
SOURCE_DB_NAME = os.getenv("SOURCE_DB_NAME")

WAREHOUSE_DB_USERNAME = os.getenv("WAREHOUSE_DB_USERNAME")
WAREHOUSE_DB_PASSWORD = os.getenv("WAREHOUSE_DB_PASSWORD")
WAREHOUSE_DB_HOST = os.getenv("WAREHOUSE_DB_HOST")
WAREHOUSE_DB_PORT = os.getenv("WAREHOUSE_DB_PORT")
WAREHOUSE_DB_NAME = os.getenv("WAREHOUSE_DB_NAME")


def source_db_engine():
    engine = create_engine(f"postgresql://{SOURCE_DB_USERNAME}:{SOURCE_DB_PASSWORD}@{SOURCE_DB_HOST}:{SOURCE_DB_PORT}/{SOURCE_DB_NAME}")

    return engine

def dw_db_engine():
    warehouse_engine = create_engine(f"postgresql://{WAREHOUSE_DB_USERNAME}:{WAREHOUSE_DB_PASSWORD}@{WAREHOUSE_DB_HOST}:{WAREHOUSE_DB_PORT}/{WAREHOUSE_DB_NAME}")

    return warehouse_engine