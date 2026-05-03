# 6. Reports & Charts

[← Previous: Categorization](./05-categorization.md) | [Back to Index](./00-index.md) | [Next: Budget Management →](./07-budgets.md)

---

## Overview

The Reports system provides comprehensive visual and analytical tools for understanding your finances. Choose from 5 report types ranging from standard charts to custom analysis.

**Access**: Click "Reports" in navigation or visit http://localhost:5001/reports

---

## Report Types Available

The Reports page now features a navigation hub with 5 report types:

1. **📊 Standard Charts** - 4 interactive Chart.js visualizations
2. **📅 Month Comparison** - Side-by-side month analysis (NEW!)
3. **🏪 Merchant Analysis** - Top merchants and spending patterns (NEW!)
4. **💎 Net Worth Tracker** - Wealth trajectory over time (NEW!)
5. **🔧 Custom Report Builder** - Build your own reports (NEW!)

---

## Standard Charts (/reports)

### Available Charts

### 1. 📈 Monthly Income vs Expenses (Line Chart)

**What it shows:**
- Income trend over time (green line)
- Expense trend over time (red line)
- Month-by-month comparison

**Use cases:**
- See if spending is increasing/decreasing
- Identify income fluctuations
- Compare summer vs winter spending

**Example:**
```
Jan 2025: Income $5,000, Expenses $3,500
Feb 2025: Income $5,000, Expenses $4,200
Mar 2025: Income $6,500, Expenses $3,800

→ You can see that Feb expenses were high!
```

### 2. 🥧 Spending by Category (Pie Chart)

**What it shows:**
- Percentage of total spending per category
- Visual breakdown of where money goes
- **Excludes transfer categories** (Account Transfer, etc.)

**Use cases:**
- Identify biggest spending categories
- See budget allocation needs
- Find savings opportunities

**Note**: Transfer categories are automatically excluded from this chart since they don't represent actual spending.

**Example:**
```
Groceries: 35% ($1,050)
Dining Out: 20% ($600)
Transportation: 15% ($450)
Entertainment: 10% ($300)
Other: 20% ($600)

→ Groceries is your biggest expense!
```

### 3. 📊 Monthly Category Trends (Stacked Bar Chart)

**What it shows:**
- Month-by-month spending per category
- Stacked bars show category contribution
- **Excludes transfer categories** (Account Transfer, etc.)

**Use cases:**
- See seasonal patterns (heating in winter, AC in summer)
- Track category spending over time
- Identify irregular months

**Note**: Transfer categories are automatically excluded since they don't represent actual spending.

**Example:**
```
October:
  Groceries: $1,200
  Dining: $400
  Gas: $200
  Total: $1,800

November:
  Groceries: $1,500
  Dining: $300
  Gas: $180
  Total: $1,980

→ November groceries were higher (Thanksgiving?)
```

### 4. 📊 Top 10 Categories (Horizontal Bar Chart)

**What it shows:**
- Highest spending categories
- Sorted by amount (largest first)
- **Excludes transfer categories** (Account Transfer, etc.)

**Use cases:**
- Quick overview of biggest expenses
- Budget priority identification
- Savings opportunity analysis

**Note**: Transfer categories are automatically excluded since they don't represent actual spending.

**Example:**
```
1. Groceries:      $3,450
2. Rent:           $1,800
3. Dining Out:     $1,200
4. Gas:            $780
5. Entertainment:  $450
...

→ Top 3 categories account for 70% of spending
```

---

## Filtering Reports

### Date Range Filters

**8 Preset Options:**
- Last 7 Days
- Last 30 Days
- Last 90 Days
- Last 6 Months
- Last 12 Months
- This Month
- This Year
- All Time

**Custom Range:**
- Set "Date From" and "Date To"
- Click "Apply Filters"

**Example:**
```
Want to see just October 2025?
Date From: 2025-10-01
Date To: 2025-10-31
[Apply Filters]
```

### Account Filter

**Dropdown**: "All Accounts" or select specific account

**Use cases:**
- Analyze just your credit card spending
- Compare checking vs savings patterns
- Focus on one account

**Example:**
```
Filter: Costco Citi Visa (credit card only)
→ Charts show only Costco card spending
→ Helps track credit card categories
```

### Combining Filters

You can combine account + date range:

**Example**:
```
Account: Chase Checking
Date: Last 90 Days
→ Shows 3-month spending from your checking account
```

---

## Exporting Data

### CSV Export

**Button**: "Export to CSV" (top right of page)

