from src.extract.extract import *
from src.load.load import *
from src.validation.validation import *
from src.cleaning.cleaning_city import *
from src.cleaning.cleaning_country import *
from src.cleaning.cleaning_data_type import *
from src.transformation.manipulation import *
import urllib.request, json
import pandas as pd


city_raw = "https://raw.githubusercontent.com/rahilpacmann/case-data-wrangling-api/main/city.csv"
country_raw = "https://raw.githubusercontent.com/rahilpacmann/case-data-wrangling-api/main/country.csv"

city_df = extract_api_csv(city_raw)
country_df = extract_api_csv(country_raw)

requirements_table_url = 'https://rahilpacmann.github.io/case-data-wrangling-api/requirements_table.json'
with urllib.request.urlopen(requirements_table_url) as url:
    requirements_table = json.load(url)

print(requirements_table.keys())

actor_df = get_table_data('actor')
store_df = get_table_data('store')
address_df = get_table_data('address')
category_df = get_table_data('category')
customer_df = get_table_data('customer')
film_actor_df = get_table_data('film_actor')
film_category_df = get_table_data('film_category')
inventory_df = get_table_data('inventory')
language_df = get_table_data('language')
rental_df = get_table_data('rental')
staff_df = get_table_data('staff')
payment_df = get_table_data('payment')
film_df = get_table_data('film')

# Your code here
table_dict = {'actor': actor_df,
              'store' : store_df,
              'address' : address_df,
              'category' :category_df,
              'customer' : customer_df,
              'film_actor' : film_actor_df,
              'film_category' : film_category_df,
              'inventory' : inventory_df,
              'language' : language_df,
              'rental' : rental_df,
              'staff' : staff_df,
              'payment' : payment_df,
              'film' : film_df,
              'city' : city_df,
              'country' : country_df}

# validation
check_table_requirements(actual_table=table_dict, requirements_table=requirements_table)