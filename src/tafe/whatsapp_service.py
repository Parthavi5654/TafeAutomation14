
import os
import requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
API_VERSION = os.getenv("WHATSAPP_API_VERSION", "v26.0")

TEMPLATE_NAME = os.getenv(
    "WHATSAPP_TEMPLATE_NAME",
    "payment_reminder"
)

TEMPLATE_LANGUAGE = os.getenv(
    "WHATSAPP_TEMPLATE_LANGUAGE",
    "en"
)

DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"

BASE_URL = f"https://graph.facebook.com/{API_VERSION}"


def send_payment_reminder(
    mobile: str,
    customer_name: str,
    pending_amount: float,
    showroom_name: str
):
    """
    Send a payment reminder using an approved WhatsApp template.

    Returns a dictionary describing the result.
    """

    if not ACCESS_TOKEN or not PHONE_NUMBER_ID:
        return {
            "success": False,
            "status": "configuration_error",
            "error": "Missing WhatsApp credentials."
        }

    if not mobile or not mobile.isdigit():
        return {
            "success": False,
            "status": "invalid_mobile",
            "error": "Mobile must contain country code and digits only."
        }

    if pending_amount <= 0:
        return {
            "success": False,
            "status": "not_required",
            "error": "No outstanding payment."
        }

    if DRY_RUN:
        print("\n===== WHATSAPP DRY RUN =====")
        print("To:", mobile)
        print("Customer:", customer_name)
        print("Pending amount:", pending_amount)
        print("Showroom:", showroom_name)
        print("Template:", TEMPLATE_NAME)
        print("No message was sent.")

        return {
            "success": True,
            "status": "dry_run",
            "message_id": None
        }

    url = f"{BASE_URL}/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": mobile,
        "type": "template",
        "template": {
            "name": TEMPLATE_NAME,
            "language": {
                "code": TEMPLATE_LANGUAGE
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": customer_name
                        },
                        {
                            "type": "text",
                            "text": showroom_name
                        },
                        {
                            "type": "text",
                            "text": f"{pending_amount:,.2f}"
                        }
                    ]
                }
            ]
        }
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        result = response.json()

        if response.ok:
            message_id = (
                result.get("messages", [{}])[0].get("id")
            )

            print(f"WhatsApp request accepted for {customer_name}")

            return {
                "success": True,
                "status": "accepted",
                "message_id": message_id
            }

        print("WhatsApp API error:", result)

        return {
            "success": False,
            "status": "failed",
            "error": result
        }

    except requests.RequestException as error:
        print("WhatsApp request error:", error)

        return {
            "success": False,
            "status": "failed",
            "error": str(error)
        }