**What you get:**
- CSV file with current filtered data
- Includes all visible transactions
- Headers: Date, Amount, Category, Description
- Opens in Excel/Numbers/Google Sheets

**Use cases:**
- Analyze in spreadsheet software
- Create custom charts
- Share with accountant
- Backup your data

**File naming:**
```
transactions_export_YYYYMMDD_HHMMSS.csv
Example: transactions_export_20251019_154530.csv
```

---

## Interpreting Charts

### Income vs Expenses (Line Chart)

**Green line above red line** = Saving money (good!) ✅
**Red line above green line** = Spending more than earning (warning!) ⚠️
**Lines converging** = Savings decreasing
**Lines diverging** = Savings increasing

**Example interpretation:**
```
Jan: Income $5k, Expenses $3k → Saved $2k ✅
Feb: Income $5k, Expenses $4k → Saved $1k (less)
Mar: Income $5k, Expenses $5.5k → Lost $500 ⚠️

→ Trend is worsening, need to reduce spending!
```

### Category Breakdown (Pie Chart)

**Large slices** = Major spending areas (target for budgets)  
**Many small slices** = Diffused spending (hard to control)  
**One dominant slice** = Concentrated spending (easy to budget)

**Example interpretation:**
```
Groceries: 40% (large slice)
→ Consider setting a grocery budget

10 slices each <5% (many small)
→ Consider grouping into "Miscellaneous"
```

### Monthly Trends (Stacked Bar)

**Growing bars over time** = Spending increasing ⚠️  
**Shrinking bars** = Spending decreasing ✅  
**Consistent bars** = Stable spending  
**Spikes** = Irregular expenses (investigate!)

**Example interpretation:**
```
Jul: $2,000
Aug: $2,100
Sep: $3,500 ← SPIKE!

→ Check September for unusual purchases
```

---

## Best Practices

### ✅ DO

- **Review charts monthly** to catch trends early
- **Use date filters** to compare time periods
- **Export data** before making big changes
- **Focus on top categories** for budget planning
- **Look for spikes** in stacked bar chart (investigate)

### ❌ DON'T

- Don't analyze without categorizing first (charts won't be useful)
- Don't compare different date ranges without adjusting for length
- Don't ignore trends (they show problems early!)

---

## Tips & Tricks

### Tip 1: Month-over-Month Comparison

**Compare this month to last month:**
1. Set Date Range: "This Month"
2. Note total expenses
3. Change to "Last 30 Days"
4. Compare values
5. Are you spending more or less?

### Tip 2: Year-over-Year Comparison

**Compare 2025 to 2024** (if you have data):
1. Filter: 2024-01-01 to 2024-12-31
2. Note total expenses
3. Filter: 2025-01-01 to 2025-12-31
4. Compare values
5. Calculate percentage change

### Tip 3: Seasonal Patterns

**Find seasonal expenses:**
1. Use "Last 12 Months" filter
2. Look at Monthly Trends chart
3. Identify peaks:
   - Summer: Travel, AC, vacation
   - Winter: Heating, holidays
   - Spring: Taxes, home improvement
   - Fall: Back to school, holidays

### Tip 4: Budget Planning

**Use reports to set budgets:**
1. Look at Spending by Category pie chart
2. Identify top 5 categories
3. Go to Budgets page
4. Create budgets for top categories
5. Use average monthly amount from charts

---

## Understanding Chart Data

### What's Included

**Income:**
- Salary, wages, bonuses
- Refunds, cashback
- Gifts received
- Interest earned

**Expenses:**
- Groceries, dining, shopping
- Bills, utilities, insurance
- Transportation, gas
- Entertainment, subscriptions

**EXCLUDED from charts:**
- **Transfer categories** (Account Transfer, etc.) - automatically excluded from all spending reports
- **Uncategorized transactions** (in some charts)

### Why Transfer Categories Are Excluded

Transfer categories don't represent actual spending:
- Paying credit card from checking = $0 net change
- Moving savings to checking = $0 net change
- Internal movements ≠ income or expenses

**All spending reports automatically exclude transfer categories** to show TRUE income/expenses without transfer noise. This includes:
- Top spending categories (dashboard and reports)
- Category breakdown charts
- Monthly category trends
- Spending by category pie charts

Transfer transactions are still visible in the transaction list and tracked separately in the transfers statistic.

---

## Interactive Features

### Hovering

**Hover over chart elements** to see details:
- Line chart: Exact values for that month
- Pie chart: Category name, amount, percentage
- Bar chart: Category breakdown for that month

### Clicking (Pie Chart)

