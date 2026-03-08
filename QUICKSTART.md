# Quick Start Guide

This guide helps you get the Python Banking System up and running in minutes.

---

## ⚡ Quick Installation

```bash
# Clone repository
git clone https://github.com/elnamaky2004/banking_program.git
cd banking_program

# Setup Python environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Running the Applications

### User App (Customer Portal)
```bash
cd user_app
python app.py
```

**Features:**
- Sign up with new account
- Login to existing account
- Transfer money (< 5000: instant, > 5000: requires approval)
- Request loans
- View account information
- Update profile
- Theme toggle (light/dark)

### Worker App (Admin Portal)
```bash
cd worker_app
python app.py
```

**Test Login Credentials:**
- Manager: `tarek.soliman@bank.com` / `TSadmin99` (full access)
- Admin: `osama.elnamki@bank.com` / `12345678`
- Teller: `mohamed.khaled@bank.com` / `MK2024`
- Auditor: `nour.ibrahim@bank.com` / `NourPass1`

**Features (based on permissions):**
- Manage Users (approve/revoke accounts)
- Approve Loans
- Approve Transactions (> 5000 EGP)
- Transaction Management (deposit/withdraw/transfer)
- Audit Transactions
- View Reports
- System Logs

---

##  Project Structure

```
banking_program/
├── user_app/           # Customer-facing application
│   ├── app.py         # Login window (START HERE)
│   ├── sign_up.py     # Registration
│   └── ...
│
├── worker_app/         # Administrative backend
│   ├── app.py         # Worker login (START HERE)
│   ├── worker_signed_in.py  # Dashboard
│   └── ...
│
├── README.md          # Full documentation
├── CONTRIBUTING.md    # Contribution guidelines
├── CHANGELOG.md       # Version history
└── requirements.txt   # Dependencies
```

---

## 🎨 Theme System

Both apps support **Light** and **Dark** modes:
- Toggle available on every window (top-right)
- Uses QDarkStyleSheet for professional dark theme
- Themes sync globally across all windows

---

## 🔑 Key Workflows

### 1. User Registration
```
Sign Up → Enter Details → Account Created (unverified)
→ Worker Approves → Account Verified → Login Enabled
```

### 2. Transfer Money (High Value)
```
User: Transfer > 5000 EGP → Saved to approval_requests.json
Worker: Review in "Approve Transactions" → Approve → Funds Transferred
```

### 3. Loan Request
```
User: Request Loan → Enter Amount/Purpose/Period → Confirm Password
→ Saved to loan_requests.json
Worker: Review in "Approve Loans" → Approve/Reject
```

---

## 🛠 Common Tasks

### Add a New Worker
Edit `worker_app/worker.json`:
```json
{
  "new.worker@bank.com": {
    "password": "password123",
    "full_name": "New Worker",
    "role": "Teller",
    "employee_id": "EMP006",
    "department": "Operations",
    "permissions": ["deposit", "withdraw"]
  }
}
```

### Grant Permissions
Available permissions:
- `full_access` - Manager/Director (all features)
- `manage_users` - User verification
- `approve_loans` - Loan approvals
- `approve_transactions` - Transfer approvals (> 5000)
- `deposit`, `withdraw`, `transfer` - Transaction management
- `audit_transactions` - Audit functionality
- `view_reports` - Analytics
- `view_logs` - System logs
- `manage_staff` - Staff management

See [`worker_app/PERMISSIONS_GUIDE.md`](worker_app/PERMISSIONS_GUIDE.md) for details.

---

## 🐛 Troubleshooting

### Issue: "No module named PyQt5"
```bash
pip install -r requirements.txt
```

### Issue: "No module named qdarkstyle"
```bash
pip install qdarkstyle
```

### Issue: Cannot login to worker app
- Check credentials in `worker_app/worker.json`
- Default test account: `osama.elnamki@bank.com` / `12345678`

### Issue: Transfer not appearing for approval
- Check amount is > 5000 EGP
- Verify `approval_requests.json` exists in worker_app
- Refresh "Approve Transactions" window

---

## 📚 Additional Resources

- **Full Documentation**: [`README.md`](README.md)
- **Contributing**: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- **Change Log**: [`CHANGELOG.md`](CHANGELOG.md)
- **Worker Permissions**: [`worker_app/PERMISSIONS_GUIDE.md`](worker_app/PERMISSIONS_GUIDE.md)

---

## 🆘 Getting Help

- **Issues**: https://github.com/elnamaky2004/banking_program/issues
- **LinkedIn**: https://www.linkedin.com/in/osama-elnamaky-55a11324a/
- **Email**: osamaalnamky@gmail.com

---

## 🎯 Next Steps

1. ✅ Run both apps to explore features
2. ✅ Try user registration flow
3. ✅ Test transfer approval workflow
4. ✅ Explore worker permission system
5. ✅ Read full documentation
6. ✅ Consider contributing!

---

**Happy Banking!** 🏦
