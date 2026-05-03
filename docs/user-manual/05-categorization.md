# 5. Categorization

[← Previous: Viewing Transactions](./04-viewing-transactions.md) | [Back to Index](./00-index.md) | [Next: Reports & Charts →](./06-reports.md)

---

## Overview

Categorization helps you understand WHERE your money goes. The system includes:
- **65+ pre-defined categorization rules** for common merchants
- **Automatic categorization** during import
- **Manual categorization** with cascading picker
- **Learning system** that creates rules from your choices
- **Two recategorization modes** (soft and hard)

---

## Accessing Categorization

**From Home Page**: Click "🏷️ Auto-Categorization"  
**From Navigation**: Click "Categories" in top menu  
**Direct URL**: http://localhost:5001/categories

---

## Category Hierarchy

Financial Assistant uses a **3-level hierarchy**:

### Level 1: Category Types (4 types)

```
💰 Income
💸 Expenses
   ├─ Fixed Expenses
   ├─ Variable Expenses
   └─ Optional Expenses
🔄 Transfers & Neutral
```

### Level 2: Subcategories

**Examples under "Variable Expenses":**
- Groceries
- Transportation
- Healthcare
- Childcare
- Personal Care

**Examples under "Optional Expenses":**
- Dining Out
- Entertainment
- Shopping
- Travel
- Hobbies
- Subscriptions
- Gifts

### Level 3: Details (Optional)

You can add specific details under any level 2 category:

**Example under "Insurance" (Fixed Expenses):**
- Car Insurance
- Health Insurance
- Home Insurance
- Life Insurance

---

## Auto-Categorization System

### How It Works

The system has **65+ pattern-matching rules**:

**Examples:**
```
"COSTCO WHSE" → Groceries
"NETFLIX" → Entertainment (Subscriptions)
"SHELL" → Transportation (Gas)  
"AUTOPAY" → Account Transfer
"SAFEWAY" → Groceries
"STARBUCKS" → Dining Out
```

### When Auto-Categorization Runs

1. **During CSV import** - Automatically applied to all valid transactions
2. **When you click "Soft Recategorize"** - Categorizes uncategorized items
3. **When you click "Hard Recategorize"** - Re-categorizes EVERYTHING

### Success Rates

Typical auto-categorization rates:
- **80-90%** for common merchants (Costco, Netflix, Walmart, etc.)
- **50-70%** for unique local businesses
- **Remaining** need manual categorization

---

## Manual Categorization

### Using the Category Picker

**Step 1: Open the Picker**
- Go to Transactions page
- Find an uncategorized transaction
- Click the gray **"Uncategorized"** button

**Step 2: Navigate the Hierarchy**

The picker shows up to 3 columns:

```
┌──────────────────┬──────────────────┬────────────────┐
│ Column 1         │ Column 2         │ Column 3       │
│ (Level 1)        │ (Level 2)        │ (Level 3)      │
├──────────────────┼──────────────────┼────────────────┤
│ ➕ Add New...    │                  │                │
│ 💰 Income        │                  │                │
│ 💸 Fixed Exp    →│                  │                │
│ 💸 Variable Exp  │                  │                │
│ 💸 Optional Exp  │                  │                │
│ 🔄 Transfers     │                  │                │
└──────────────────┴──────────────────┴────────────────┘

Click "Optional Expenses":

┌──────────────────┬──────────────────┬────────────────┐
│ Optional Exp   ✓ │ ➕ Add New...    │                │
│                  │ Dining Out      →│                │
│                  │ Entertainment    │                │
│                  │ Shopping         │                │
│                  │ Travel           │                │
│                  │ Hobbies          │                │
│                  │ Subscriptions    │                │
│                  │ Gifts            │                │
└──────────────────┴──────────────────┴────────────────┘
```

**Step 3: Assign Category**
- Select through the hierarchy
- Check "🧠 Remember this for similar transactions" (optional, creates rule)
- Click **"✓ Assign Category"** button

**The transaction updates immediately!**

### Creating New Categories While Categorizing

**If you need a category that doesn't exist:**

1. In the picker, click **"➕ Add New..."** at the top of any column
2. Enter the category name (e.g., "Gym Membership")
3. Category is created and **automatically selected**
4. Click "✓ Assign Category"

**Example**: Adding "Car Insurance"
```
Column 1: Fixed Expenses
Column 2: Click "Insurance"
Column 3: Click "➕ Add New Insurance Detail..."
Enter: "Car Insurance"
→ Auto-selected!
[✓ Assign Category]
```

---

## Recategorization Modes

Visit the **Categories page** (/categories) to see two powerful buttons:

### 🟢 Soft Recategorization

**Button**: "🔄 Auto-Cat Uncategorized"

**What it does:**
- Only processes **UNCATEGORIZED** transactions
- **Preserves** your manual categorizations
- Safe to run anytime

**When to use:**
- After importing new CSV files
- After adding new categorization rules
- Regular maintenance

**Example:**
```
Before Soft Recat:
- 200 manually categorized
- 876 uncategorized

After Soft Recat:
- 200 manually categorized (UNCHANGED)
- 700 auto-categorized (NEW)
- 176 still uncategorized (no matching rules)
```

### 🟡 Hard Recategorization  

**Button**: "⚡ Re-Cat ALL (Override)"

