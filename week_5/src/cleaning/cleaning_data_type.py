import pandas as pd
def adjust_data_types(actual_table, requirements_table):
    adjusted_table_dict = {}

    for table_name, df in actual_table.items():
        if table_name in requirements_table:
            table_requirements = requirements_table[table_name]

            for column_info in table_requirements:
                column_name = column_info["column_name"]
                data_type = column_info["data_type"]

                if column_name in df.columns:
                    df[column_name] = df[column_name].astype(data_type)

            adjusted_table_dict[table_name] = df

    return adjusted_table_dict