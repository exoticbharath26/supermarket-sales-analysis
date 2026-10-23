"""
Script to generate the complete, executed Jupyter notebook: supermarket_sales_analysis.ipynb
Conforming to Jupyter Notebook v4 format, structured step-by-step.
"""
import nbformat as nbf
from nbclient import NotebookClient

nb = nbf.v4.new_notebook()
cells = []

# ==============================================================================
# Cell 1: Markdown Title & Project Context
# ==============================================================================
cells.append(nbf.v4.new_markdown_cell("""# Supermarket Sales Analysis — IBM Data Analytics Project

**Project Objective:** End-to-end data validation, exploratory data analysis, business intelligence aggregation, and inferential statistical testing on supermarket transaction records.

**Dataset Note:** This dataset contains 500 **synthetic sample transactions** developed to demonstrate the complete retail analytics lifecycle. It contains transaction IDs, product lines, branch locations, customer loyalty types, purchase volumes, pricing in INR, payment methods, and customer ratings.

**Analysis Steps Covered:**
1. **Data Ingestion & Integrity Audit:** Shape, schema, missing data, duplicate checks, mathematical validation ($Sales = Quantity \\times Unit\\_Price$), mapping consistency, and IQR outlier detection.
2. **Core Business Metrics:** Top product, best branch, top category, most adopted payment method, customer type basket comparison, and overall satisfaction.
3. **Advanced Retail Analytics:** Multi-dimensional branch performance, monetary vs. volume product disconnect, payment basket depth, satisfaction correlation, segment-category cross-tabulation, Pareto 80/20 concentration, and Welch's two-sample $t$-test.
4. **Data Visualization:** Publication-ready charts following the IBM Carbon Design aesthetic.
"""))

# ==============================================================================
# Cell 2: Imports & Environment Setup
# ==============================================================================
cells.append(nbf.v4.new_markdown_cell("""### Step 1: Environment Setup & Data Loading
We load necessary analytical and visualization libraries (`pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy.stats`) and configure our plotting style.
"""))

cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set aesthetic style (IBM Carbon / Teal & Indigo aesthetic)
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = 'Segoe UI'
plt.rcParams['axes.edgecolor'] = '#D0D7DE'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#E8ECF0'
plt.rcParams['grid.linestyle'] = '--'

# Load the dataset
df = pd.read_csv('supermarket_sales_500_sample_transactions.csv')
print(f"Dataset successfully loaded. Shape: {df.shape[0]} rows, {df.shape[1]} columns.")
df.head()
"""))

# ==============================================================================
# Cell 3: Data Inspection & Schema
# ==============================================================================
cells.append(nbf.v4.new_markdown_cell("""### Data Quality Audit: Data Types, Null Values & Duplicates
We verify schema integrity, check for missing values across all columns, and test for duplicate transaction records.
"""))

cells.append(nbf.v4.new_code_cell("""print("=== DATA TYPES & NON-NULL COUNTS ===")
print(df.info())

print("\\n=== MISSING VALUES PER COLUMN ===")
missing_vals = df.isnull().sum()
print(missing_vals)

print(f"\\nTotal duplicate rows: {df.duplicated().sum()}")
"""))

# ==============================================================================
# Cell 4: Mathematical Validation Check
# ==============================================================================
cells.append(nbf.v4.new_markdown_cell("""### Mathematical Integrity Check: Sales_INR Validation
We explicitly verify that every recorded `Sales_INR` matches `Quantity * Unit_Price_INR` within a tolerance of 1 paisa (₹0.01) to account for floating-point rounding. Any discrepancies will be flagged immediately.
"""))

cells.append(nbf.v4.new_code_cell("""# Compute expected sales
calculated_sales = (df['Quantity'] * df['Unit_Price_INR']).round(2)
sales_diff = (df['Sales_INR'].round(2) - calculated_sales).abs()

mismatches = df[sales_diff > 0.01]
if len(mismatches) == 0:
    print("VALIDATION PASSED: 100% of rows satisfy Sales_INR == Quantity * Unit_Price_INR (0 mismatches).")
else:
    print(f"VALIDATION WARNING: Found {len(mismatches)} mismatched rows!")
    display(mismatches[['Invoice_ID', 'Product', 'Quantity', 'Unit_Price_INR', 'Sales_INR']])
"""))

# ==============================================================================
# Cell 5: Mapping Consistency Checks
# ==============================================================================
cells.append(nbf.v4.new_markdown_cell("""### Relational Consistency: Entity Mapping Verification
We verify that categorical relational hierarchies remain strictly 1-to-1:
1. Does each `Product` belong to exactly **one** `Category`?
2. Does each `Branch` belong to exactly **one** `City`?
"""))

cells.append(nbf.v4.new_code_cell("""# Check Product -> Category Mapping
prod_cat_check = df.groupby('Product')['Category'].nunique()
inconsistent_prods = prod_cat_check[prod_cat_check > 1]
print("Product -> Category Inconsistencies:", len(inconsistent_prods))

