import pandas as pd
import psycopg2
from sqlalchemy import create_engine

def extract_api_csv(api_link):
    try:
        df = pd.read_csv(api_link)
        return df
    except  Exception as e:
        print(e)

def get_table_data(table_name):
    dbname = "dvdrental"
    user = "postgres"
    password = "qwerty123"
    host = "localhost"
    port = "5433"

    engine_str = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    engine = create_engine(engine_str)

    try:
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, engine)

        return df

    except Exception as e:
        print(f"Error: {e}")

        return pd.DataFrame()