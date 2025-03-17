import googleapiclient.discovery
import google.oauth2.credentials
from flask import session

def get_sheets_service():
    """Initialize Google Sheets API service for the logged-in user."""
    credentials = google.oauth2.credentials.Credentials(**session["credentials"])
    return googleapiclient.discovery.build("sheets", "v4", credentials=credentials)

def get_or_create_user_sheet(email):
    """Find or create a Google Sheet for the user."""
    service = get_sheets_service()
    spreadsheet_title = f"My Wealth Manager - {email}"

    # Check if user already has a sheet
    drive_service = googleapiclient.discovery.build("drive", "v3", credentials=service._http.credentials)
    query = f"name='{spreadsheet_title}' and mimeType='application/vnd.google-apps.spreadsheet'"
    response = drive_service.files().list(q=query).execute()
    files = response.get("files", [])

    if files:
        return files[0]["id"]

    # Create a new sheet if not found
    spreadsheet = {"properties": {"title": spreadsheet_title}}
    sheet = service.spreadsheets().create(body=spreadsheet).execute()
    return sheet["spreadsheetId"]

def add_transaction(sheet_id, data):
    """Append transaction data to user's Google Sheet."""
    service = get_sheets_service()
    values = [[data["date"], data["fund_name"], data["amount"], data["units"]]]
    body = {"values": values}

    service.spreadsheets().values().append(
        spreadsheetId=sheet_id, range="Transactions!A:D",
        valueInputOption="RAW", body=body).execute()

def get_transactions(sheet_id):
    """Fetch transactions from the user's Google Sheet."""
    service = get_sheets_service()
    result = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="Transactions!A:D").execute()
    return result.get("values", [])
