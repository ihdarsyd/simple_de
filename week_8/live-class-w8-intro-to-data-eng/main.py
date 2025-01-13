from pipeline.extract_api import ExtractAPIPaymentData
from pipeline.extract_db import ExtractDBHotelData
from pipeline.validation import ValidateData
from pipeline.transform import TransformHotelData
from pipeline.load import LoadData
from utils.clean_directory import clean_output
import luigi



if __name__ == "__main__":
    luigi.build([ExtractAPIPaymentData(), ExtractDBHotelData(), ValidateData(), TransformHotelData(), LoadData()])
    clean_output()