**What it does:**
- Recategorizes **ALL** transactions
- **Overrides** manual categorizations
- **DOUBLE confirmation** required
- Use with caution!

**When to use:**
- Rules changed dramatically
- Want to trust auto-cat more than manual
- Starting fresh with categorization

**Example:**
```
Before Hard Recat:
- 876 categorized (manual + auto)
- 200 uncategorized

After Hard Recat:
- ALL 1,076 recategorized from scratch
- Manual categorizations LOST
- Fresh start based on current rules
```

---

## Managing Categories & Rules

Visit **/categories/manage** for full category and rule management.

### Categories Tab

**Add New Category:**
1. Enter category name
2. Select level (1, 2, or 3)
3. Select parent (for level 2/3)
4. Click "Add Category"

**Delete Category:**
- Click "Delete" next to any category
- Confirmation required
- Transactions using this category become uncategorized

### Rules Tab

**View All Rules:**
- See all 65+ categorization rules
- Pattern → Category mapping
- Priority order

**Add New Rule:**
1. Enter pattern (e.g., "TRADER JOE")
2. Select category
3. Set priority (higher = more important)
4. Click "Create Rule"

**Edit Existing Rule:**
1. Click "Edit" button next to any rule
2. Modify pattern, category, or priority
3. Click "Update Rule"
4. Changes apply to future transactions

**How patterns work:**
- Case-insensitive
- Substring matching
- "COSTCO" matches "COSTCO WHSE #123", "Costco Gas", etc.

**Delete Rule:**
- Click "Delete" next to any rule
- Future transactions won't use this rule
- Existing categorizations unchanged

---

## Learning System

### How It Works

When you manually categorize a transaction with **"🧠 Remember this"** checked:
1. System extracts keywords from description
2. Creates a new categorization rule
3. Future transactions with similar descriptions auto-categorize

**Example:**
```
You categorize:
Description: "TRADER JOE'S #456"
Category: Groceries
[✓] Remember this for similar transactions

System creates rule:
Pattern: "TRADER JOE"
→ Groceries

Future transactions match:
"TRADER JOE'S #789" → Auto-categorized as Groceries!
```

### When to Use Learning

**DO use learning for:**
- ✅ Recurring merchants (your regular grocery store)
- ✅ Subscriptions (Netflix, Spotify, etc.)
- ✅ Regular bills (utilities, insurance)
- ✅ Frequently visited businesses

**DON'T use learning for:**
- ❌ One-time purchases
- ❌ Ambiguous descriptions
- ❌ Generic terms ("PURCHASE", "PAYMENT")

---

## Category Statistics

On the Categories page, you'll see:

```
Database Statistics:
┌─────────────────────────────────────┐
│ Total Categories: 45                │
│ Total Rules: 65                     │
│ Categorized: 876 (81%)              │
│ Uncategorized: 200 (19%)            │
└─────────────────────────────────────┘
```

**Category Hierarchy with Counts:**
- Shows how many transactions in each category
- Helps you understand spending patterns
- Identifies categories needing attention

---

## Best Practices

### ✅ DO

- **Run soft recategorize** after importing new data
- **Use the learning system** for recurring merchants
- **Create specific categories** for your regular expenses
- **Review uncategorized monthly** and assign categories
- **Use hierarchical structure** (Level 1 → 2 → 3) for better reports

### ❌ DON'T

- Don't create too many level-1 categories (use subcategories instead)
- Don't use hard recategorize unless absolutely necessary
- Don't create duplicate categories with different names
- Don't forget to check "Remember this" for recurring merchants

---

## Common Categorization Patterns

### Groceries
- **Primary**: Costco, Safeway, Trader Joe's, Whole Foods
- **Category**: Variable Expenses → Groceries

### Entertainment
- **Streaming**: Netflix, Spotify, Disney+, HBO, Hulu
- **Category**: Optional Expenses → Entertainment (Subscriptions)

### Dining Out
- **Restaurants**: Chipotle, McDonald's, Starbucks
- **Category**: Optional Expenses → Dining Out

### Transportation
- **Gas**: Shell, Chevron, 76, Arco
- **Category**: Variable Expenses → Transportation (Gas)

### Bills & Utilities
- **Electric, Gas, Water**: PG&E, SoCal Gas
- **Category**: Fixed Expenses → Utilities

### Transfers
- **Credit card payments**: Autopay, Payment
- **Account transfers**: Online Transfer, Transfer
- **Category**: Transfers & Neutral → Account Transfer

---

## Troubleshooting

**Issue**: Category not showing in picker  
**Solution**: Hard refresh (Cmd+Shift+R), category might be in a different hierarchy

**Issue**: Can't assign category (button disabled)  
**Solution**: Select a category first in the picker

**Issue**: "Remember this" not working  
**Solution**: The rule was created but won't apply to existing transactions - use "Soft Recategorize"

**Issue**: Too many uncategorized  
**Solution**: 
1. Go to Categories page
2. Click "🔄 Auto-Cat Uncategorized"
3. Manually categorize remaining items

---

## Next Steps

- **Analyze spending** - See [Reports & Charts](./06-reports.md)
- **Set budgets** - See [Budget Management](./07-budgets.md)
- **Understand transfers** - See [Transfer Transactions](./08-transfers.md)

---

[← Previous: Viewing Transactions](./04-viewing-transactions.md) | [Back to Index](./00-index.md) | [Next: Reports & Charts →](./06-reports.md)


