# 🏦 Python Banking System

A comprehensive desktop banking application with **User** and **Worker** portals built with **Python** and **PyQt5**. Features include secure authentication, transaction management, loan requests, approval workflows, and a complete administrative backend.

> **Quick Start**: See [`QUICKSTART.md`](QUICKSTART.md) for a rapid setup guide.

---

## 🚀 Features

### 👤 User Portal (`user_app/`)

#### Authentication & Security
- **User Registration** with account creation
- **Secure Login** with password encryption
- **Account Verification** by workers before activation

#### Banking Operations
- **Transfer Money**
  - Instant transfers for amounts ≤ 5000 EGP
  - Approval-required transfers for amounts > 5000 EGP
  - Real-time balance validation
- **Account Information** dashboard with balance display
- **Update Profile** (username and password changes)
- **Request Loans**
  - Specify loan amount, purpose, and repayment period
  - Password confirmation required
  - Submitted to worker approval queue

#### User Experience
- **Global Theme System** (Light/Dark mode with animated toggle)
- **About Page** with external links
- **Responsive UI** with consistent styling across all windows

---

### 👨‍💼 Worker Portal (`worker_app/`)

#### Role-Based Access Control
- **Permission System** with granular access controls
- **Manager/Director** role with full access
- **Specialized Roles**: System Admin, Branch Manager, Teller, Auditor, Loan Officer
- See [`PERMISSIONS_GUIDE.md`](worker_app/PERMISSIONS_GUIDE.md) for details

#### Administrative Features

**User Management** (`manage_users.py`)
- View pending user verifications
- Approve or revoke user accounts
- Batch processing capabilities

**Loan Approvals** (`approve_loans.py`)
- Review loan requests from users
- Approve or reject with worker tracking
- View amount, purpose, and repayment terms

**Transaction Approvals** (`approve_transactions.py`)
- Review high-value transfer requests (> 5000 EGP)
- Approve: Validates funds and executes transfer
- Reject: Updates status without processing
- Full sender/recipient details

**Transaction Management** (`manage_transactions.py`)
- Direct deposits, withdrawals, and transfers
- Worker-initiated account operations
- Immediate processing for authorized personnel

**Audit Transactions** (`audit_transactions.py`)
- Search users by email or name
- Generate full audit reports
- Export transaction histories

**View Reports** (`view_reports.py`)
- User statistics and analytics
- Transaction summaries
- Loan overview reports

**System Logs** (`view_logs.py`)
- View all system activities
- Clear logs (admin only)
- Timestamp tracking

#### Worker Experience
- **Unified Theme System** (QDarkStyleSheet integration)
- **Permission-based UI** (buttons show/hide based on role)
- **Dashboard Overview** with role, employee ID, and department info

---

## 🛠 Tech Stack

- **Python 3.11.9** (via pyenv)
- **PyQt5** - Desktop GUI framework
- **QDarkStyleSheet** - Professional dark theme
- **JSON** - Persistent data storage
- **Git & GitHub** - Version control

---

## 📦 Project Structure

```
banking_program/
├── README.md
├── .gitignore
│
├── user_app/                    # User-facing application
│   ├── app.py                  # User login window
│   ├── sign_up.py              # Registration form

│   ├── signed_in_window.py     # User dashboard
│   ├── transfer_money.py       # Money transfer + approval workflow
│   ├── account_information.py  # Account details view
│   ├── update_info.py          # Profile update
│   ├── request_loan.py         # Loan request form
│   ├── loan_calculator.py      # Loan calculation utilities
│   ├── about_app.py            # About page
│   ├── theme.py                # Theme system (QDarkStyleSheet)
│   └── users.json              # User database (gitignored)
│
└── worker_app/                  # Worker administration portal
    ├── app.py                  # Worker login window
    ├── worker_signed_in.py     # Worker dashboard
    ├── manage_users.py         # User verification & management
    ├── approve_loans.py        # Loan approval interface
    ├── approve_transactions.py # Transaction approval (> 5000)
    ├── manage_transactions.py  # Direct transaction operations
    ├── audit_transactions.py   # Audit & search functionality
    ├── view_reports.py         # Analytics and reporting
    ├── view_logs.py            # System logs viewer
    ├── theme.py                # Theme system (QDarkStyleSheet)
    ├── PERMISSIONS_GUIDE.md    # Role & permission documentation
    ├── worker.json             # Worker accounts (gitignored)
    ├── approval_requests.json  # Pending transfer approvals (gitignored)
    ├── loan_requests.json      # Pending loan requests (gitignored)
    ├── system_logs.json        # Activity logs (gitignored)
    └── transfer_requests.json  # Transfer history (gitignored)
```

---

## 🎨 Theme System

Both applications feature a **synchronized global theme system**:

