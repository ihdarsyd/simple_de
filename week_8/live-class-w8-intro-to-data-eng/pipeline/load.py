import pandas as pd
import requests
import luigi
import os   
import logging
from dotenv import load_dotenv
from pangres import upsert
from pipeline.transform import TransformHotelData
from utils.db_connector import dw_db_engine

load_dotenv()

DIR_LOG = os.getenv("DIR_LOG")
DIR_RAW = os.getenv("DIR_RAW")
DIR_TRANSFORM = os.getenv("DIR_TRANSFORM")
DIR_LOAD = os.getenv("DIR_LOAD")

class LoadData(luigi.Task):

    def requires(self):
        return TransformHotelData()

    def output(self):
        return luigi.LocalTarget(f"{DIR_LOAD}/load_hotel_analysis_data.csv")

    def run(self):
        logging.basicConfig(filename = f'{DIR_LOG}/logs.log', 
                    level = logging.INFO, 
                    format = '%(asctime)s - %(levelname)s - %(message)s')
        # read data from previous task
        load_hotel_data = pd.read_csv(self.input().path)

        load_hotel_data = load_hotel_data.set_index("reservation_id")

        # init data warehouse engine
        dw_engine = dw_db_engine()

        dw_table_name = "hotel_analysis_table"

        # upsert using pangres library
        upsert(con = dw_engine,
               df = load_hotel_data,
               table_name = dw_table_name,
               if_row_exists = "update")

        # save the output
        load_hotel_data.to_csv(self.output().path, index = False)