import pandas as pd
from datetime import datetime


data = pd.read_excel("corp loss ratio claim.xlsx")  # type: ignore
data1 = pd.read_excel("Final Data Nov - loss ratio -business.xlsx")  # type: ignore

# convert object data type to datetimef
data1["START_DATE"] = pd.to_datetime(data1["START_DATE"], dayfirst=True)
data1["EXPIRY_DATE"] = pd.to_datetime(data1["EXPIRY_DATE"], dayfirst=True)

data1.info()

# Group by policy number tp get total claim amount by each policy
agg_functions = {
    "FINAL_CLAIM_AMOUNT": "sum",
    "Insurance Company ": "any",
    "Final Sector Mapping": "any",
    "VEH_MAKE": "any",
    "VEH_MODEL": "any",
    "NATURE_OF_LOSS": "any",
    "SUB_PRODUCT_NAME": "any",
    "CLAIM_STATUS": "any",
    "DATE_OF_ACCIDENT": "any",
    "INTIMATION_DATE": "any",
    "CASHLESS_CLAIM": "any",
    "PAYMENT_DATE": "any",
}

data2 = data.groupby(by="POLICY_NO").agg(agg_functions).reset_index()

# merge both datsets
df = data1.merge(data2, how="left", on="POLICY_NO")

# Set the financial year start and end dates as global variables
financial_year_start = datetime(2022, 4, 1)
financial_year_end = datetime(2023, 3, 31)


# Create function to calculate days
def calculate_elapsed_days(row):
    global financial_year_start, financial_year_end

    # Skip rows with start date after financial year end or end date before financial year start
    if (
        row["START_DATE"] > financial_year_end
        or row["EXPIRY_DATE"] < financial_year_start
    ):
        return 0

    start_date = max(row["START_DATE"], financial_year_start)
    end_date = min(row["EXPIRY_DATE"], financial_year_end)

    elapsed_days = (end_date - start_date).days + 1
    return elapsed_days


# Create function to divide premiun by days
def calculate_premium_per_day(row):
    if row["elapsed_days"] > 0:
        premium_per_day = row["PBST (NP)"] / row["elapsed_days"]
        return premium_per_day
    else:
        return 0


# Create function to divide od by days
def calculate_od_per_day(row):
    if row["elapsed_days"] > 0:
        od_per_day = row["OD/Brok Premium"] / row["elapsed_days"]
        return od_per_day
    else:
        return 0


# Apply the calculate_elapsed_days function using global financial year dates
df["elapsed_days"] = df.apply(calculate_elapsed_days, axis=1)

# Calculate premium per day
df["premium_per_day"] = df["PBST (NP)"] / 365 * df["elapsed_days"]

# Calculate OD per day
df["od_per_day"] = df["OD/Brok Premium"] / 365 * df["elapsed_days"]


df.to_excel("Final.xlsx")
