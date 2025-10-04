# Google Sheets CRUD API

This project is a Python-based REST API that uses a Google Sheet as its database. It provides complete CRUD (Create, Read, Update, Delete) functionality for two main resources: `Colaboradores` (Collaborators) and `Servicos` (Services).

The API is built using the **FastAPI** framework.

## Features

*   **Colaborador Management:**
    *   Create, read, update, and delete collaborators.
    *   Fields: `id`, `nome`, `cpf`, `chavePix`, `dataInicio`, `dataFim`
*   **Serviço Management:**
    *   Create, read, update, and delete services.
    *   Fields: `id`, `tipoServico`, `valor`, `dataInicio`, `dataFim`
*   **Google Sheets Integration:** All data is stored and retrieved from a designated Google Sheet, with separate worksheets for collaborators and services.
*   **Automatic Documentation:** Interactive API documentation is available at `/docs` and `/redoc`.

## Setup Instructions

Follow these steps to get the application running locally.

### 1. Google Cloud & Sheets Configuration

To connect the API to your Google Sheet, you need to authenticate using a service account.

1.  **Enable APIs:** Go to the [Google Cloud Console](https://console.cloud.google.com/) and enable the **Google Sheets API** and **Google Drive API** for your project.
2.  **Create a Service Account:**
    *   Navigate to "IAM & Admin" > "Service Accounts".
    *   Click "Create Service Account".
    *   Give it a name and description, then click "Create and Continue".
    *   Grant it the "Editor" role to allow it to read and write to your sheet, then click "Done".
3.  **Generate a JSON Key:**
    *   Find the service account you just created, click the three-dot menu under "Actions", and select "Manage keys".
    *   Click "Add Key" > "Create new key".
    *   Choose **JSON** as the key type and click "Create". A JSON file will be downloaded.
4.  **Rename and Place the Key:** Rename the downloaded file to `credentials.json` and place it in the root directory of this project.
5.  **Create and Share a Google Sheet:**
    *   Create a new Google Sheet where you want to store your data.
    *   Open your `credentials.json` file and find the `client_email` address (e.g., `my-service-account@...iam.gserviceaccount.com`).
    *   Click the "Share" button in your Google Sheet and share it with this `client_email`, giving it **Editor** permissions.

### 2. Environment Variables

Create a file named `.env` in the root directory of the project and add the name of your Google Sheet:

```env
SPREADSHEET_NAME="Your Google Sheet Name Here"
```

### 3. Install Dependencies

It is recommended to use a virtual environment. Once your environment is active, install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Application

To start the API server, run the following command from the project's root directory:

```bash
uvicorn app.main:app --reload
```

The server will be available at `http://127.0.0.1:8000`.

## API Usage

Once the server is running, you can access the interactive API documentation at:

*   **Swagger UI:** `http://127.0.0.1:8000/docs`
*   **ReDoc:** `http://127.0.0.1:8000/redoc`

These interfaces allow you to explore and test all the available API endpoints for `colaboradores` and `servicos`.