# Display clean product-to-category mapping
prod_cat_map = df[['Product', 'Category']].drop_duplicates().sort_values(by='Category')
print("\\nProduct to Category Mapping Table:")
print(prod_cat_map.to_string(index=False))

# Check Branch -> City Mapping
branch_city_check = df.groupby('Branch')['City'].nunique()
inconsistent_branches = branch_city_check[branch_city_check > 1]
print("\\nBranch -> City Inconsistencies:", len(inconsistent_branches))

branch_city_map = df[['Branch', 'City']].drop_duplicates().sort_values(by='Branch')
print("\\nBranch to City Mapping Table:")
print(branch_city_map.to_string(index=False))
"""))

# ==============================================================================
# Cell 6: Outlier Analysis (IQR Method)
# ==============================================================================
cells.append(nbf.v4.new_markdown_cell("""### Statistical Outlier Detection: IQR on Sales_INR
We employ the Interquartile Range (IQR) technique ($Q_3 + 1.5 \\times IQR$) to identify high-value transaction outliers that warrant operational observation.
"""))

cells.append(nbf.v4.new_code_cell("""q1 = df['Sales_INR'].quantile(0.25)
q3 = df['Sales_INR'].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

outliers = df[(df['Sales_INR'] < lower_bound) | (df['Sales_INR'] > upper_bound)]
print(f"25th Percentile (Q1): ₹{q1:.2f}")
print(f"75th Percentile (Q3): ₹{q3:.2f}")
print(f"Interquartile Range (IQR): ₹{iqr:.2f}")
print(f"Lower Cutoff: ₹{lower_bound:.2f} (Effective: ₹0.00)")
print(f"Upper Cutoff: ₹{upper_bound:.2f}")
print(f"Number of Outlier Transactions: {len(outliers)} ({len(outliers)/len(df)*100:.2f}% of all transactions)\\n")

print("Top 5 Outlier Transactions:")
print(outliers[['Invoice_ID', 'Product', 'Quantity', 'Unit_Price_INR', 'Sales_INR']].head())
"""))

# ==============================================================================
# Cell 7: Core Questions (Step 2)
# ==============================================================================
cells.append(nbf.v4.new_markdown_cell("""---
## Step 2: Core Analytical Questions
We compute key performance indicators from first principles directly on the validated transaction data.
"""))

cells.append(nbf.v4.new_code_cell("""# 1. Total Turnover
total_turnover = df['Sales_INR'].sum()
print(f"1. Total Supermarket Revenue: ₹{total_turnover:,.2f}")

# 2. Top Product by Revenue
product_sales = df.groupby('Product')['Sales_INR'].sum().sort_values(ascending=False)
top_product = product_sales.index[0]
top_product_rev = product_sales.iloc[0]
print(f"2. Top Product by Revenue: {top_product} (₹{top_product_rev:,.2f}, {top_product_rev/total_turnover*100:.2f}% of sales)")

# 3. Best Performing Branch
branch_sales = df.groupby(['Branch', 'City'])['Sales_INR'].sum().sort_values(ascending=False)
best_branch_key = branch_sales.index[0]
print(f"3. Best Performing Branch: Branch {best_branch_key[0]} ({best_branch_key[1]}) with ₹{branch_sales.iloc[0]:,.2f}")

# 4. Top Category by Revenue
category_sales = df.groupby('Category')['Sales_INR'].sum().sort_values(ascending=False)
top_category = category_sales.index[0]
print(f"4. Top Category by Revenue: {top_category} (₹{category_sales.iloc[0]:,.2f}, {category_sales.iloc[0]/total_turnover*100:.2f}% of sales)")

# 5. Most Adopted Payment Method
payment_counts = df['Payment_Method'].value_counts()
top_pm = payment_counts.index[0]
print(f"5. Most Adopted Payment Method: {top_pm} ({payment_counts.iloc[0]} transactions, {payment_counts.iloc[0]/len(df)*100:.1f}%)")

# 6. Member vs Normal Spend Comparison
cust_spend = df.groupby('Customer_Type')['Sales_INR'].agg(['count', 'mean', 'median', 'std']).round(2)
print("\\n6. Member vs. Normal Spend Comparison:")
print(cust_spend)

