# TAFE – Cloud Excel Automation

## Overview

TAFE is a Python-based automation project designed to work with Excel files stored in Microsoft OneDrive and SharePoint using the Microsoft Graph API.

The project currently includes Microsoft authentication and OneDrive file access. Additional automation modules will be added as development progresses.

## Features

- Microsoft account authentication using MSAL.
- Secure token caching for authentication.
- Access to OneDrive files through Microsoft Graph API.
- Retrieve and list files stored in OneDrive.
- Designed for future Excel automation workflows.

## Tech Stack

- Python
- Microsoft Graph API
- Microsoft Authentication Library (MSAL)
- Requests
- python-dotenv
- uv (Python package and environment manager)

## Project Structure

```text
tafe/
├── data/
├── src/
│   └── tafe/
│       ├── __init__.py
│       └── auth.py
├── .env.example
├── .gitignore
├── main.py
├── pyproject.toml
├── requirements.txt
├── uv.lock
└── README.md
```

## Prerequisites

- Python (version specified in `.python-version`)
- Git
- uv
- A Microsoft Entra ID application registration
- Microsoft Graph API delegated permission: `Files.Read`

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

Create your local `.env` file using the example:

**Windows PowerShell:**

```powershell
Copy-Item .env.example .env
```

Add your Microsoft application details:

```env
CLIENT_ID=your-microsoft-client-id
TENANT_ID=organizations
```

Never commit your `.env` file or authentication token cache to GitHub.

## Authentication

Run the following command to authenticate with Microsoft:

```bash
uv run python -c "from src.tafe.auth import login_device_flow; login_device_flow()"
```

Follow the device login instructions displayed in the terminal.

## Run the Application

```bash
uv run python main.py
```

The application will retrieve and display files available in your OneDrive.

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
- Use your own Microsoft account credentials for local development.

## Project Status

**In Development** – Authentication and basic OneDrive integration are implemented. Further Excel automation features are planned.