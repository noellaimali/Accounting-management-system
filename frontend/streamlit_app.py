import streamlit as st
import requests
import pandas as pd
from datetime import date
import os
import base64

API_URL = "http://localhost:8000/api"

st.set_page_config(page_title="Accounting System", page_icon="💰", layout="wide")

# Add background image
img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'accounting-inscription-coming-out-from-an-open-book-business-concept-2A15NHB.jpg')
try:
    with open(img_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpeg;base64,{encoded_string});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        /* Add a semi-transparent dark overlay to main container so the text remains readable! */
        .block-container {{
            background-color: rgba(14, 17, 23, 0.85);
            padding: 3rem;
            border-radius: 15px;
            margin-top: 2rem;
            margin-bottom: 2rem;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
except Exception as e:
    pass

st.title("Double-Entry Accounting System 📊")

# Ensure API is reachable
try:
    accounts_resp = requests.get(f"{API_URL}/accounts")
    accounts_resp.raise_for_status()
    accounts = accounts_resp.json()
except Exception as e:
    st.error("Backend API is not running. Please start the backend server to continue.")
    st.info("Run `python -m uvicorn backend.app:app` in your terminal.")
    st.stop()

tab1, tab2, tab3 = st.tabs(["Dashboard", "Add Transaction", "Journal Entries"])

with tab1:
    st.header("Dashboard 📈")
    df_accounts = pd.DataFrame(accounts)
    if not df_accounts.empty:
        df_accounts = df_accounts[['id', 'name', 'account_type', 'balance']]
        
        col1, col2 = st.columns(2)
        total_assets = df_accounts[df_accounts['account_type'] == 'Asset']['balance'].sum()
        total_liabilities = df_accounts[df_accounts['account_type'] == 'Liability']['balance'].sum()
        
        col1.metric("Total Assets", f"${total_assets:,.2f}")
        col2.metric("Total Liabilities", f"${total_liabilities:,.2f}")
        
        st.divider()
        st.subheader("📊 Account Balances")
        # Equivalent to the balance summation SQL query Visualization
        chart_df = df_accounts[['name', 'balance']].sort_values('balance', ascending=True)
        st.bar_chart(chart_df.set_index("name"))
        
        # Transactions Over Time Visualization 
        try:
            journal_resp = requests.get(f"{API_URL}/journal")
            if journal_resp.status_code == 200:
                journal = journal_resp.json()
                df_journal = pd.DataFrame(journal)
                
                if not df_journal.empty:
                    st.divider()
                    st.subheader("📈 Transactions by Month")
                    # Equivalent to DATE_TRUNC total transactions grouping SQL query
                    df_unique_trans = df_journal[['date', 'description']].drop_duplicates()
                    df_unique_trans['month'] = pd.to_datetime(df_unique_trans['date']).dt.to_period('M').astype(str)
                    trans_by_month = df_unique_trans.groupby('month').size().reset_index(name='total_transactions')
                    
                    st.bar_chart(trans_by_month.set_index('month'))
        except Exception as e:
            pass

        st.divider()
        st.subheader("Chart of Accounts Data")
        st.dataframe(df_accounts, use_container_width=True)
        
    else:
        st.info("No accounts found.")

with tab2:
    st.header("Add New Transaction")
    
    with st.form("transaction_form", clear_on_submit=True):
        col1, col2 = st.columns([1, 2])
        with col1:
            trans_date = st.date_input("Date", value=date.today())
        with col2:
            description = st.text_input("Description", placeholder="e.g., Sold goods for cash")
            
        st.divider()
        st.subheader("Journal Entries")
        
        account_names = {acc['id']: f"{acc['name']} ({acc['account_type']})" for acc in accounts}
        acc_options = list(account_names.keys())
        
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            acc1 = st.selectbox("Account 1", options=acc_options, format_func=lambda x: account_names[x], key="acc1")
        with c2:
            debit1 = st.number_input("Debit 1", min_value=0.0, step=0.01, key="db1")
        with c3:
            credit1 = st.number_input("Credit 1", min_value=0.0, step=0.01, key="cr1")
            
        c4, c5, c6 = st.columns([2, 1, 1])
        with c4:
            acc2 = st.selectbox("Account 2", options=acc_options, format_func=lambda x: account_names[x], index=1 if len(acc_options)>1 else 0, key="acc2")
        with c5:
            debit2 = st.number_input("Debit 2", min_value=0.0, step=0.01, key="db2")
        with c6:
            credit2 = st.number_input("Credit 2", min_value=0.0, step=0.01, key="cr2")

        submitted = st.form_submit_button("Submit Transaction", type="primary")
        
        if submitted:
            total_debits = round(debit1 + debit2, 2)
            total_credits = round(credit1 + credit2, 2)
            
            if total_debits == 0 and total_credits == 0:
                st.error("Please enter numbers for debit or credit.")
            elif total_debits != total_credits:
                st.error(f"Debits (${total_debits}) must equal Credits (${total_credits}).")
            else:
                entries = []
                if debit1 > 0 or credit1 > 0:
                    entries.append({"account_id": acc1, "debit": debit1, "credit": credit1})
                if debit2 > 0 or credit2 > 0:
                    entries.append({"account_id": acc2, "debit": debit2, "credit": credit2})
                    
                payload = {
                    "date": str(trans_date),
                    "description": description,
                    "entries": entries
                }
                
                res = requests.post(f"{API_URL}/transactions", json=payload)
                if res.status_code == 200:
                    st.success("Transaction added successfully!")
                else:
                    st.error(f"Error adding transaction: {res.text}")

with tab3:
    st.header("Journal Entries")
    if st.button("Refresh Journal 🔄"):
        pass # Streamlit handles re-running natively
        
    try:
        journal_resp = requests.get(f"{API_URL}/journal")
        journal_resp.raise_for_status()
        journal = journal_resp.json()
        
        df_journal = pd.DataFrame(journal)
        if not df_journal.empty:
            st.dataframe(df_journal, use_container_width=True)
            
            # Show total trial balance
            tot_debit = df_journal['debit'].sum()
            tot_credit = df_journal['credit'].sum()
            
            st.divider()
            st.write(f"### Trial Balance Totals: 🔵 Debit: ${tot_debit:,.2f} | 🟢 Credit: ${tot_credit:,.2f}")
            if round(tot_debit, 2) == round(tot_credit, 2):
                st.success("Books are balanced! ✓")
            else:
                st.error("Books are unbalanced through manual intervention! ✗")
        else:
            st.info("No journal entries found.")
    except Exception as e:
        st.error("Failed to load journal.")
