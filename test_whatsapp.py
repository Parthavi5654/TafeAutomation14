
import os
import requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
API_VERSION = os.getenv("WHATSAPP_API_VERSION", "v26.0")
TEST_TO = os.getenv("WHATSAPP_TEST_TO")

DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"

BASE_URL = f"https://graph.facebook.com/{API_VERSION}"


def check_connection():
    """Check whether the token and Phone Number ID are valid."""

    if not ACCESS_TOKEN or not PHONE_NUMBER_ID:
        print("ERROR: Missing credentials in .env")
        return False

    url = f"{BASE_URL}/{PHONE_NUMBER_ID}"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    params = {
        "fields": "id,display_phone_number,verified_name"
    }

    print("\nChecking WhatsApp API connection...")

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=20
        )

        if response.ok:
            data = response.json()

            print("SUCCESS: WhatsApp connection working!")
            print("Phone Number ID:", data.get("id"))
            print("Sender Number:", data.get("display_phone_number"))
            print("Verified Name:", data.get("verified_name"))
            return True

        print("CONNECTION FAILED")
        print("HTTP Status:", response.status_code)
        print("Error:", response.text)
        return False

    except requests.RequestException as error:
        print("Network error:", error)
        return False


def send_test_message():
    """Send Meta's hello_world test template."""

    if not TEST_TO:
        print("ERROR: Add WHATSAPP_TEST_TO to .env")
        return

    if DRY_RUN:
        print("\nDRY_RUN is enabled.")
        print("No WhatsApp message was sent.")
        print("Test recipient:", TEST_TO)
        print("Set DRY_RUN=false when ready to send.")
        return

    url = f"{BASE_URL}/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": TEST_TO,
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {
                "code": "en_US"
            }
        }
    }

    print("\nSending test WhatsApp message...")

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=20
        )

        if response.ok:
            result = response.json()
            message_id = result.get("messages", [{}])[0].get("id")

            print("SUCCESS: Meta accepted the message request!")
            print("Message ID:", message_id)
            print("Check your WhatsApp for the test message.")

        else:
            print("MESSAGE SENDING FAILED")
            print("HTTP Status:", response.status_code)
            print("Error:", response.text)

    except requests.RequestException as error:
        print("Network error:", error)


if __name__ == "__main__":
    print("===== WHATSAPP API TEST =====")

    if check_connection():
        send_test_message()
    else:
        print("\nFix the connection error before testing messages.")
