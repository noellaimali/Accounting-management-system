# Accounting System

A simple double-entry accounting system with a FastAPI backend and a Streamlit frontend. It allows users to register journal entries dynamically, computes total balances, and interacts seamlessly through a sleek local dashboard.

## Project Structure
```text
accounting-system/
│
├── backend/                  # FastAPI backend
│   ├── app.py                # Main app entry point
│   ├── models.py             # Database access and logic
│   ├── routes.py             # API endpoints
│
├── database/                 # Database scripts
│   ├── schema.sql            # Table definitions
│   ├── queries.sql           # Helpful SQL queries
│
├── frontend/                 # Streamlit UI
│   ├── streamlit_app.py      # Main frontend logic
│
└── README.md                 # Project documentation
```

## Setup Instructions

### Prerequisites
1. Python 3.8+
2. Install the necessary pip packages by running:
   ```bash
   pip install fastapi uvicorn requests pandas streamlit
   ```

### Running the Application
The application is split into a backend API and a frontend UI. *Both need to be running simultaneously to work perfectly.*

**1. Start the Backend API**
Open a terminal in the root of the project (`accounting-system`) and run:
```bash
python -m uvicorn backend.app:app --reload
```
The API will be available at `http://localhost:8000`. The SQLite database will be created automatically in the root folder on the first run.

**2. Start the Frontend UI**
Open a separate terminal in the root of the project and run:
```bash
streamlit run frontend/streamlit_app.py
```
This will open the Streamlit web application in your browser (usually at `http://localhost:8501`).

## Using the System
- **Dashboard:** View the chart of accounts and their current balances. Check your Assets and Liabilities.
- **Add Transaction:** Create double-entry journal entries. Ensure total debits equal total credits.
- **Journal Entries:** View all historical transactions and confirm that your general ledger is balanced.

## Database
The system uses `sqlite3`.
The files under `database/` store your SQL schemas and standard queries. They are used internally by `models.py` to initialize the database if it doesn't already exist. You can run `queries.sql` in any SQLite client to directly query your database.
