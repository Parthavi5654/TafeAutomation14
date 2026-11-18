
import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
WABA_ID = os.getenv("WHATSAPP_BUSINESS_ACCOUNT_ID")
VERSION = os.getenv("WHATSAPP_API_VERSION", "v26.0")

url = f"https://graph.facebook.com/{VERSION}/{WABA_ID}/message_templates"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

params = {
    "fields": "name,status,language,category",
    "limit": 100
}

response = requests.get(
    url,
    headers=headers,
    params=params,
    timeout=30
)

print("HTTP Status:", response.status_code)

if response.ok:
    templates = response.json().get("data", [])

    if not templates:
        print("No templates found for this WhatsApp Business Account.")

    for template in templates:
        print("\n--------------------------")
        print("Name:", template.get("name"))
        print("Status:", template.get("status"))
        print("Language:", template.get("language"))
        print("Category:", template.get("category"))
else:
    print(response.text)
