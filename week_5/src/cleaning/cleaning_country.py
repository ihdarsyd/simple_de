import pandas as pd

def handling_column_country(country_df):
    country_df['country_id'] = country_df.index + 1

    return country_df