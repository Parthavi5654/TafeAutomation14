
import os
from dotenv import load_dotenv

from tafe.whatsapp_service import send_payment_reminder

load_dotenv()

test_mobile = os.getenv("WHATSAPP_TEST_TO")
showroom_name = os.getenv("SHOWROOM_NAME", "Tractor Showroom")

if not test_mobile:
    raise ValueError("Add WHATSAPP_TEST_TO to your .env file")

result = send_payment_reminder(
    mobile=test_mobile,
    customer_name="Test Customer",
    pending_amount=25000,
    showroom_name=showroom_name
)

print("\n===== TEST RESULT =====")
print(result)
