import luigi
import pandas as pd
import requests
from helper.db_connector import source_db_engine, dw_db_engine
from helper.data_validator import validatation_process
from pangres import upsert
import logging
import os

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

class ValidateData(luigi.Task):

    def requires(self):
        return [ExtractAPIPaymentData(),
                ExtractDBHotelData()]
    
    def output(self):
        pass

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
        validatation_process(data = validate_payment_data,
                             table_name = "payment")
        
        validatation_process(data = validate_reservation_data,
                             table_name = "reservation")
        
        validatation_process(data = validate_customer_data,
                             table_name = "customer")


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

        load_hotel_data.insert(0, 'analysis_id', range(0, 0 + len(load_hotel_data)))

        load_hotel_data = load_hotel_data.set_index("analysis_id")

        # init data warehouse engine
        dw_engine = dw_db_engine()

        dw_table_name = "hotel_analysis_table"

        upsert(con = dw_engine,
               df = load_hotel_data,
               table_name = dw_table_name,
               if_row_exists = "update")

        # # insert data to data warehouse
        # load_hotel_data.to_sql(name = dw_table_name,
        #                        con = dw_engine,
        #                        if_exists = "append",
        #                        index = False)

        # save the output
        load_hotel_data.to_csv(self.output().path, index = False)

if __name__ == "__main__":
    
    luigi.build([ExtractAPIPaymentData(),
                ExtractDBHotelData(),
                ValidateData(),
                TransformHotelData(),
                LoadData()])