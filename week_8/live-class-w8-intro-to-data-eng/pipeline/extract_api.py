import pandas as pd
import requests
import luigi
import os   
import logging
from dotenv import load_dotenv

load_dotenv()
DIR_LOG = os.getenv("DIR_LOG")
DIR_RAW = os.getenv("DIR_RAW")
DIR_TRANSFORM = os.getenv("DIR_TRANSFORM")
DIR_LOAD = os.getenv("DIR_LOAD")

class ExtractAPIPaymentData(luigi.Task):

    def requires(self):
        pass

    def output(self):
        return luigi.LocalTarget(f"{DIR_RAW}/extract_payment_data.csv")

    def run(self):
        logging.basicConfig(filename = f'{DIR_LOG}/logs.log', 
                    level = logging.INFO, 
                    format = '%(asctime)s - %(levelname)s - %(message)s')

        resp = requests.get("https://shandytepe.github.io/payment.json")

        raw_payment_data = resp.json()

        extract_payment_data = pd.DataFrame(raw_payment_data["payment_data"])

        extract_payment_data.to_csv(self.output().path, index = False)