import pandas as pd

def load_test_cases(file_path):

    if file_path.suffix.lower() == ".csv":
        return pd.read_csv(file_path)

    if file_path.suffix.lower() == ".xlsx":
        return pd.read_excel(file_path)

    return pd.DataFrame()