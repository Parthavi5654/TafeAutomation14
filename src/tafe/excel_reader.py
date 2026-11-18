
# import re
# from pathlib import Path
# from datetime import date

# import pandas as pd

# from .models import Customer


# # Excel file location
# EXCEL_FILE = Path("data/tractor_payment.xlsx")

# # Your workbook's headings are on the second row.
# HEADER_ROW = 1


# def normalize_mobile(value):
#     """
#     Remove spaces and special characters from a mobile number.
#     Accept numbers containing 10 to 15 digits.
#     """
#     if pd.isna(value):
#         return None

#     digits = re.sub(r"\D", "", str(value))

#     if digits.startswith("0"):
#         digits = digits.lstrip("0")

#     if 10 <= len(digits) <= 15:
#         return digits

#     return None


# def read_customers():
#     """
#     Read Excel and return customers with BAKI > 0.

#     Also identify missing or invalid data.
#     """

#     if not EXCEL_FILE.exists():
#         raise FileNotFoundError(
#             f"Excel file not found: {EXCEL_FILE}"
#         )

#     df = pd.read_excel(
#         EXCEL_FILE,
#         header=HEADER_ROW,
#         engine="openpyxl"
#     )

#     # Normalize column names
#     df.columns = [
#         str(column).strip().upper()
#         for column in df.columns
#     ]

#     required_columns = [
#         "NAME",
#         "MOBILE",
#         "DATE",
#         "BAKI"
#     ]

#     missing_columns = [
#         column
#         for column in required_columns
#         if column not in df.columns
#     ]

#     if missing_columns:
#         raise ValueError(
#             f"Missing Excel columns: {missing_columns}"
#         )

#     customers = []

#     for index, row in df.iterrows():

#         errors = []

#         # Read customer name
#         name = (
#             str(row["NAME"]).strip()
#             if pd.notna(row["NAME"])
#             else ""
#         )

#         if not name:
#             errors.append("Missing customer name")

#         # Validate mobile number
#         mobile = normalize_mobile(row["MOBILE"])

#         if not mobile:
#             errors.append("Missing or invalid mobile number")

#         # Read purchase date
#         purchase_date = None

#         if pd.notna(row["DATE"]):
#             try:
#                 purchase_date = pd.to_datetime(
#                     row["DATE"]
#                 ).date()
#             except (ValueError, TypeError):
#                 errors.append("Invalid purchase date")
#         else:
#             errors.append("Missing purchase date")

#         # Read outstanding balance
#         try:
#             if pd.isna(row["BAKI"]):
#                 pending_amount = 0.0
#                 errors.append("Missing BAKI amount")
#             else:
#                 pending_amount = float(row["BAKI"])

#         except (ValueError, TypeError):
#             pending_amount = 0.0
#             errors.append("Invalid BAKI amount")

#         # Ignore customers who have no outstanding balance.
#         if pending_amount <= 0:
#             continue

#         # Temporary ID until a permanent CUSTOMER_ID exists.
#         customer_id = f"ROW-{index + HEADER_ROW + 2}"

#         customer = Customer(
#             customer_id=customer_id,
#             name=name,
#             mobile=mobile,
#             purchase_date=purchase_date,
#             pending_amount=pending_amount,
#             excel_row=index + HEADER_ROW + 2,
#             errors=errors
#         )

#         customers.append(customer)

#     return customers

import re
from pathlib import Path

import pandas as pd

from .models import Customer


EXCEL_FILE = Path("data/Tractor_Payment_Master.xlsx")
HEADER_ROW = 1


def normalize_mobile(value):
    if pd.isna(value):
        return None

    digits = re.sub(r"\D", "", str(value))

    if digits.startswith("0"):
        digits = digits.lstrip("0")

    if 10 <= len(digits) <= 15:
        return digits

    return None


def read_customers():

    if not EXCEL_FILE.exists():
        raise FileNotFoundError(
            f"Excel file not found: {EXCEL_FILE}"
        )

    df = pd.read_excel(
        EXCEL_FILE,
        header=HEADER_ROW,
        engine="openpyxl"
    )

    df.columns = [
        str(column).strip().upper()
        for column in df.columns
    ]

    required_columns = ["NAME", "MOBILE", "DATE", "BAKI"]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing Excel columns: {missing_columns}"
        )

    customers = []

    for index, row in df.iterrows():

        errors = []

        name = (
            str(row["NAME"]).strip()
            if pd.notna(row["NAME"])
            else ""
        )

        if not name:
            errors.append("Missing customer name")

        mobile = normalize_mobile(row["MOBILE"])

        if not mobile:
            errors.append("Missing or invalid mobile number")

        purchase_date = None

        if pd.notna(row["DATE"]):
            try:
                purchase_date = pd.to_datetime(
                    row["DATE"]
                ).date()
            except (ValueError, TypeError):
                errors.append("Invalid purchase date")
        else:
            errors.append("Missing purchase date")

        try:
            if pd.isna(row["BAKI"]):
                pending_amount = 0.0
                errors.append("Missing BAKI amount")
            else:
                pending_amount = float(row["BAKI"])

        except (ValueError, TypeError):
            pending_amount = 0.0
            errors.append("Invalid BAKI amount")

        if pending_amount <= 0:
            continue

        customer = Customer(
            customer_id=f"ROW-{index + HEADER_ROW + 2}",
            name=name,
            mobile=mobile,
            purchase_date=purchase_date,
            pending_amount=pending_amount,
            excel_row=index + HEADER_ROW + 2,
            errors=errors
        )

        customers.append(customer)

    return customers
