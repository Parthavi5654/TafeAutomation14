
from datetime import date, timedelta

from .database import get_last_successful_reminder


REMINDER_INTERVAL_DAYS = 6


def get_customers_due_for_reminder(customers, today=None):

    today = today or date.today()

    due_customers = []

    for customer in customers:

        # Skip records with invalid data.
        if customer.errors:
            continue

        # Skip customers who have completed payment.
        if customer.pending_amount <= 0:
            continue

        if not customer.mobile or not customer.purchase_date:
            continue

        # First reminder: six days after purchase.
        first_reminder_date = (
            customer.purchase_date
            + timedelta(days=REMINDER_INTERVAL_DAYS)
        )

        if today < first_reminder_date:
            continue

        # Check reminder history.
        last_reminder = get_last_successful_reminder(
            customer.customer_id
        )

        if last_reminder:

            last_reminder_date = last_reminder.date()

            next_reminder_date = (
                last_reminder_date
                + timedelta(days=REMINDER_INTERVAL_DAYS)
            )

            if today < next_reminder_date:
                continue

        due_customers.append(customer)

    return due_customers
