import pandas as pd
import psycopg2
from sqlalchemy import create_engine


def dw_postgres_engine(database_name):

    # Koneksi ke database
    user = "root"
    password = "qwerty123"
    host = "localhost"
    port = "3000"

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database_name}")

    return engine

def load_cleaning(table_dict):
    # Buat engine postgres
    engine = dw_postgres_engine(database_name = 'dvdrental_clean')

    # Iterasi melalui dictionary table_dict
    for table_name, df in table_dict.items():
        # Insert data ke table
        df.to_sql(table_name, engine, if_exists = 'replace', index = False)

    # Tutup koneksi ke database
    engine.dispose()

def load_analysis(table_dict):
    engine = dw_postgres_engine(database_name = "dvdrental_analysis")

    # Insert data ke table film_list
    not_insert = ['film','actor','category','film_category','film_actor']
    # Iterasi melalui dictionary table_dict
    for table_name, df in table_dict.items():
        if table_name not in not_insert:
            df.to_sql(table_name, engine, if_exists = 'replace', index = False)
    engine.dispose()
    