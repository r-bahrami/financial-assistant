# Financial Assistant

> **Your Personal Financial Tracker** - Track, Analyze, and Optimize Your Finances Locally and Securely

A powerful, privacy-focused web application for managing your personal finances. Import bank statements, auto-categorize transactions, create budgets, and gain insights into your financial health - all stored locally on your computer.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.13+](https://img.shields.io/badge/Python-3.13%2B-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/Version-1.0--draft-green.svg)](https://github.com/saeid-h/financial-assistant/releases)

---

## 🚀 Quick Start

```bash
# 1. Clone and setup
git clone https://github.com/saeid-h/financial-assistant.git
cd financial-assistant
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install and initialize
pip install -r requirements.txt
python src/init_db.py
python src/seed_rules.py

# 3. Run the application
./start.sh

# 4. Open in browser
# Visit: http://localhost:5001
```

**First time user?** Check out the [Getting Started Guide](docs/user-manual/01-getting-started.md)!

---

## ✨ Features

### 💳 **Account Management**
- Track checking, savings, and credit card accounts
- Set reference balance with date for accurate tracking
- View real-time current balances
- Edit and manage multiple accounts

### 📥 **Smart CSV Import**
- **100+ bank formats supported** - Chase, Bank of America, Citi, Wells Fargo, and more
- Automatic format detection (delimiters, dates, columns)
- Duplicate detection (prevents re-importing same transactions)
- Bulk import with preview and validation
- Archives original files automatically

### 🏷️ **Auto-Categorization**
- **65+ pre-defined rules** for common merchants
- **80-90% auto-categorization rate** out of the box
- Learning system creates rules from your corrections
- 3-level category hierarchy (Income, Expenses, Transfers)
- Manual categorization with cascading picker
- Soft & hard recategorization modes

### 🔍 **Advanced Search & Filtering**
- Real-time search as you type
- Filter by account, date range, amount
- Filter by category, transaction type
- Advanced filter panel
- Color-coded transactions (Green=Income, Red=Expense, Purple=Transfer)

### 📊 **Visual Reports & Analytics**
- **5 Report Types**: Standard charts, month comparison, merchant analysis, net worth, custom builder
- **Standard Charts**: 4 interactive Chart.js visualizations (income/expenses, category pie, trends, top categories)
- **Month Comparison**: Side-by-side analysis with variance tracking
- **Merchant Analysis**: Top 50 merchants, spending patterns, smart grouping
- **Net Worth Tracker**: Wealth trajectory over time with growth metrics
- **Custom Report Builder**: Flexible metrics, groupings, and visualizations
- Date range filters (8 presets + custom)
- CSV export on all reports
- PDF export capability (reportlab installed)

### 💰 **Budget Management**
- Create monthly budgets by category
- Real-time progress tracking
- Color-coded alerts (On Track, Warning, Over Budget)
- Visual progress bars
- Multiple budgets per month

### 💹 **Transfer Accounting**
- Proper handling of credit card payments
- Account-to-account transfers marked neutral
- Transfers excluded from expense calculations
- Purple color coding for visual distinction
- Accurate net worth tracking

### 🔄 **Recurring Transaction Detection** (Phase 3)
- Auto-detect subscriptions and bills (Levenshtein algorithm)
- 5 frequency types: weekly, bi-weekly, monthly, quarterly, annual
- 85% similarity threshold with fuzzy matching
- Alert on missing payments (3+ days overdue)
- Alert on amount changes (>10% variance)
- Bulk scanner CLI tool
- Manage recurring items (pause, resume, delete)

### 📊 **Financial Health Dashboard** (Phase 3)
- Comprehensive health score (0-100 algorithm)
- 30-day income, expenses, and savings rate
- Total net worth across all accounts
- Top 5 spending categories (excludes transfer categories)
- Quick links to all features
- One-click financial overview

### 🔐 **Privacy & Security**
- **100% local storage** - No cloud, no external servers
- All data stays on your computer
- Git-ignored data directories
- No data transmission over internet

---

## 📚 User Manual

Comprehensive guides for every feature:

### Getting Started
- **[1. Getting Started](docs/user-manual/01-getting-started.md)** - Installation, first launch, quick setup

### Core Features
- **[2. Account Management](docs/user-manual/02-accounts.md)** - Adding accounts, setting reference balance, editing, deleting
- **[3. Importing Transactions](docs/user-manual/03-importing-transactions.md)** - CSV upload, supported formats, duplicate detection, manual entry
- **[4. Viewing Transactions](docs/user-manual/04-viewing-transactions.md)** - Transaction list, search, filters, color coding
- **[5. Categorization](docs/user-manual/05-categorization.md)** - Auto-categorization, manual categorization, rules, learning system

### Analysis & Planning
- **[6. Reports & Charts](docs/user-manual/06-reports.md)** - Visual analysis, chart types, filtering, export
- **[7. Budget Management](docs/user-manual/07-budgets.md)** - Creating budgets, tracking progress, alerts

### Advanced Topics
- **[8. Transfer Transactions](docs/user-manual/08-transfers.md)** - Understanding transfers, accounting paradigm, neutral transactions
- **[9. Admin Functions](docs/user-manual/09-admin.md)** - Database management, backups, recategorization
- **[10. Troubleshooting](docs/user-manual/10-troubleshooting.md)** - Common issues, solutions, debugging

**→ [Complete User Manual Index](docs/user-manual/00-index.md)**

---

## 🏗️ Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Backend** | Python Flask | 3.0.0 |
| **Database** | SQLite | 3.x |
| **Data Processing** | pandas | 2.2.0+ |
| **Frontend** | HTML5/CSS3/JavaScript | - |
| **Charts** | Chart.js | 4.4.0 |
| **Testing** | pytest | 8.0.0+ |
| **Python** | CPython | 3.13+ |

---

## 📂 Project Structure

```
financial-assistant/
├── src/                          # Source code
│   ├── app.py                   # Flask application entry point
│   ├── init_db.py               # Database initialization
│   ├── seed_rules.py            # Categorization rules seeder
│   ├── reset_transactions.py    # Utility to clear transactions
│   ├── scan_recurring.py        # CLI tool for recurring detection
│   ├── migrate_*.py             # Database migration scripts
│   ├── models/                  # Database models
│   │   ├── account.py          # Account CRUD operations
│   │   ├── transaction.py      # Transaction model
│   │   ├── category.py         # Category management
│   │   ├── budget.py           # Budget model
│   │   └── goal.py             # Savings goals model
│   ├── services/                # Business logic
│   │   ├── csv_parser.py       # CSV parsing (100+ formats)
│   │   ├── categorization_engine.py  # Auto-categorization
│   │   ├── duplicate_detector.py     # Duplicate detection
│   │   ├── file_archiver.py    # CSV archiving
│   │   ├── report_service.py   # Report data aggregation
│   │   ├── budget_service.py   # Budget calculations
│   │   ├── recurring_detector.py     # Pattern detection (Levenshtein)
│   │   └── recurring_manager.py      # Recurring CRUD & alerts
│   ├── routes/                  # Flask blueprints
│   │   ├── accounts.py         # Account API
│   │   ├── import_routes.py    # Import functionality
│   │   ├── transactions.py     # Transaction API
│   │   ├── categories.py       # Category API
│   │   ├── reports.py          # Reports API (5 report types)
│   │   ├── budgets.py          # Budget API
│   │   ├── recurring.py        # Recurring transactions API
│   │   ├── dashboard.py        # Financial health dashboard
│   │   └── admin.py            # Admin functions
│   ├── templates/               # Jinja2 HTML templates
│   │   ├── reports*.html       # 5 report templates
│   │   ├── dashboard.html      # Financial health dashboard
│   │   ├── recurring.html      # Recurring transactions page
│   │   └── ...                 # Other templates
│   └── static/css/             # Stylesheets
├── data/                         # Data storage (gitignored)
│   ├── financial_assistant.db  # SQLite database
│   └── archives/               # Archived CSV files (YYYY/MM/)
├── docs/                        # Documentation
│   ├── user-manual/            # User guides
│   ├── delivery/               # PBI documentation
│   │   ├── backlog.md         # Product backlog
│   │   └── {1-7}/             # PBI directories
│   ├── CSV-FORMAT-GUIDE.md    # Detailed CSV format guide
│   └── technical/             # Technical documentation
├── tests/                       # Test suite
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   ├── fixtures/               # Test data
│   └── conftest.py            # Pytest configuration
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Pytest configuration
├── start.sh                    # Application launcher
├── .gitignore                  # Git ignore rules (protects data)
└── LICENSE                     # MIT License
```

---

## 🎯 Development Roadmap

### ✅ Phase 1: MVP - Core Functionality (COMPLETE)
- [x] Project infrastructure and setup
- [x] CSV import with flexible parsing
- [x] Account management
- [x] Transaction categorization
- [x] Basic reporting

### ✅ Phase 2: Enhanced Features (COMPLETE)
- [x] Advanced search and filtering
- [x] Budget management system
- [x] Transfer transaction handling
- [x] Reference balance with dates

### 🔄 Phase 3: Advanced Financial Tracking (IN PROGRESS)
- [ ] Recurring transaction detection
- [ ] Savings goals tracking
- [ ] Cash flow predictions and alerts
- [ ] Financial health dashboard

### 📅 Phase 4: Future Enhancements (PLANNED)
- [ ] Category picker scrolling improvements
- [ ] Hierarchical category counting
- [ ] Multi-currency support
- [ ] Mobile-responsive design
- [ ] Data export/import tools

**Current Version**: v1.0-draft ([Tagged](https://github.com/saeid-h/financial-assistant/releases))

---

## 🧪 Testing

### Running Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html tests/

# Run specific test category
pytest tests/unit/           # Unit tests only
pytest tests/integration/    # Integration tests only

# Run specific test file
pytest tests/unit/test_account_model.py
```

### Test Statistics (v1.0-draft)

```
Total Tests: 125+
Unit Tests: 85+
Integration Tests: 40+
Coverage: 85%+
Status: ✅ All Passing
```

### Writing Tests

Follow the project structure:
- **Unit tests**: `tests/unit/test_{module}.py`
- **Integration tests**: `tests/integration/test_{feature}.py`
- **Fixtures**: `tests/fixtures/` for test data

---

## 🔧 Configuration

### Application Settings

**Port**: Default is `5001` (configurable in `src/app.py`)

**Database**: `data/financial_assistant.db` (SQLite)

**Debug Mode**: Enabled by default for development

### Environment Variables

Currently not used. All configuration is in source files.

---

## 🛠️ Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Can't access localhost:5001 | Start application with `./start.sh` |
| Port already in use | Kill process: `lsof -i :5001` then `kill -9 <PID>` |
| Import fails | Check [CSV Format Guide](docs/CSV-FORMAT-GUIDE.md) |
| Categories not showing | Hard refresh: `Cmd+Shift+R` or `Ctrl+Shift+R` |
| Balance incorrect | Set reference balance and date in account settings |
| Tests failing | Reinstall dependencies: `pip install -r requirements.txt` |

**→ [Complete Troubleshooting Guide](docs/user-manual/10-troubleshooting.md)**

---

## 📖 Documentation

### For Users
- **[User Manual](docs/user-manual/00-index.md)** - Comprehensive guides for all features
- **[CSV Format Guide](docs/CSV-FORMAT-GUIDE.md)** - Supported bank formats
- **[Quick Start](docs/user-manual/01-getting-started.md)** - 5-minute setup guide

### For Developers
- **[Project Policy](.cursor/rules/sw-pbi.mdc)** - Development workflow and rules
- **[Product Backlog](docs/delivery/backlog.md)** - PBIs and roadmap
- **[PBI Documentation](docs/delivery/)** - Detailed requirements for each feature
- **[Git Rules](docs/technical/git-rules.md)** - Commit conventions

### Additional Resources
- **[Privacy Policy](PRIVACY.md)** - Data handling and privacy
- **[License](LICENSE)** - MIT License details

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Follow the project policy**: See [.cursor/rules/sw-pbi.mdc](.cursor/rules/sw-pbi.mdc)
4. **Write tests** for new features
5. **Ensure all tests pass**: `pytest`
6. **Commit with clear messages**: Follow [Git Rules](docs/technical/git-rules.md)
7. **Push and create a pull request**

### Development Workflow

This project follows a **Task-Driven Development** approach:
- All work must be linked to a PBI (Product Backlog Item)
- Each PBI has detailed tasks in `docs/delivery/{PBI-ID}/`
- All commits reference task IDs
- See [Project Policy](.cursor/rules/sw-pbi.mdc) for full workflow

---

## 📊 Project Stats

### Current Status (v1.0-draft)

```
✅ PBIs Completed: 7
✅ Total Tests: 125+
✅ Code Coverage: 85%+
✅ Supported Banks: 100+
✅ Auto-Categorization Rules: 65+
✅ Default Categories: 30+
```

### Phase Completion

- ✅ **Phase 1**: Core Functionality (PBIs 1-5) - **COMPLETE**
- ✅ **Phase 2**: Enhanced Features (PBIs 6-7) - **COMPLETE**
- 🔄 **Phase 3**: Advanced Financial Tracking (PBIs 8-11) - **IN PROGRESS**
- 📅 **Phase 4**: Future Enhancements - **PLANNED**

---

## 🎯 Key Features Explained

### Reference Balance System

**Problem**: Without a starting point, your balance is just the sum of imported transactions.

**Solution**:
```
Reference Balance: $10,000.00 (as of Oct 1, 2025)
+ Imported Transactions: -$2,570.59
= Current Balance: $7,429.41 ✓
```

Set reference balance when editing any account!

### Transfer Accounting

**Transfers are NEUTRAL** - they don't change your net worth:

```
Income:    $5,000  💰 (Money IN - green)
Expenses:  $3,000  💸 (Money OUT - red)
Transfers: $500    💹 (Neutral - purple)
────────────────────
Net Flow:  +$2,000 📊 (Income - Expenses, excludes transfers)
```

Credit card payments from checking = Transfer (not expense!)

### Auto-Categorization

Import transactions and **80-90% categorize automatically**:
- COSTCO WHSE → Groceries
- NETFLIX → Entertainment
- SHELL → Transportation (Gas)
- AUTOPAY → Account Transfer

**Two recategorization modes:**
- 🟢 **Soft**: Categorizes only uncategorized (safe)
- 🟡 **Hard**: Recategorizes ALL (overrides manual work)

---

## 💻 System Requirements

### Minimum

- **OS**: macOS 10.15+, Windows 10+, Linux
- **Python**: 3.13 or higher
- **RAM**: 2GB
- **Disk**: 500MB (plus space for your data)
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

### Recommended

- **RAM**: 4GB+
- **Disk**: 2GB (for large transaction history)
- **Browser**: Latest Chrome or Firefox
- **Screen**: 1920x1080 or higher

---

## 🔒 Privacy & Security

### Local-Only Storage

✅ **All data stored locally** on your computer  
✅ **No external servers** - No data transmission  
✅ **No cloud sync** - Complete privacy  
✅ **Git-ignored data** - Won't accidentally commit to GitHub  

**Your data never leaves your machine!**

### Data Locations

```
data/
├── financial_assistant.db    # SQLite database (gitignored)
└── archives/                 # Original CSV files (gitignored)
    └── YYYY/MM/             # Organized by year and month
```

**Protected by `.gitignore`** - Sensitive data never committed to version control.

### Backup Recommendations

**Manual backup**:
```bash
# Copy database to safe location
cp data/financial_assistant.db ~/Backups/financial_$(date +%Y%m%d).db
```

**Automated** (future feature):
- Planned for Phase 4
- Automatic daily/weekly backups
- Cloud backup support (encrypted)

---

## 🐛 Troubleshooting

### Quick Fixes

**90% of issues fixed by:**
1. Hard refresh: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)
2. Restart application: Stop (Ctrl+C) and run `./start.sh`
3. Clear browser cache: DevTools → Application → Clear Storage

### Common Issues

**"Can't access localhost:5001"**
- Start the application: `./start.sh`
- Check terminal for errors
- Try http://127.0.0.1:5001

**"CSV import failed"**
- Check [CSV Format Guide](docs/CSV-FORMAT-GUIDE.md)
- Verify file is actual CSV (not Excel)
- Try re-downloading from bank

**"Category picker not working"**
- Hard refresh browser (Cmd+Shift+R)
- Clear browser cache
- Check browser console for errors

**"Balance doesn't update"**
- Edit account → Set reference balance and date
- Current balance will recalculate automatically

**→ [Complete Troubleshooting Guide](docs/user-manual/10-troubleshooting.md)**

---

## 📈 Changelog

### v1.0-draft (2025-10-19)

**Phase 1 & 2 Complete:**
- ✅ 7 PBIs implemented
- ✅ 125+ tests passing
- ✅ 100+ bank CSV formats supported
- ✅ 65+ auto-categorization rules
- ✅ 4 chart types
- ✅ Budget management
- ✅ Transfer accounting

**Recent Updates:**
- Added reference date to accounts
- Transfer transactions now purple
- Current balance auto-recalculation
- Dual recategorization modes (soft/hard)
- Comprehensive user manual

**Known Issues:**
- Category picker scrolling (deferred)
- Hierarchical category counting (planned)

**Git Tag**: `v1.0-draft` - Stable checkpoint for Phase 1 & 2

---

## 🤔 FAQ

**Q: Is this free?**  
A: Yes! MIT License - free to use, modify, and distribute.

**Q: Does it work on Windows/Mac/Linux?**  
A: Yes! Python and Flask run on all platforms.

**Q: Where is my data stored?**  
A: Locally in `data/financial_assistant.db` - never leaves your computer.

**Q: Can I use it for multiple people?**  
A: Currently single-user. Multi-user support planned for future.

**Q: What banks are supported?**  
A: 100+ banks! See [CSV Format Guide](docs/CSV-FORMAT-GUIDE.md). If your bank exports CSV, it likely works.

**Q: Can I import OFX/QFX files?**  
A: Not yet. CSV only for now. OFX support planned for future.

**Q: How do I backup my data?**  
A: Copy `data/financial_assistant.db` and `data/archives/` to a safe location. See [Admin Guide](docs/user-manual/09-admin.md).

**Q: Is it safe for sensitive financial data?**  
A: Yes! All data is local-only. No internet connection required. See [Privacy Policy](PRIVACY.md).

---

## 📋 Changelog

### v2.0 (October 2025) - Enhanced Reports & Analysis
- ✅ **4 New Report Types**: Month Comparison, Merchant Analysis, Net Worth Tracker, Custom Report Builder
- ✅ **Month Comparison**: Side-by-side variance analysis with color coding
- ✅ **Merchant Analysis**: Top 50 merchants with smart grouping and real-time search
- ✅ **Net Worth Tracker**: Wealth trajectory with growth metrics
- ✅ **Custom Report Builder**: Flexible metrics, groupings, and visualizations
- ✅ **CSV Export**: Available on all reports
- ✅ **Reports Navigation Hub**: Organized access to all 5 report types
- ✅ **File Organization**: Moved utility scripts to `src/` directory
- ✅ **PDF Export Prep**: Installed reportlab dependency

### v1.0 (October 2025) - Phase 3 Complete
- ✅ **Financial Health Dashboard**: Health score, 30-day metrics, top categories
- ✅ **Recurring Transactions**: Auto-detection with Levenshtein algorithm, 5 frequencies
- ✅ **Savings Goals**: Database schema and model (UI deferred)
- ✅ **Cash Flow Alerts**: Integrated with recurring patterns
- ✅ **Phase 3**: 11 PBIs complete, 100% feature delivery

### v0.9 (October 2025) - Phase 2 Complete
- ✅ **Budget Management**: Monthly budgets, progress tracking, alerts
- ✅ **Enhanced Search**: Real-time search, amount filters, transaction type filters
- ✅ **Notes & Tags**: Database schema (UI deferred)
- ✅ **Phase 2**: 7 PBIs complete

### v0.8 (October 2025) - Phase 1 Complete
- ✅ **CSV Import**: Flexible parser supporting 100+ formats from major banks
- ✅ **Auto-Categorization**: 30 categories, 65+ rules, pattern matching engine
- ✅ **Visual Reports**: 4 Chart.js visualizations with date filters
- ✅ **Account Management**: Full CRUD with balance tracking
- ✅ **Transaction Views**: Filter, search, statistics dashboard
- ✅ **Duplicate Detection**: Hash-based checking with configurable thresholds
- ✅ **File Archiving**: Automatic CSV archiving to `data/archives/YYYY/MM/`

---

## 📜 License

**MIT License**

Copyright © 2025 Saeed Hoss

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

See [LICENSE](LICENSE) file for full text.

---

## 👤 Author

**Saeed Hoss**

- **GitHub**: https://github.com/saeid-h
- **Repository**: https://github.com/saeid-h/financial-assistant
- **License**: MIT

---

## 🙏 Acknowledgments

- **Flask** - Web framework
- **pandas** - CSV parsing and data manipulation
- **Chart.js** - Beautiful charts
- **SQLite** - Reliable local database
- **pytest** - Comprehensive testing framework

---

## 🔗 Quick Links

- 📚 [User Manual](docs/user-manual/00-index.md)
- 📋 [Product Backlog](docs/delivery/backlog.md)
- 📊 [CSV Format Guide](docs/CSV-FORMAT-GUIDE.md)
- 🔒 [Privacy Policy](PRIVACY.md)
- 📄 [License](LICENSE)
- 🐛 [Report Issues](https://github.com/saeid-h/financial-assistant/issues)

---

**Version**: 1.0-draft  
**Last Updated**: 2025-10-19  
**Status**: Phase 1 & 2 Complete, Phase 3 In Progress

**Start tracking your finances today!** → [Getting Started Guide](docs/user-manual/01-getting-started.md)

