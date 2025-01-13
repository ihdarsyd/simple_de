import pandas as pd
import requests
import luigi
import os   
import logging
from dotenv import load_dotenv
from pipeline.extract_db import ExtractDBHotelData
from pipeline.extract_api import ExtractAPIPaymentData  

load_dotenv()

DIR_LOG = os.getenv("DIR_LOG")
DIR_RAW = os.getenv("DIR_RAW")
DIR_TRANSFORM = os.getenv("DIR_TRANSFORM")
DIR_LOAD = os.getenv("DIR_LOAD")

class TransformHotelData(luigi.Task):

    def requires(self):
        return [ExtractAPIPaymentData(),
                ExtractDBHotelData()]

    def output(self):
        return luigi.LocalTarget(f"{DIR_TRANSFORM}/transform_hotel_data.csv")

    def run(self):
        logging.basicConfig(filename = f'{DIR_LOG}/logs.log', 
                    level = logging.INFO, 
                    format = '%(asctime)s - %(levelname)s - %(message)s')
        # read data from previous source
        payment_data = pd.read_csv(self.input()[0].path)
        reservation_data = pd.read_csv(self.input()[1][0].path)
        customer_data = pd.read_csv(self.input()[1][1].path)

        # merge data based on condition
        merge_hotel_data = reservation_data.merge(customer_data, how = "left",
                                                  on = "customer_id", suffixes = ("_x1", "_y1"))

        merge_hotel_data = payment_data.merge(merge_hotel_data, how = "left",
                                              on = "reservation_id", suffixes = ("_x2", "_y2"))

        # create full_name column
        merge_hotel_data["full_name"] = merge_hotel_data["first_name"] + " " + merge_hotel_data["last_name"]

        # create currency column
        merge_hotel_data["currency"] = "IDR"

        # extract domain and create domain_email column
        merge_hotel_data["domain_email"] = merge_hotel_data['email'].str.split('@').str[1]

        # select columns based on the requirements
        SELECTED_COLUMNS = ["reservation_id", "full_name", "email", "domain_email",
                            "reservation_date", "payment_date", "start_date", "end_date", "total_price",
                            "currency", "provider", "payment_status"]

        hotel_analysis_data = merge_hotel_data[SELECTED_COLUMNS]

        # impute missing values
        hotel_analysis_data["payment_date"] = hotel_analysis_data["payment_date"].fillna(value = "Tidak Ada Data")

        # save the output to csv
        hotel_analysis_data.to_csv(self.output().path, index = False)

