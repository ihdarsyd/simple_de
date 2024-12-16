import pandas as pd
from tabulate import tabulate

# pengecekan nama tabel v
def check_table_requirements(actual_table, requirements_table):

    actual_table_name = list(actual_table.keys())
    requirements_table_name = list(requirements_table.keys())
    table_checking = []

    for table_name in requirements_table_name:

        if table_name in actual_table_name:
            table_checking.append([table_name, "✓"]) 

        else:
            table_checking.append([table_name, "✗"])

    table_headers = ['Table_name', 'Is_Exist']
    table = tabulate(table_checking, headers = table_headers, tablefmt = 'grid')
    print("=> STEP 1: Check Table")
    print(table)

# pengecekan ukuran tabel v
def check_shape(actual_table):
    print("=> STEP 2: Check Data Shape")
    shape_checking = []

    for table_name in actual_table:
        n_row = actual_table[table_name].shape[0]
        n_col = actual_table[table_name].shape[1]
        shape_checking.append([table_name, n_row, n_col])

    # Print Table
    table_headers = ['Table_name', 'Number of rows', 'Number of columns']
    table = tabulate(shape_checking, headers = table_headers, tablefmt = 'grid')
    print(table)

# pengecekan kolom -> kolom yang disesuaikan
def check_columns(actual_table, requirements_table):
    print("=> STEP 3: Check Columns")

    for table_name in requirements_table:
        result = []

        # dapatkan nama kolom untuk tabel aktual
        actual_columns = list(actual_table[table_name].columns)

        # dapatkan nama kolom untuk table req
        requirements_columns = []
        requirements_table_data = requirements_table[table_name]
        for column in requirements_table_data:
            requirements_columns.append(column['column_name'])

        for column_name in set(actual_columns + requirements_columns):
            in_actual_table = '✔' if column_name in actual_columns else '✘'
            in_requirements_table = '✔' if column_name in requirements_columns else '✘'
            result.append([column_name, in_actual_table, in_requirements_table])

        if set(actual_columns) == set(requirements_columns):
            pass

        else:
            headers = ["column_name", "in_actual_table", "in_requirements_table"]
            print(f"Table : {table_name}")
            print(tabulate(result, headers = headers, tablefmt = "grid"))
            print("\n")

# pengecekan data type -> casting
def check_data_types(actual_table, requirements_table):
    print("=> STEP 4: Check Data Types")
    summary_data = []

    for table_name, df in actual_table.items():
        if table_name in requirements_table:
            for column_info in requirements_table[table_name]:
                column_name = column_info["column_name"]
                requirements_type = column_info["data_type"]

                if column_name in df.columns:
                    actual_type = str(df[column_name].dtype)
                    match = "✔" if actual_type == requirements_type else "✘"
                    summary_data.append([table_name, column_name, actual_type, requirements_type, match])
                else:
                    summary_data.append([table_name, column_name, "N/A", requirements_type, "✘ (Column not found)"])

    headers = ["Table Name", "Column Name", "Actual Type", "Requirements Type", "Match"]

    mismatch_data = [row for row in summary_data if "✘" in row[4]]

    if mismatch_data:
        print("\nSummary of Mismatches Data Types:")
        print(tabulate(mismatch_data, headers = headers, tablefmt = "grid"))

    else:
        print("All Data Types Match")

# missing value -> handle biarkan/dihapus
def check_missing_values(actual_table):
    print("=> STEP 5: Check Missing Values")

    missing_summary = []

    for table_name, df in actual_table.items():
        missing_count = df.isnull().sum()
        missing_percentage = (df.isnull().mean() * 100).round(2)

        for column_name, count in missing_count.items():
            if count > 0:
                percentage = missing_percentage[column_name]
                missing_summary.append([table_name, column_name, count, percentage])

    if missing_summary:
        print("Missing Value Summary:")
        print(tabulate(missing_summary, headers=["Table Name", "Column Name", "Missing Value Count", "Missing Value Percentage"], tablefmt="grid"))

    else:
        print("There's no Missing Values")


# dupliacate data -> handle dibiarkan/hihapus
def check_duplicates_data(actual_table):
    print("=> STEP 6: Check Duplicates Data")
    duplicate_summary = []

    for table_name, df in actual_table.items():
        try:
            duplicate_rows = df[df.duplicated(keep = False)]

            if not duplicate_rows.empty:
                duplicate_summary.append([table_name, len(duplicate_rows)])
        except:
            pass

    if duplicate_summary:
        print("Duplicate Data Summary:")
        print(tabulate(duplicate_summary, headers=["Table Name", "Duplicate Rows Count"], tablefmt="grid"))
    else:
        print("No Duplicate Data Found")