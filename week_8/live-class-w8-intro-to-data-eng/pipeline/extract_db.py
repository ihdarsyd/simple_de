import pandas as pd
import requests
import luigi
import os   
import logging
from dotenv import load_dotenv

from utils.db_connector import source_db_engine

load_dotenv()
DIR_LOG = os.getenv("DIR_LOG")
DIR_RAW = os.getenv("DIR_RAW")
DIR_TRANSFORM = os.getenv("DIR_TRANSFORM")
DIR_LOAD = os.getenv("DIR_LOAD")

class ExtractDBHotelData(luigi.Task):

    def requires(self):
        pass

    def output(self):
        return [luigi.LocalTarget(f"{DIR_RAW}/extract_reservation_data.csv"),
                luigi.LocalTarget(f"{DIR_RAW}/extract_customer_data.csv")]

    def run(self):
        logging.basicConfig(filename = f'{DIR_LOG}/logs.log', 
                    level = logging.INFO, 
                    format = '%(asctime)s - %(levelname)s - %(message)s')
        # initiate engine
        source_engine = source_db_engine()

        # extract reservation data
        query_reservation = "SELECT * FROM reservation"

        extract_reservation_data = pd.read_sql(sql = query_reservation,
                                               con = source_engine)

        # extract customer data
        query_customer = "SELECT * FROM customer"

        extract_customer_data = pd.read_sql(sql = query_customer,
                                            con = source_engine)

        # save the output
        extract_reservation_data.to_csv(self.output()[0].path, index = False)
        extract_customer_data.to_csv(self.output()[1].path, index = False)
