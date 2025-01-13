import os
from dotenv import load_dotenv

load_dotenv()

DIR_RAW = os.getenv("DIR_RAW")
DIR_TRANSFORM = os.getenv("DIR_TRANSFORM")
DIR_LOAD = os.getenv("DIR_LOAD")
DIR_VALIDATION = os.getenv("DIR_VALIDATION")

def clean_output():
    for file in os.listdir(F"{DIR_RAW}"):
        os.remove(f"{DIR_RAW}/{file}")
    for file in os.listdir(f"{DIR_VALIDATION}"):
        os.remove(f"{DIR_VALIDATION}/{file}")
    for file in os.listdir(f"{DIR_LOAD}"):
        os.remove(f"{DIR_LOAD}/{file}")
    for file in os.listdir(f"{DIR_TRANSFORM}"):
        os.remove(f"{DIR_TRANSFORM}/{file}")