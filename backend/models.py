import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'accounting.db')
SCHEMA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'schema.sql')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        with open(SCHEMA_FILE, 'r') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()

def get_accounts():
    conn = get_db_connection()
    accounts = conn.execute('SELECT * FROM accounts').fetchall()
    conn.close()
    return [dict(ix) for ix in accounts]

def add_transaction(date, description, entries):
    """
    entries is a list of dicts: [{'account_id': int, 'debit': float, 'credit': float}]
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO transactions (date, description) VALUES (?, ?)', (date, description))
        transaction_id = cursor.lastrowid
        
        for entry in entries:
            cursor.execute(
                'INSERT INTO journal_entries (transaction_id, account_id, debit, credit) VALUES (?, ?, ?, ?)',
                (transaction_id, entry['account_id'], entry.get('debit', 0.0), entry.get('credit', 0.0))
            )
            
            # Update account balance logic
            account = cursor.execute('SELECT account_type FROM accounts WHERE id = ?', (entry['account_id'],)).fetchone()
            if account['account_type'] in ['Asset', 'Expense']:
                balance_change = entry.get('debit', 0.0) - entry.get('credit', 0.0)
            else:
                balance_change = entry.get('credit', 0.0) - entry.get('debit', 0.0)
                
            cursor.execute('UPDATE accounts SET balance = balance + ? WHERE id = ?', (balance_change, entry['account_id']))
            
        conn.commit()
        return True, "Transaction added successfully."
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def get_journal():
    conn = get_db_connection()
    query = """
    SELECT 
        t.date, 
        t.description, 
        a.name AS account_name, 
        je.debit, 
        je.credit
    FROM transactions t
    JOIN journal_entries je ON t.id = je.transaction_id
    JOIN accounts a ON je.account_id = a.id
    ORDER BY t.date DESC, t.id DESC
    """
    journal = conn.execute(query).fetchall()
    conn.close()
    return [dict(ix) for ix in journal]
