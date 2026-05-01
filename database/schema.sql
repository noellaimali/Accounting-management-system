CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    account_type TEXT NOT NULL,
    balance REAL DEFAULT 0.0
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS journal_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id INTEGER NOT NULL,
    account_id INTEGER NOT NULL,
    debit REAL DEFAULT 0.0,
    credit REAL DEFAULT 0.0,
    FOREIGN KEY(transaction_id) REFERENCES transactions(id),
    FOREIGN KEY(account_id) REFERENCES accounts(id)
);

-- Insert some default accounts for demonstration
INSERT INTO accounts (name, account_type) VALUES 
('Cash', 'Asset'),
('Accounts Receivable', 'Asset'),
('Inventory', 'Asset'),
('Accounts Payable', 'Liability'),
('Sales Revenue', 'Revenue'),
('Cost of Goods Sold', 'Expense'),
('Salary Expense', 'Expense');