### Dark Mode
- Uses **QDarkStyleSheet** library for professional styling
- Custom overrides for labels, buttons, and primary actions
- Smooth toggle animation with `AnimatedToggleSwitch` widget

### Light Mode
- Clean, modern design with high contrast
- Consistent color palette across all windows
- Optimized for readability

**Toggle**: Available on every window via animated switch in the header

---

## 🔐 Security Features

1. **Password Hashing** (planned: bcrypt/scrypt)
2. **Worker Verification** required before account activation
3. **Role-Based Access Control** for workers
4. **High-Value Transaction Approval** (> 5000 EGP)
5. **Password Confirmation** for sensitive operations
6. **Session Management** (in development)

---

## 🚦 Workflows

### User Registration Flow
1. User enters email, password, name, title, and account details
2. Account created with `is_verified: false` status
3. Worker reviews and approves account
4. User gains full access

### Transfer Money Flow (> 5000 EGP)
1. User initiates transfer
2. System detects amount > 5000
3. Request saved to `approval_requests.json`
4. Worker reviews in "Approve Transactions" module
5. Worker approves → funds transferred
6. Worker rejects → status updated, no transfer

### Loan Request Flow
1. User submits loan request with amount, purpose, period
2. Request saved to `loan_requests.json`
3. Worker reviews in "Approve Loans" module
4. Worker approves/rejects with tracking
5. (Future: Automatic fund disbursement)

---

## 📌 Version

**v2.0.0** - Major Update
- Added Worker Portal with role-based permissions
- Implemented transaction approval workflow
- Added loan request system
- Integrated QDarkStyleSheet
- Reorganized project structure

---

## 🔮 Future Improvements

### Planned Features
- [ ] Database migration (SQLite/PostgreSQL)
- [ ] Password hashing (bcrypt)
- [ ] Transaction history export (PDF/CSV)
- [ ] Email notifications for approvals
- [ ] Two-factor authentication (2FA)
- [ ] Mobile-responsive web version
- [ ] Real-time balance updates
- [ ] Loan repayment tracking
- [ ] Interest calculation automation
- [ ] Multi-currency support improvements
- [ ] Backup and restore functionality

### Technical Debt
- [ ] Refactor JSON storage to database
- [ ] Implement proper logging framework
- [ ] Add unit tests (pytest)
- [ ] CI/CD pipeline setup
- [ ] API documentation
- [ ] Input sanitization improvements

---

## 🛠 Setup & Installation

### Prerequisites
- Python 3.11.9 (recommended via pyenv)
- pip package manager

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/elnamaky2004/banking_program.git
cd banking_program
```

2. **Set up Python environment**
```bash
# Using pyenv (recommended)
pyenv install 3.11.9
pyenv local 3.11.9

# Or use your system Python 3.11+
python --version  # Ensure 3.11+
```

3. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install PyQt5 qdarkstyle
```

5. **Initialize data files (if not present)**
```bash
# User data
echo '{}' > user_app/users.json

# Worker data
echo '{}' > worker_app/worker.json
echo '{}' > worker_app/approval_requests.json
echo '{}' > worker_app/loan_requests.json
echo '[]' > worker_app/system_logs.json
echo '{}' > worker_app/transfer_requests.json
```

---

## 🎮 Usage

### Running the User App
```bash
cd user_app
python app.py
```

**Test Account** (if configured):
- Email: `elnamaky2004@icloud.com`
- Password: (set during registration)

### Running the Worker App
```bash
cd worker_app
python app.py
```

**Test Accounts** (based on PERMISSIONS_GUIDE):
- **Manager**: `tarek.soliman@bank.com` / `TSadmin99`
- **Admin**: `osama.elnamki@bank.com` / `12345678`
- **Teller**: `mohamed.khaled@bank.com` / `MK2024`
- **Auditor**: `nour.ibrahim@bank.com` / `NourPass1`

---

## 📖 Documentation

- **Worker Permissions**: See [`worker_app/PERMISSIONS_GUIDE.md`](worker_app/PERMISSIONS_GUIDE.md)
- **Theme Customization**: See `theme.py` in both apps

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

**Osama Elnamaky**  
- LinkedIn: [osama-elnamaky](https://www.linkedin.com/in/osama-elnamaky-55a11324a/)  
- GitHub: [@elnamaky2004](https://github.com/elnamaky2004)

---

## 🙏 Acknowledgments

- **QDarkStyleSheet** - Professional dark theme library
- **PyQt5** - Powerful Python GUI framework
- **Python Community** - For excellent documentation and support

---

## ⚠️ Disclaimer

This is an educational project demonstrating desktop application development with PyQt5. **Do not use in production** without implementing proper security measures:
- Password hashing
- Database encryption
- SQL injection prevention
- Input validation
- Secure session management
- HTTPS for any web components
- Compliance with financial regulations

---

**Built with ❤️ using Python and PyQt5**
