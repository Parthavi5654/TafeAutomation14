import os
import msal

from pathlib import Path
from dotenv import load_dotenv


# --------------------------------------------------
# Environment configuration
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")

CLIENT_ID = os.getenv("CLIENT_ID")
TENANT_ID = os.getenv("TENANT_ID", "organizations")

if not CLIENT_ID:
    raise RuntimeError("CLIENT_ID is missing from your .env file.")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

# Delegated permission for listing the signed-in user's files.
SCOPES = ["Files.Read"]

# Local development cache only.
# Production: store a separate encrypted cache per customer in a database.
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

CACHE_FILE = DATA_DIR / "token_cache.json"

# Optional: set this if you want to select a particular account
# when multiple accounts exist in the cache.
ACCOUNT_USERNAME = os.getenv("ACCOUNT_USERNAME")


# --------------------------------------------------
# Token cache
# --------------------------------------------------

cache = msal.SerializableTokenCache()


def load_token_cache():
    """Load the local MSAL cache."""

    if CACHE_FILE.exists():
        cache.deserialize(CACHE_FILE.read_text(encoding="utf-8"))


def save_token_cache():
    """Persist the cache when MSAL has changed it."""

    if cache.has_state_changed:
        temp_file = CACHE_FILE.with_suffix(".tmp")

        temp_file.write_text(
            cache.serialize(),
            encoding="utf-8"
        )

        # Replace atomically rather than writing directly over the cache.
        temp_file.replace(CACHE_FILE)

        try:
            os.chmod(CACHE_FILE, 0o600)
        except OSError:
            # Windows may not support Unix-style permissions.
            pass


load_token_cache()


# --------------------------------------------------
# MSAL application
# --------------------------------------------------

app = msal.PublicClientApplication(
    client_id=CLIENT_ID,
    authority=AUTHORITY,
    token_cache=cache
)


# --------------------------------------------------
# Account selection
# --------------------------------------------------

def get_selected_account():
    """
    Find the account in the cache.

    For this local prototype:
    - If ACCOUNT_USERNAME is configured, match that account.
    - If only one account exists, use it.
    - If multiple accounts exist, require an explicit username.
    """
    print("Checking for cached Microsoft accounts...")
    accounts = app.get_accounts()

    if not accounts:
        return None

    if ACCOUNT_USERNAME:
        for account in accounts:
            if account.get("username", "").lower() == ACCOUNT_USERNAME.lower():
                return account

        return None

    if len(accounts) == 1:
        return accounts[0]

    raise RuntimeError(
        "Multiple Microsoft accounts are cached. "
        "Set ACCOUNT_USERNAME in .env to select the correct account."
    )


# --------------------------------------------------
# Interactive login
# --------------------------------------------------

def login_device_flow():
    """
    Run this manually when connecting an account for the first time,
    or when the customer needs to reconnect.

    Do not call this automatically from a scheduled background job.
    """

    flow = app.initiate_device_flow(scopes=SCOPES)

    if "user_code" not in flow:
        raise RuntimeError(
            f"Unable to start device login: {flow}"
        )

    print("\nMicrosoft account login required.")
    print(flow["message"])

    result = app.acquire_token_by_device_flow(flow)

    save_token_cache()

    if "access_token" not in result:
        raise RuntimeError(
            result.get("error_description", str(result))
        )

    account = get_selected_account()

    print("\nAuthentication successful.")

    if account:
        print("Connected account:", account.get("username"))

    return result["access_token"]


# --------------------------------------------------
# Silent token acquisition
# --------------------------------------------------

def get_access_token():
    """
    Obtain an access token without user interaction.

    This function is suitable for normal API calls and,
    after the architecture is upgraded, scheduled jobs.
    """
    
    account = get_selected_account()

    if not account:
        raise RuntimeError(
            "No connected Microsoft account found. "
            "Run login_device_flow() first."
        )

    result = app.acquire_token_silent(
        scopes=SCOPES,
        account=account
    )

    save_token_cache()

    if not result or "access_token" not in result:
        error = result.get("error") if result else "no_cached_token"
        description = (
            result.get("error_description")
            if result else "MSAL could not obtain a token silently."
        )

        raise RuntimeError(
            f"Microsoft authentication needs attention: "
            f"{error}: {description}. "
            f"Reconnect the Microsoft account."
        )

    return result["access_token"]


# --------------------------------------------------
# Disconnect account
# --------------------------------------------------

def logout():
    """Remove cached account tokens for this local prototype."""

    accounts = app.get_accounts()

    for account in accounts:
        app.remove_account(account)

    save_token_cache()

    if CACHE_FILE.exists():
        CACHE_FILE.unlink()

    print("Local Microsoft account cache cleared.")


# --------------------------------------------------
# Manual authentication test
# --------------------------------------------------

if __name__ == "__main__":
    login_device_flow()