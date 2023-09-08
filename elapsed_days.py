import numpy
import pandas as pd
from datetime import datetime

# Set the financial year start and end dates as global variables

financial_year_start = datetime(2022, 4, 1)
financial_year_end = datetime(2023, 3, 31)


def calculate_elapsed_days(df):
    global financial_year_start, financial_year_end

    for row in df:
        if df.row["START_DATE"] < financial_year_start:
            start_date = financial_year_start
        else:
            start_date = df.row["START_DATE"]

        if df.row["EXPIRY_DATE"] > financial_year_end:
            end_date = financial_year_end
        else:
            end_date = df.row["EXPIRY_DATE"]

        elapsed_days = (end_date - start_date).days + 1
        return elapsed_days


# Example DataFrame
data = {
    "start_date": [datetime(2022, 4, 1), datetime(2022, 3, 2)],
    "end_date": [datetime(2023, 3, 31), datetime(2023, 3, 1)],
}
df = pd.DataFrame(data)

# Apply the calculate_elapsed_days function to each row
df["elapsed_days"] = df.apply(calculate_elapsed_days(data), axis=1)

print(df)
