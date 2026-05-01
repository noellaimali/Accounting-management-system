-- View all accounts
SELECT * FROM accounts;

-- View all transactions with entries
SELECT 
    t.date, 
    t.description, 
    a.name AS account_name, 
    je.debit, 
    je.credit
FROM transactions t
JOIN journal_entries je ON t.id = je.transaction_id
JOIN accounts a ON je.account_id = a.id
ORDER BY t.date DESC;

-- Calculate Total Trial Balance
SELECT 
    SUM(debit) AS total_debits, 
    SUM(credit) AS total_credits 
FROM journal_entries;

-- Calculate Account Balances
SELECT 
    a.name, 
    a.account_type, 
    SUM(je.debit) - SUM(je.credit) AS balance
FROM accounts a
LEFT JOIN journal_entries je ON a.id = je.account_id
GROUP BY a.id, a.name, a.account_type;
