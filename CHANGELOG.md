# Changelog

All notable changes to the Python Banking System will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2026-03-08

### Major Release - Worker Portal & Advanced Features

### Added

#### User App (`user_app/`)
- **Account Verification System**
  - New accounts require worker approval before activation
  - `is_verified` flag in user data
  
- **Loan Request Feature** (`request_loan.py`)
  - Request loans with amount, purpose, and repayment period
  - Password confirmation required
  - Submitted to worker approval queue
  - Integration with loan calculator

- **Transaction Approval Workflow** (`transfer_money.py`)
  - Automatic approval requirement for transfers > 5000 EGP
  - Instant processing for transfers ≤ 5000 EGP
  - Request tracking with timestamps
  - Real-time balance validation

#### Worker App (`worker_app/`) - **NEW**
- **Worker Portal** - Complete administrative backend
  - Role-based access control system
  - Permission-based UI (buttons show/hide by role)
  - Dashboard with role, employee ID, and department info

- **User Management Module** (`manage_users.py`)
  - Approve/revoke user accounts
  - View pending verifications
  - Batch processing capabilities

- **Loan Approval Module** (`approve_loans.py`)
  - Review loan requests from users
  - Approve or reject with worker tracking
  - View loan details (amount, purpose, period)

- **Transaction Approval Module** (`approve_transactions.py`)
  - Review high-value transfer requests (> 5000 EGP)
  - Approve with automatic fund transfer
  - Reject with status update
  - Full sender/recipient details display

- **Transaction Management Module** (`manage_transactions.py`)
  - Direct deposits, withdrawals, and transfers
  - Worker-initiated account operations
  - Immediate processing for authorized personnel

- **Audit Module** (`audit_transactions.py`)
  - Search users by email or name
  - Generate full audit reports
  - Export transaction histories
  - Fixed balance type handling bugs

- **Reports Module** (`view_reports.py`)
  - User statistics and analytics
  - Transaction summaries
  - Loan overview reports

- **System Logs Module** (`view_logs.py`)
  - View all system activities
  - Clear logs (admin only)
  - Timestamp tracking

- **Permission System**
  - Granular access controls
  - Manager/Director with full access
  - Specialized roles: Admin, Branch Manager, Teller, Auditor
  - See `PERMISSIONS_GUIDE.md` for details

#### Theme System Enhancements
- **QDarkStyleSheet Integration**
  - Professional dark mode styling
  - Custom overrides for labels and buttons
  - Fallback to custom dark theme if library unavailable
  
- **Animated Toggle Switch**
  - Smooth toggle animation
  - Consistent theme across all windows
  - Synced state management

#### Documentation
- **Comprehensive README.md**
  - Complete feature documentation
  - Installation instructions
  - Usage examples
  - Test account credentials

- **PERMISSIONS_GUIDE.md** (Worker App)
  - Role and permission documentation
  - Available modules with required permissions
  - Test account information

- **CONTRIBUTING.md**
  - Contribution guidelines
  - Coding standards
  - Commit message format
  - PR process

- **LICENSE** (MIT)
- **requirements.txt**
- **.gitattributes** for consistent line endings

### Changed

- **Project Structure** - Reorganized into `user_app/` and `worker_app/` directories
- **Theme System** - Upgraded to use QDarkStyleSheet with custom overrides
- **Data Storage** - Added multiple JSON files for different data types
  - `user_app/users.json` - User accounts
  - `worker_app/worker.json` - Worker accounts
  - `worker_app/approval_requests.json` - Pending transfer approvals
  - `worker_app/loan_requests.json` - Pending loan requests
  - `worker_app/system_logs.json` - Activity logs
  - `worker_app/transfer_requests.json` - Transfer history

- **Label Sizing** - Fixed label font sizes to be consistent between light and dark modes
- **Button Styling** - Improved primary button styling across both apps

### Fixed

- **Audit Transactions** - Fixed search by name error (boolean argument handling)
- **Audit Report** - Fixed balance type conversion error in full audit generation
- **File Naming** - Renamed `transfer_requestd.json` → `transfer_requests.json`
- **Password Input** - Fixed incomplete password field in loan request form
- **Theme Consistency** - Fixed label sizes in dark mode to match light mode

### Security

- **Password Verification** - Required for sensitive operations (loans, profile updates)
- **Worker Verification** - Manual approval of new user accounts
- **High-Value Approvals** - Transfers > 5000 EGP require worker review
- **Role-Based Access** - Granular permissions for worker actions

---

## [1.0.0] - 2025-XX-XX

### Initial Release

### Added

#### User App Features
- User registration and login
- Transfer money between accounts
- View account information
- Update username and password
- About page with external links

#### Theme System
- Light mode
- Dark mode
- Theme toggle switch
- Global theme synchronization

#### Technical
- PyQt5 desktop GUI
- JSON-based data storage
- Git version control

---

## Future Releases

### [2.1.0] - Planned
- [ ] Database migration (SQLite)
- [ ] Password hashing (bcrypt)
- [ ] Transaction history export (PDF/CSV)
- [ ] Email notifications for approvals
- [ ] Unit tests (pytest)

### [3.0.0] - Planned
- [ ] Two-factor authentication (2FA)
- [ ] Real-time balance updates
- [ ] Loan repayment tracking
- [ ] Interest calculation automation
- [ ] Mobile-responsive web version

---

[2.0.0]: https://github.com/elnamaky2004/banking_program/releases/tag/v2.0.0
[1.0.0]: https://github.com/elnamaky2004/banking_program/releases/tag/v1.0.0
