# Worker App - Permission System Documentation

## Overview
The worker app now uses a comprehensive role-based permission system where buttons are displayed based on each worker's permissions.

## Permission Levels

### Manager/Director (Full Access)
Workers with `"full_access"` permission see ALL buttons:
- Manage Users
- Verify Accounts  
- Approve Loans
- Approve Transactions
- View Reports
- Transaction Management
- Audit Transactions
- View System Logs
- Staff Management

**Example Manager:** Tarek Soliman (tarek.soliman@bank.com)

### Other Roles
Workers see only buttons matching their specific permissions:

#### System Administrator
Permissions: `["system_admin", "manage_users", "view_logs"]`
Sees: Manage Users, Verify Accounts, View System Logs

#### Branch Manager
Permissions: `["approve_loans", "approve_transactions", "view_reports", "manage_staff"]`
Sees: Approve Loans, Approve Transactions, View Reports, Staff Management

#### Senior Teller
Permissions: `["deposit", "withdraw", "transfer"]`
Sees: Transaction Management

#### Internal Auditor
Permissions: `["view_reports", "audit_transactions"]`
Sees: View Reports, Audit Transactions

#### Loan Officer
Permissions: `["review_loans", "approve_small_loans"]`
Sees: (Limited functionality - future expansion)

## Available Modules

### 1. Manage Users (`manage_users.py`)
- Verify/revoke user accounts
- View pending verifications
- Required permission: `manage_users`

### 2. Approve Loans (`approve_loans.py`)
- Approve or reject loan requests
- View pending loan applications
- Required permission: `approve_loans`

### 3. Approve Transactions (`approve_transactions.py`)
- Approve or reject high-value transfer requests (> 5000 EGP)
- Process approved transfers
- View pending transaction approvals
- Required permission: `approve_transactions`

### 4. View Reports (`view_reports.py`)
- Generate various financial reports
- User statistics, transaction summaries, loan overviews
- Required permission: `view_reports`

### 5. Manage Transactions (`manage_transactions.py`)
- Process deposits, withdrawals, transfers
- Direct account management
- Required permission: `deposit` (or withdraw/transfer)

### 6. Audit Transactions (`audit_transactions.py`)
- Search and audit user accounts
- Generate full audit reports
- Required permission: `audit_transactions`

### 7. View System Logs (`view_logs.py`)
- View system activity logs
- Clear logs (admin only)
- Required permission: `view_logs`

## How to Add New Permissions

1. Add permission to worker in `worker.json`:
```json
"permissions": ["new_permission", "existing_permission"]
```

2. Add button in `worker_signed_in.py` button_configs:
```python
("Button Text", "new_permission", self._callback_method)
```

3. Create the callback method and module window

## Testing Different Roles

Login credentials (all in `worker.json`):
- Manager: `tarek.soliman@bank.com` / `TSadmin99`
- Admin: `osama.elnamki@bank.com` / `12345678`
- Teller: `mohamed.khaled@bank.com` / `MK2024`
- Auditor: `nour.ibrahim@bank.com` / `NourPass1`

Each role will see different buttons based on their permissions!
