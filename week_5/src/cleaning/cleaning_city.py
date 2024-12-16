import pandas as pd

def handling_column_city(city_df, country_df):
    city_df = city_df.merge(country_df, on = 'country', how = 'left')

    city_df = city_df[['city_id', 'country_id', 'city', 'last_update']]

    return city_df

def remove_missing_values_city(city_df):
    city_df = city_df.dropna()

    return city_df

def remove_duplicates_city(city_df):
    city_df = city_df.drop_duplicates(keep='first')

    return city_df