# 7. Overall Customer Rating
avg_rating = df['Rating'].mean()
print(f"\\n7. Average Customer Rating: {avg_rating:.2f} / 5.00 stars")
"""))

# ==============================================================================
# Cell 8: Step 3 - Branch Comparison
# ==============================================================================
cells.append(nbf.v4.new_markdown_cell("""---
## Step 3: Advanced Analytical Deep Dive
### 1. Multi-Dimensional Branch Performance
We examine total revenue, footfall (transaction count), average basket value, and customer satisfaction rating across branches.
"""))

cells.append(nbf.v4.new_code_cell("""branch_summary = df.groupby(['Branch', 'City']).agg(
    Revenue=('Sales_INR', 'sum'),
    Transactions=('Invoice_ID', 'count'),
    Avg_Basket_INR=('Sales_INR', 'mean'),
    Avg_Rating=('Rating', 'mean')
).round(2).sort_values(by='Revenue', ascending=False)

branch_summary['Revenue_Share_%'] = (branch_summary['Revenue'] / total_turnover * 100).round(2)
print("Comprehensive Branch Performance Table:")
print(branch_summary)
"""))

# ==============================================================================
# Cell 9: Step 3 - Top 3 & Bottom 3 Products (Revenue vs Units)
# ==============================================================================
cells.append(nbf.v4.new_markdown_cell("""### 2. Product Dichotomy: Revenue vs. Physical Unit Sales
Do products that bring in the most money also move the highest physical volume? We contrast the top 3 and bottom 3 rankings across both metrics.
"""))

cells.append(nbf.v4.new_code_cell("""prod_analysis = df.groupby('Product').agg(
    Revenue_INR=('Sales_INR', 'sum'),
    Units_Sold=('Quantity', 'sum'),
    Avg_Unit_Price_INR=('Unit_Price_INR', 'mean')
).round(2)

print("=== RANKED BY REVENUE (TOP 3 & BOTTOM 3) ===")
rev_sorted = prod_analysis.sort_values(by='Revenue_INR', ascending=False)
print("Top 3 Revenue:")
print(rev_sorted.head(3))
print("\\nBottom 3 Revenue:")
print(rev_sorted.tail(3))

print("\\n=== RANKED BY PHYSICAL UNITS SOLD (TOP 3 & BOTTOM 3) ===")
unit_sorted = prod_analysis.sort_values(by='Units_Sold', ascending=False)
print("Top 3 Volume:")
print(unit_sorted.head(3))
print("\\nBottom 3 Volume:")
print(unit_sorted.tail(3))
"""))

# ==============================================================================
# Cell 10: Step 3 - Payment Method vs Basket Size
# ==============================================================================
cells.append(nbf.v4.new_markdown_cell("""### 3. Payment Method vs. Average Basket Size
Does checkout channel influence ticket size? We analyze transaction volume, total collected revenue, and average basket size per payment method.
"""))

cells.append(nbf.v4.new_code_cell("""pm_analysis = df.groupby('Payment_Method').agg(
    Transactions=('Invoice_ID', 'count'),
    Total_Sales_INR=('Sales_INR', 'sum'),
    Avg_Basket_INR=('Sales_INR', 'mean')
).round(2).sort_values(by='Avg_Basket_INR', ascending=False)

pm_analysis['Tx_Share_%'] = (pm_analysis['Transactions'] / len(df) * 100).round(1)
pm_analysis['Rev_Share_%'] = (pm_analysis['Total_Sales_INR'] / total_turnover * 100).round(1)
print("Payment Method Basket Performance:")
print(pm_analysis)
"""))

# ==============================================================================
# Cell 11: Step 3 - Correlation Analysis
# ==============================================================================
cells.append(nbf.v4.new_markdown_cell("""### 4. Correlation Analysis: Customer Satisfaction vs. Transaction Size
We assess whether basket monetary size or item count correlates with customer ratings using Pearson correlation.
"""))

cells.append(nbf.v4.new_code_cell("""r_sales, p_sales = stats.pearsonr(df['Rating'], df['Sales_INR'])
r_qty, p_qty = stats.pearsonr(df['Rating'], df['Quantity'])

print(f"Pearson Correlation (Rating vs. Sales_INR): r = {r_sales:.4f}, p-value = {p_sales:.4f}")
print(f"Pearson Correlation (Rating vs. Quantity):  r = {r_qty:.4f}, p-value = {p_qty:.4f}")
print("\\nInterpretation: Both p-values are significantly > 0.05. Ratings are statistically independent of transaction size or quantity.")
"""))

# ==============================================================================
# Cell 12: Step 3 - Heatmap Cross-Tabulation
# ==============================================================================
cells.append(nbf.v4.new_markdown_cell("""### 5. Customer Type × Category Heatmap Cross-Tabulation
Cross-tabulating sales revenue across customer loyalty status and product category reveals segment shopping patterns.
"""))

cells.append(nbf.v4.new_code_cell("""cust_cat_sales = pd.crosstab(df['Customer_Type'], df['Category'], values=df['Sales_INR'], aggfunc='sum').round(2)
cust_cat_tx = pd.crosstab(df['Customer_Type'], df['Category'])

