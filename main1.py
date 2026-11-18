# print("Hello from main1.py!")
# from tafe.excel_reader import read_customers

# def main():

#     print("\nStarting Phase 1: Excel Data Processing\n")

#     customers = read_customers()

#     print(f"Customers with outstanding payments: {len(customers)}")

#     print("\nCUSTOMER DETAILS")
#     print("-" * 65)

#     for customer in customers:

#         print(f"Customer ID : {customer.customer_id}")
#         print(f"Name        : {customer.name}")
#         print(f"Mobile      : {customer.mobile}")
#         print(f"Purchase    : {customer.purchase_date}")
#         print(f"BAKI        : {customer.pending_amount:.2f}")
#         print(f"Excel Row   : {customer.excel_row}")

#         if customer.errors:
#             print("Errors      :", ", ".join(customer.errors))
#         else:
#             print("Validation  : Passed")

#         print("-" * 65)

#     valid_customers = [
#         customer for customer in customers
#         if not customer.errors
#     ]

#     invalid_customers = [
#         customer for customer in customers
#         if customer.errors
#     ]

#     print("\nSUMMARY")
#     print(f"Total pending customers : {len(customers)}")
#     print(f"Valid customer records  : {len(valid_customers)}")
#     print(f"Records with errors     : {len(invalid_customers)}")


# if __name__ == "__main__":
#     main()


# from tafe.excel_reader import read_customers


# def main():
#     print("\n===== PHASE 1: EXCEL DATA PROCESSING =====\n")

#     customers = read_customers()

#     valid_customers = [
#         customer for customer in customers
#         if not customer.errors
#     ]

#     invalid_customers = [
#         customer for customer in customers
#         if customer.errors
#     ]

#     print(f"Total pending customers: {len(customers)}")
#     print(f"Valid customers: {len(valid_customers)}")
#     print(f"Customers with errors: {len(invalid_customers)}")

#     print("\n===== VALID CUSTOMERS =====")

#     for customer in valid_customers:
#         print(
#             f"ID: {customer.customer_id} | "
#             f"Name: {customer.name} | "
#             f"Mobile: {customer.mobile} | "
#             f"BAKI: {customer.pending_amount}"
#         )

#     print("\n===== CUSTOMERS WITH ERRORS =====")

#     for customer in invalid_customers:
#         print(
#             f"ID: {customer.customer_id} | "
#             f"Name: {customer.name} | "
#             f"Errors: {', '.join(customer.errors)}"
#         )


# if __name__ == "__main__":
#     main()



from tafe.excel_reader import read_customers
from tafe.database import initialize_database
from tafe.reminder_service import get_customers_due_for_reminder


def main():

    print("\n===== PHASE 2: REMINDER BUSINESS LOGIC =====\n")

    # Create database and reminder history table.
    initialize_database()

    # Read the latest Excel data.
    customers = read_customers()

    print(f"Total pending customers: {len(customers)}")

    # Find customers whose reminders are due.
    due_customers = get_customers_due_for_reminder(customers)

    print(f"Reminders due today: {len(due_customers)}")

    print("\n===== CUSTOMERS DUE FOR REMINDER =====")

    for customer in due_customers:

        print(f"Customer ID : {customer.customer_id}")
        print(f"Name        : {customer.name}")
        print(f"Mobile      : {customer.mobile}")
        print(f"Purchase    : {customer.purchase_date}")
        print(f"Pending     : {customer.pending_amount}")
        print("-" * 40)

    if not due_customers:
        print("No customers are due for a reminder today.")


if __name__ == "__main__":
    main()