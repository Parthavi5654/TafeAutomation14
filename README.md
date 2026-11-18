# TAFE – Cloud Excel & WhatsApp Payment Reminder Automation

## Overview

TAFE is a Python-based automation project designed to access Excel files stored in Microsoft OneDrive and SharePoint using the Microsoft Graph API.

The project is being developed to automate customer payment reminders for a tractor showroom. It reads customer payment information from Excel, identifies outstanding balances, and uses the WhatsApp Business Cloud API to send payment reminders.

The long-term goal is to provide automated payment follow-ups without requiring showroom staff to manually initiate each reminder.

## Features

### Microsoft Cloud Integration
- Microsoft account authentication using MSAL.
- Secure token caching for authentication.
- Access to OneDrive files through Microsoft Graph API.
- Retrieve and list files stored in OneDrive.
- Foundation for accessing Excel workbooks stored in Microsoft cloud.

### Excel Processing
- Read customer payment information from Excel.
- Identify customers with outstanding balances.
- Extract customer names, mobile numbers, purchase dates, and pending amounts.
- Validate customer information before processing reminders.
- Use the `BAKI` column as the source of the outstanding payment balance.

### WhatsApp Integration
- Integration with Meta WhatsApp Business Cloud API.
- Authentication using WhatsApp access tokens.
- Send WhatsApp messages using approved message templates.
- Support for personalized payment reminders.
- Dry-run mode for safe testing.

### Reminder Management
- Reminder scheduling based on purchase dates.
- Six-day reminder interval.
- SQLite database for storing reminder history.
- Prevent repeated reminders using previous reminder records.
- Skip customers whose outstanding balance is zero.

## Tech Stack

- Python
- Microsoft Graph API
- Microsoft Authentication Library (MSAL)
- Meta WhatsApp Business Cloud API
- SQLite
- Pandas
- OpenPyXL
- Requests
- python-dotenv
- uv (Python package and environment manager)

## Project Structure

```text
tafe/
├── data/
│   ├── tractor_payment.xlsx
│   └── reminder_history.db
│
├── src/
│   └── tafe/
│       ├── __init__.py
│       ├── auth.py
│       ├── models.py
│       ├── excel_reader.py
│       ├── database.py
│       ├── reminder_service.py
│       └── whatsapp_service.py
│
├── .env
├── .env.example
├── .gitignore
├── main.py
├── main1.py
├── test_whatsapp.py
├── test_payment_reminder.py
├── check_templates.py
├── pyproject.toml
├── requirements.txt
├── uv.lock
└── README.md
```

*Note: The project structure may change as additional modules are developed.*

## Prerequisites

- Python version specified in `.python-version`.
- Git.
- uv.
- A Microsoft Entra ID application registration.
- Microsoft Graph API delegated permission: `Files.Read`.
- A Meta Developer account.
- A Meta Developer App configured for WhatsApp.
- A WhatsApp Business Account and configured phone number.
- An approved WhatsApp message template for payment reminders.

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/tafe.git
cd tafe
```

Install dependencies:

```bash
uv sync
```

## Configuration

Create a local `.env` file using the example:

**Windows PowerShell:**

```powershell
Copy-Item .env.example .env
```

Configure your Microsoft application:

```env
CLIENT_ID=your-microsoft-client-id
TENANT_ID=organizations
```

Configure your WhatsApp Cloud API credentials:

```env
WHATSAPP_ACCESS_TOKEN=your-whatsapp-access-token
WHATSAPP_PHONE_NUMBER_ID=your-phone-number-id
WHATSAPP_BUSINESS_ACCOUNT_ID=your-whatsapp-business-account-id

WHATSAPP_API_VERSION=v26.0
WHATSAPP_TEMPLATE_NAME=payment_reminder
WHATSAPP_TEMPLATE_LANGUAGE=your-approved-template-language

WHATSAPP_TEST_TO=91XXXXXXXXXX

SHOWROOM_NAME=Your Showroom Name

DRY_RUN=true
```

Replace the placeholder values with your actual configuration.

**Important:** Keep `.env` private. Never commit access tokens, credentials, or customer information to GitHub.

## Microsoft Authentication

Run the following command to authenticate with Microsoft:

```bash
uv run python -c "from src.tafe.auth import login_device_flow; login_device_flow()"
```

Follow the device login instructions displayed in the terminal.

## Run the Application

Run the Microsoft OneDrive integration:

```bash
uv run python main.py
```

Run the payment reminder workflow:

```bash
uv run python main1.py
```

## WhatsApp API Testing

Test the WhatsApp API connection:

```bash
uv run python test_whatsapp.py
```

Test a personalized payment reminder:

```bash
uv run python test_payment_reminder.py
```

Check available WhatsApp message templates:

```bash
uv run python check_templates.py
```

For initial development and testing, keep:

```env
DRY_RUN=true
```

Set `DRY_RUN=false` only when you intentionally want to send a real message to an authorized test recipient.

WhatsApp business-initiated reminders require an approved message template and appropriate customer opt-in.

## Payment Reminder Workflow

The intended automation workflow is:

1. Retrieve the latest customer payment information from Excel.
2. Identify customers with outstanding balances.
3. Validate customer details and mobile numbers.
4. Check whether a reminder is due.
5. Send a WhatsApp payment reminder using an approved template.
6. Store the reminder attempt and message information in SQLite.
7. Repeat the reminder process every six days until the outstanding balance is cleared.

The latest outstanding amount should always be read from Excel before sending a reminder.

## Planned Features

- Connect directly to client Excel workbooks in OneDrive and SharePoint.
- Retrieve real-time updated Excel payment information through Microsoft Graph API.
- Update reminder information in Excel safely.
- Track WhatsApp message delivery and failure statuses using webhooks.
- Automate daily reminder execution.
- Generate and email payment follow-up reports to the showroom owner every five days.
- Deploy the automation to a cloud server.
- Support multiple reminder languages.

## Development

Create a feature branch before working on a new module:

```bash
git checkout -b feature/your-feature-name
```

Commit and push your changes:

```bash
git add .
git commit -m "Describe your changes"
git push -u origin feature/your-feature-name
```

## Security

- Do not commit `.env` files.
- Do not commit access tokens or authentication cache files.
- Do not upload real customer or confidential Excel data.
- Use environment variables for API credentials.
- Use approved WhatsApp message templates.
- Send reminders only to customers who have opted in.
- Keep test and production credentials separate.

## Project Status

**In Development**

Microsoft authentication and basic OneDrive integration have been implemented. Excel customer processing, reminder scheduling logic, SQLite history, and WhatsApp Cloud API messaging have been developed and tested individually.

Integration of the complete automated workflow, delivery tracking, scheduling, owner reporting, and cloud deployment is ongoing.