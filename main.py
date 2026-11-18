import requests

from src.tafe.auth import get_access_token


GRAPH_URL = "https://graph.microsoft.com/v1.0"


def get_onedrive_files():
    """Retrieve files from the signed-in user's OneDrive root."""

    token = get_access_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    # Select only the fields needed by this application.
    url = (
        f"{GRAPH_URL}/me/drive/root/children"
        "?$select=id,name,size,webUrl,lastModifiedDateTime,file,folder"
        "&$top=100"
    )

    all_files = []

    while url:
        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        if response.status_code == 401:
            raise RuntimeError(
                "Microsoft Graph rejected the access token. "
                "Reconnect the Microsoft account."
            )

        response.raise_for_status()

        data = response.json()

        all_files.extend(data.get("value", []))

        # Graph returns this when another page is available.
        url = data.get("@odata.nextLink")

    return all_files


def display_files(files):
    """Print the retrieved OneDrive files."""

    if not files:
        print("No files found in the OneDrive root.")
        return

    print(f"\nFound {len(files)} items:\n")

    for item in files:
        item_type = "Folder" if "folder" in item else "File"

        print(f"Name: {item.get('name')}")
        print(f"Type: {item_type}")
        print(f"ID: {item.get('id')}")
        print(f"Size: {item.get('size', 0)} bytes")
        print(f"Modified: {item.get('lastModifiedDateTime')}")
        print(f"URL: {item.get('webUrl')}")
        print("-" * 50)


if __name__ == "__main__":
    try:
        files = get_onedrive_files()
        display_files(files)

    except Exception as error:
        print(f"Error: {error}")