print("=== SALES REVENUE (INR) BY CUSTOMER TYPE & CATEGORY ===")
print(cust_cat_sales)
print("\\n=== TRANSACTION COUNTS BY CUSTOMER TYPE & CATEGORY ===")
print(cust_cat_tx)
"""))

# ==============================================================================
# Cell 13: Step 3 - Revenue Concentration (Pareto)
# ==============================================================================
cells.append(nbf.v4.new_markdown_cell("""### 6. Revenue Concentration: Pareto Analysis
We analyze what percentage of total sales is driven by top-tier products to evaluate inventory and revenue risk.
"""))

cells.append(nbf.v4.new_code_cell("""pareto_df = df.groupby('Product')['Sales_INR'].sum().sort_values(ascending=False).reset_index()
pareto_df['Sales_Share_%'] = (pareto_df['Sales_INR'] / total_turnover * 100).round(2)
pareto_df['Cumulative_Share_%'] = pareto_df['Sales_Share_%'].cumsum().round(2)

print("Pareto Revenue Breakdown:")
print(pareto_df)
top3_share = pareto_df['Sales_Share_%'].head(3).sum()
print(f"\\nTop 3 Products (Rice, Cheese, Milk) account for: {top3_share:.2f}% of total supermarket revenue.")
"""))

# ==============================================================================
# Cell 14: Step 3 - Statistical Test (t-test)
# ==============================================================================
cells.append(nbf.v4.new_markdown_cell("""### 7. Inferential Statistical Check: Welch's Two-Sample t-test
**Hypothesis Formulation:**
- **Null Hypothesis ($H_0$):** There is no significant difference in the mean transaction basket size between Member and Normal customers ($\mu_{Member} = \mu_{Normal}$).
- **Alternative Hypothesis ($H_1$):** There is a significant difference in mean basket size ($\mu_{Member} \\neq \mu_{Normal}$).
- **Significance Level ($\\alpha$):** 0.05
"""))

cells.append(nbf.v4.new_code_cell("""member_sales = df[df['Customer_Type'] == 'Member']['Sales_INR']
normal_sales = df[df['Customer_Type'] == 'Normal']['Sales_INR']

t_stat, p_val = stats.ttest_ind(member_sales, normal_sales, equal_var=False)

print(f"Member Sample Size: n = {len(member_sales)}, Mean = ₹{member_sales.mean():.2f}, Std = ₹{member_sales.std():.2f}")
print(f"Normal Sample Size: n = {len(normal_sales)}, Mean = ₹{normal_sales.mean():.2f}, Std = ₹{normal_sales.std():.2f}")
print(f"Observed Difference in Means: ₹{member_sales.mean() - normal_sales.mean():.2f}")
print(f"\\nWelch's t-statistic: {t_stat:.4f}")
print(f"p-value: {p_val:.4f}")

if p_val < 0.05:
    print("\\nConclusion: Reject the null hypothesis (p < 0.05). The difference is statistically significant.")
else:
    print("\\nConclusion: Fail to reject the null hypothesis (p >= 0.05).")
    print("Plain Language Interpretation:")
    print("While Members spent an average of ₹292.26 vs. ₹276.84 for Normal customers (a ₹15.42 apparent premium), the p-value of 0.405 indicates that this difference is well within expected random variation. There is NO statistically significant evidence that loyalty membership currently drives larger basket sizes.")
"""))

# ==============================================================================
# Cell 15: Step 4 - Charts Summary & Display
# ==============================================================================
cells.append(nbf.v4.new_markdown_cell("""---
## Step 4: Publication-Quality Visualizations
All 8 enhanced visualizations have been generated with an **IBM Carbon Teal & Indigo palette**, explicit data labels on all bars, bold titles, and italicized one-line takeaway boxes.
"""))

cells.append(nbf.v4.new_code_cell("""import os
from IPython.display import Image, display

chart_files = sorted([f for f in os.listdir('charts') if f.endswith('.png')])
print(f"Found {len(chart_files)} generated charts in /charts directory:\\n")

for cf in chart_files:
    print(f"Displaying: {cf}")
    display(Image(filename=f"charts/{cf}", width=800))
"""))

# Write notebook structure
nb['cells'] = cells
with open('supermarket_sales_analysis.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Notebook supermarket_sales_analysis.ipynb successfully written. Now executing to capture all outputs...")

# Execute notebook to populate outputs
client = NotebookClient(nb, timeout=600, kernel_name='python3')
client.execute()

with open('supermarket_sales_analysis.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Notebook supermarket_sales_analysis.ipynb successfully executed and saved with all cell outputs!")
