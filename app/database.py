import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv

load_dotenv()

# INSTRUCTIONS FOR THE USER:
# 1. Enable the Google Sheets API and Google Drive API in your Google Cloud Platform project.
# 2. Create a service account and download the JSON key file.
# 3. Rename the JSON key file to `credentials.json` and place it in the root of this project.
# 4. Create a new Google Sheet.
# 5. Share the Google Sheet with the `client_email` found in your `credentials.json` file, giving it "Editor" permissions.
# 6. Create a `.env` file in the root of the project and add the following line:
#    SPREADSHEET_NAME="Your Google Sheet Name"

SCOPE = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
CREDS_FILE = "credentials.json"
SPREADSHEET_NAME = os.getenv("SPREADSHEET_NAME")

def get_creds():
    """Authenticates with Google Sheets API using service account credentials."""
    if not os.path.exists(CREDS_FILE):
        raise FileNotFoundError(
            "The `credentials.json` file was not found. "
            "Please follow the setup instructions in `database.py`."
        )
    return ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)

def get_client():
    """Returns an authorized gspread client."""
    creds = get_creds()
    return gspread.authorize(creds)

def get_spreadsheet():
    """Returns the spreadsheet instance."""
    client = get_client()
    try:
        return client.open(SPREADSHEET_NAME)
    except gspread.exceptions.SpreadsheetNotFound:
        raise ValueError(
            f"Spreadsheet '{SPREADSHEET_NAME}' not found. "
            "Please check the SPREADSHEET_NAME in your `.env` file and ensure you have shared it with the service account."
        )

def get_colaboradores_sheet():
    """Returns the 'Colaboradores' worksheet, creating it if it doesn't exist."""
    spreadsheet = get_spreadsheet()
    try:
        return spreadsheet.worksheet("Colaboradores")
    except gspread.exceptions.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title="Colaboradores", rows="100", cols="20")
        worksheet.append_row(["id", "nome", "cpf", "chavePix", "percentualComissao", "dataInicio", "dataFim"])
        return worksheet

def get_servicos_sheet():
    """Returns the 'Servicos' worksheet, creating it if it doesn't exist."""
    spreadsheet = get_spreadsheet()
    try:
        return spreadsheet.worksheet("Servicos")
    except gspread.exceptions.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title="Servicos", rows="100", cols="20")
        worksheet.append_row(["id", "tipoServico", "valor", "dataInicio", "dataFim"])
        return worksheet