**Click a pie slice** to:
- Highlight that category
- See exact breakdown
- (Future: Filter transactions to that category)

### Zooming (Future Feature)

Currently not implemented, planned for future:
- Click and drag to zoom
- Reset zoom button
- Drill-down into specific time periods

---

## Common Questions

**Q: Why don't my charts show any data?**  
A: You need to:
1. Import transactions first
2. Categorize them (or run auto-categorize)
3. Refresh the Reports page

**Q: Charts show "No data available"**  
A: Check your date range filter - you might be filtering to a period with no transactions

**Q: Pie chart shows "Uncategorized" as biggest slice**  
A: Go to Categories page → Click "🔄 Auto-Cat Uncategorized" to categorize your transactions

**Q: Can I print the charts?**  
A: Use browser print (Cmd+P / Ctrl+P) - charts will print as images

**Q: Can I customize chart colors?**  
A: Not currently - colors are fixed for consistency

---

---

## NEW: Month-over-Month Comparison (/reports/month-comparison)

### What It Is

Compare spending between any two months to identify trends and changes in your financial behavior.

### How to Use

1. Visit `/reports/month-comparison`
2. Select **Month 1** (base month, e.g., September)
3. Select **Month 2** (comparison month, e.g., October)
4. Click **"Compare"**

### What You'll See

**Summary Cards:**
- Month 1 Total Spending
- Month 2 Total Spending  
- Change ($ and %)

**Comparison Table:**
- Category-by-category breakdown
- Amount for each month
- Variance in $ and %
- Color coding:
  - 🔴 Red = Increased spending
  - 🟢 Green = Decreased spending
  - ▲ Up arrow = increase
  - ▼ Down arrow = decrease

### Use Cases

**"Did I improve this month?"**
- Compare this month to last month
- See which categories you reduced

**"Seasonal patterns?"**
- Compare summer to winter
- Identify seasonal expenses (heating, AC, etc.)

**"Budget impact?"**
- Compare month before budget to month after
- Measure budget effectiveness

### Example

```
September vs October Comparison:

Groceries: $1,200 → $1,050 (▼ -$150, -12.5%) ✓ Improved!
Dining Out: $300 → $450 (▲ +$150, +50.0%) ✗ Increased
Gas: $200 → $180 (▼ -$20, -10.0%) ✓ Reduced

Total: $3,500 → $3,400 (▼ -$100, -2.9%)
```

---

## NEW: Merchant Analysis (/reports/merchants)

### What It Is

Analyze where you spend your money by merchant/vendor. Identifies your most expensive stores and shopping patterns.

### How to Use

1. Visit `/reports/merchants`
2. Adjust date range if needed (defaults to last 90 days)
3. Click **"Load Merchants"** (or auto-loads)
4. Use search box to find specific merchants

### What You'll See

**Top 10 Chart:**
- Bar chart of your biggest spending merchants
- Visual comparison

**Top 50 Table:**
- Merchant name
- Total spent
- Transaction count
- Average per transaction
- Last seen date

### Features

**Smart Merchant Grouping:**
- "COSTCO WHSE #123" = "COSTCO #456" = same merchant
- "NETFLIX.COM" = "NETFLIX SUBSCRIPTION" = same merchant
- Uses same algorithm as recurring detection

**Search:**
- Type in search box to filter
- Real-time filtering
- Case-insensitive

### Use Cases

**"Where do I shop most?"**
- See top merchants by total spending
- Identify your regular stores

**"Which vendor is most expensive?"**
- Sort by total spent
- Find biggest expense sources

**"How often do I go to Costco?"**
- Check transaction count
- See visit frequency

**"Find savings opportunities?"**
- High total + high average = expensive vendor
- Consider alternatives

### Example

```
Top Merchants (Last 90 Days):

1. COSTCO WHSE     $2,450  (18 transactions)  Avg: $136
2. SAFEWAY         $1,200  (24 transactions)  Avg: $50
3. SHELL           $780    (15 transactions)  Avg: $52
4. AMAZON          $650    (12 transactions)  Avg: $54
5. NETFLIX         $48     (3 transactions)   Avg: $16
```

---

## NEW: Net Worth Tracker (/reports/net-worth)

### What It Is

Track your total wealth (all accounts combined) over time. See if you're getting richer or poorer.

### How to Use

1. Visit `/reports/net-worth`
2. Auto-loads all available history
3. View trajectory chart

### What You'll See

**Summary Cards:**
- Current Net Worth
- Change from Start ($ and color)
- Average Monthly Change
- Months Tracked

