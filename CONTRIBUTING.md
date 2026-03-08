# Contributing to Python Banking System

Thank you for your interest in contributing to this project! 🎉

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)

---

## 📜 Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to:
- Be respectful and inclusive
- Provide constructive feedback
- Focus on what's best for the project
- Show empathy towards other contributors

---

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/banking_program.git
   cd banking_program
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/elnamaky2004/banking_program.git
   ```

---

## 🛠 Development Setup

### Prerequisites
- Python 3.11.9+ (pyenv recommended)
- Git
- Code editor (VS Code recommended)

### Setup Steps

1. **Create virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Test the applications**:
   ```bash
   # User app
   cd user_app && python app.py
   
   # Worker app
   cd worker_app && python app.py
   ```

---

## 🤝 How to Contribute

### Reporting Bugs
1. Check if the bug is already reported in [Issues](https://github.com/elnamaky2004/banking_program/issues)
2. If not, create a new issue with:
   - Clear title
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots (if applicable)
   - Environment details (OS, Python version)

### Suggesting Features
1. Check existing feature requests
2. Open a new issue with:
   - Clear description of the feature
   - Use case and benefits
   - Proposed implementation (optional)

### Submitting Code
1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Follow coding standards (see below)
   - Add comments for complex logic
   - Update documentation if needed

3. **Test your changes**:
   - Test both user and worker apps
   - Verify theme switching works
   - Check for errors in console

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request** on GitHub

---

## 💻 Coding Standards

### Python Style
- Follow **PEP 8** guidelines
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use snake_case for functions and variables
- Use PascalCase for classes

### PyQt5 Conventions
- Use descriptive object names
- Set `objectName` for styled widgets
- Use layouts instead of absolute positioning
- Keep UI logic separate from business logic

### File Organization
```python
# Order of imports
import sys                    # Standard library
import json
from pathlib import Path

from PyQt5.QtWidgets import   # Third-party
from PyQt5.QtCore import

import theme                  # Local modules
from other_module import
```

### Naming Conventions
- **Files**: `snake_case.py` (e.g., `approve_transactions.py`)
- **Classes**: `PascalCase` (e.g., `ApproveTransactionsWindow`)
- **Functions**: `snake_case` with leading underscore for private (e.g., `_load_data()`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `SENDER_EMAIL`)

### Documentation
- Add docstrings to classes and complex functions
- Use inline comments for non-obvious logic
- Update README.md for new features

---

## 📝 Commit Guidelines

### Commit Message Format
```
<type>: <subject>

[optional body]

[optional footer]
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Formatting, missing semicolons, etc.
- **refactor**: Code restructuring
- **test**: Adding tests
- **chore**: Maintenance tasks

### Examples
```bash
feat: Add transaction export to PDF

fix: Resolve OTP expiration bug

docs: Update installation instructions in README

refactor: Simplify loan approval logic
```

---

## 🔄 Pull Request Process

### Before Submitting
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No errors in console
- [ ] Tested on both apps (if applicable)

### PR Template
When creating a PR, include:

**Description**
- What changes were made?
- Why were they needed?

**Type of Change**
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

**Testing**
- How was this tested?
- Test cases covered?

**Screenshots** (if UI changes)

---

## 🎯 Priority Areas

### High Priority
- [ ] Database migration (SQLite/PostgreSQL)
- [ ] Password hashing implementation
- [ ] Input validation improvements
- [ ] Error handling enhancements

### Medium Priority
- [ ] Unit tests (pytest)
- [ ] Transaction history export (PDF/CSV)
- [ ] Email notifications
- [ ] Loan repayment tracking

### Nice to Have
- [ ] Mobile web version
- [ ] Multi-language support
- [ ] Custom themes
- [ ] Backup/restore functionality

---

## ❓ Questions?

If you have questions, feel free to:
- Open an issue for discussion
- Contact the maintainer via [LinkedIn](https://www.linkedin.com/in/osama-elnamaky-55a11324a/)

---

## 🙏 Thank You!

Your contributions make this project better. We appreciate your time and effort! 🎉

---

**Happy Coding!** 🚀
