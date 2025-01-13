import pandas as pd
import requests
import luigi
import os   
import logging
from dotenv import load_dotenv

from pipeline.extract_db import ExtractDBHotelData
from pipeline.extract_api import ExtractAPIPaymentData  
from utils.data_validator import validatation_process

load_dotenv()

DIR_LOG = os.getenv("DIR_LOG")
DIR_RAW = os.getenv("DIR_RAW")
DIR_TRANSFORM = os.getenv("DIR_TRANSFORM")
DIR_LOAD = os.getenv("DIR_LOAD")
DIR_VALIDATION = os.getenv("DIR_VALIDATION")

class ValidateData(luigi.Task):

    def requires(self):
        return [ExtractAPIPaymentData(),
                ExtractDBHotelData()]

    def output(self):
        return luigi.LocalTarget(f"{DIR_VALIDATION}/validation.csv")

    def run(self):
        logging.basicConfig(filename = f'{DIR_LOG}/logs.log', 
                    level = logging.INFO, 
                    format = '%(asctime)s - %(levelname)s - %(message)s')
        
        # read payment data
        validate_payment_data = pd.read_csv(self.input()[0].path)

        # read reservation data
        validate_reservation_data = pd.read_csv(self.input()[1][0].path)

        # read customer data
        validate_customer_data = pd.read_csv(self.input()[1][1].path)

        # validate data
        text_payment = validatation_process(data = validate_payment_data,
                             table_name = "payment")

        text_reservation = validatation_process(data = validate_reservation_data,
                             table_name = "reservation")

        text_customer = validatation_process(data = validate_customer_data,
                             table_name = "customer")
        
        pd.DataFrame([text_payment, text_reservation, text_customer]).to_csv(self.output().path, index = True)