**Line Chart:**
- Net worth over time
- Month-by-month data points
- Green line = wealth increasing ✓
- Red line = wealth decreasing ✗

### How It's Calculated

For each month:
```
Net Worth = Sum of all account balances

Account Balance = Reference Balance + Transactions up to that month

Example:
Chase Checking:  $10,000 + (-$2,570) = $7,430
Costco Credit:   $0 + (-$3,771)      = -$3,771
────────────────────────────────────────────────
Net Worth:       $10,000 + (-$6,341) = $3,659
```

### Use Cases

**"Am I getting richer?"**
- Upward trend = yes!
- Downward trend = need to save more

**"What's my financial progress?"**
- See growth over 6 months, 1 year
- Measure wealth building

**"Is my debt decreasing?"**
- Credit card balances included (negative)
- Paying down debt increases net worth

**"Monthly progress check"**
- Average monthly change shows rate of growth
- Set goals based on this rate

### Example

```
Net Worth Trajectory:

January:  $3,000
February: $3,500  (+$500, +16.7%)
March:    $4,200  (+$700, +20.0%)
April:    $4,800  (+$600, +14.3%)

Current: $4,800
Change from Start: +$1,800
Avg Monthly Change: +$600
Trend: ✓ Increasing (green line)
```

---

## NEW: Custom Report Builder (/reports/builder)

### What It Is

Build your own custom reports with complete flexibility over metrics, groupings, date ranges, and visualizations.

### How to Use

**5-Step Process:**

**Step 1: Select Metrics** (what to measure)
- ☑ Income
- ☑ Expenses
- ☐ Net (Income - Expenses)
- ☐ Transaction Count
- ☐ Average Transaction

**Step 2: Group By** (how to organize)
- Category
- Merchant
- Account
- Month

**Step 3: Date Range**
- Date From: 2025-01-01
- Date To: 2025-12-31

**Step 4: Visualization**
- Table (default)
- Bar Chart
- Line Chart
- Pie Chart

**Step 5: Generate & Export**
- Click "Generate Report"
- Click "Export CSV" to download

### Example Reports

**Example 1: "Where did my money go last quarter?"**
```
Metrics: Expenses
Group By: Category
Date: Jul 1 - Sep 30
Visualization: Pie Chart

Result: Pie chart showing category breakdown
```

**Example 2: "Which account do I use most?"**
```
Metrics: Transaction Count
Group By: Account
Date: This Year
Visualization: Bar Chart

Result: Bar chart showing transactions per account
```

**Example 3: "Monthly income trend?"**
```
Metrics: Income
Group By: Month
Date: Last 12 Months
Visualization: Line Chart

Result: Line chart showing income over time
```

**Example 4: "Average grocery trip cost?"**
```
Metrics: Average Transaction
Group By: Merchant
Date: Last 90 Days
Visualization: Table

Result: Table with avg cost per merchant
```

### Advanced Features

**Multiple Metrics:**
- Select Income + Expenses together
- See both columns in results

**CSV Export:**
- Download results as spreadsheet
- Open in Excel/Numbers/Google Sheets
- Further analysis

**Dynamic Queries:**
- Backend builds query based on your selections
- Flexible and powerful

### Use Cases

**Budgeting:**
- "Show me all expense categories this month"
- Build budget based on historical averages

**Tax Preparation:**
- "Show me all income by month this year"
- Organize for tax filing

**Pattern Discovery:**
- "Which day of month do I spend most?"
- Group by date, look for patterns

**Comparative Analysis:**
- "How do my accounts compare?"
- Group by account, see differences

---

## Exporting Data

### CSV Export (Available Now)

**Custom Report Builder:**
- Generate any report
- Click "Export CSV"
- Opens in spreadsheet software

**Standard Reports:**
- Click "Export to CSV" button (bottom of standard reports page)
- Downloads all current data

### PDF Export (Future)

**Status**: Dependency installed (`reportlab`), service deferred

**When Available:**
- "Download PDF" button on each report
- Formatted PDF with charts and tables
- Print-ready format

**For Now:**
- Use browser print: `Cmd+P` (Mac) or `Ctrl+P` (Windows)
- Or use CSV export

---

## Next Steps

- **Create budgets** based on your spending patterns - See [Budget Management](./07-budgets.md)
- **Understand transfer transactions** - See [Transfer Transactions](./08-transfers.md)
- **Track recurring expenses** - See [Admin Functions](./09-admin.md) for recurring scanner

---

[← Previous: Categorization](./05-categorization.md) | [Back to Index](./00-index.md) | [Next: Budget Management →](./07-budgets.md)


