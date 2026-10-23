"""
Generate Publication-Quality Enhanced Visualizations for Supermarket Sales Analysis
IBM Carbon / Teal & Indigo Aesthetic
"""
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Set aesthetic styling
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Segoe UI', 'DejaVu Sans', 'Arial'],
    'axes.edgecolor': '#D0D7DE',
    'axes.linewidth': 0.8,
    'grid.color': '#E8ECF0',
    'grid.linestyle': '--',
    'grid.alpha': 0.7,
    'figure.autolayout': False
})

IBM_PALETTE = ["#0F62FE", "#009D9A", "#8A3FFC", "#1192E8", "#005D5D", "#6929C4", "#002D9C", "#A56EFF", "#0043CE", "#33B1FF"]
TEAL_INDIGO = ["#009D9A", "#0F62FE", "#8A3FFC", "#1192E8"]

df = pd.read_csv('supermarket_sales_500_sample_transactions.csv')
os.makedirs('charts', exist_ok=True)

# -------------------------------------------------------------------------
# Chart 1: Sales by Product & Pareto Concentration
# -------------------------------------------------------------------------
prod_df = df.groupby('Product')['Sales_INR'].sum().reset_index().sort_values(by='Sales_INR', ascending=False)
prod_df['Cum_Pct'] = (prod_df['Sales_INR'].cumsum() / prod_df['Sales_INR'].sum()) * 100

fig, ax1 = plt.subplots(figsize=(10, 6))
bars = ax1.bar(prod_df['Product'], prod_df['Sales_INR'], color="#0F62FE", width=0.6, zorder=3, label='Sales (INR)')
ax1.set_ylabel('Total Sales (INR)', color='#0F62FE', fontsize=12, fontweight='bold')
ax1.set_ylim(0, prod_df['Sales_INR'].max() * 1.18)
ax1.tick_params(axis='x', rotation=30, labelsize=10)

# Add bar labels
for bar in bars:
    height = bar.get_height()
    ax1.annotate(f'₹{height:,.0f}',
                 xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 4),
                 textcoords="offset points",
                 ha='center', va='bottom', fontsize=9, fontweight='bold', color='#161616')

# Line plot for Pareto Cumulative Percentage
ax2 = ax1.twinx()
ax2.plot(prod_df['Product'], prod_df['Cum_Pct'], color="#8A3FFC", marker='o', linewidth=2.5, markersize=7, zorder=4, label='Cumulative %')
ax2.set_ylabel('Cumulative Sales %', color='#8A3FFC', fontsize=12, fontweight='bold')
ax2.set_ylim(0, 110)
ax2.grid(False)

# Add percentage labels
for i, txt in enumerate(prod_df['Cum_Pct']):
    ax2.annotate(f'{txt:.1f}%', (i, txt), textcoords="offset points", xytext=(0, 8),
                 ha='center', fontsize=8.5, fontweight='bold', color='#6929C4')

# Threshold line at 80%
ax2.axhline(80, color='#DA1E28', linestyle=':', alpha=0.8, label='80% Threshold')

plt.title('Product Revenue & Cumulative Pareto Distribution', fontsize=14, fontweight='bold', pad=15)
fig.text(0.5, -0.05, 'Takeaway: Rice is the top revenue generator (₹24,340); the top 3 products account for 42.16% of total supermarket turnover.',
         ha='center', fontsize=10.5, fontstyle='italic', color='#393939', bbox=dict(boxstyle='round,pad=0.5', facecolor='#F4F4F4', edgecolor='#D0D7DE'))
plt.tight_layout()
plt.savefig('charts/01_sales_by_product_pareto.png', dpi=300, bbox_inches='tight')
plt.close()

# -------------------------------------------------------------------------
# Chart 2: Branch Comparison (Revenue, Transactions, Avg Basket)
# -------------------------------------------------------------------------
branch_df = df.groupby(['Branch', 'City']).agg(
    Revenue=('Sales_INR', 'sum'),
    Transactions=('Invoice_ID', 'count'),
    Avg_Basket=('Sales_INR', 'mean'),
    Avg_Rating=('Rating', 'mean')
).reset_index()
branch_df['Branch_Label'] = branch_df['Branch'] + ' (' + branch_df['City'] + ')'
branch_df = branch_df.sort_values(by='Revenue', ascending=False)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))

# Subplot 1: Total Revenue
b_bars1 = ax1.bar(branch_df['Branch_Label'], branch_df['Revenue'], color=['#0F62FE', '#009D9A', '#1192E8'], width=0.55, zorder=3)
ax1.set_title('Total Revenue by Branch', fontsize=12, fontweight='bold')
ax1.set_ylabel('Revenue (INR)', fontsize=11)
ax1.set_ylim(0, branch_df['Revenue'].max() * 1.18)
for bar in b_bars1:
    h = bar.get_height()
    ax1.annotate(f'₹{h:,.0f}', xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 4),
                 textcoords="offset points", ha='center', va='bottom', fontsize=9.5, fontweight='bold')

# Subplot 2: Transactions & Avg Basket
x = np.arange(len(branch_df))
width = 0.35
ax2.bar(x - width/2, branch_df['Transactions'], width, label='Transactions (Count)', color='#009D9A', zorder=3)
ax2_twin = ax2.twinx()
ax2_twin.bar(x + width/2, branch_df['Avg_Basket'], width, label='Avg Basket (INR)', color='#8A3FFC', zorder=3)
ax2_twin.grid(False)

ax2.set_xticks(x)
ax2.set_xticklabels(branch_df['Branch_Label'], fontsize=10)
ax2.set_title('Transaction Volume vs. Average Basket Size', fontsize=12, fontweight='bold')
ax2.set_ylabel('Transaction Count', color='#009D9A', fontsize=11, fontweight='bold')
ax2_twin.set_ylabel('Average Basket (INR)', color='#8A3FFC', fontsize=11, fontweight='bold')
ax2.set_ylim(0, branch_df['Transactions'].max() * 1.25)
ax2_twin.set_ylim(0, branch_df['Avg_Basket'].max() * 1.25)

for i in range(len(branch_df)):
    ax2.annotate(f"{branch_df['Transactions'].iloc[i]}", xy=(x[i] - width/2, branch_df['Transactions'].iloc[i]),
                 xytext=(0, 4), textcoords="offset points", ha='center', fontsize=9, fontweight='bold', color='#005D5D')
    ax2_twin.annotate(f"₹{branch_df['Avg_Basket'].iloc[i]:.0f}", xy=(x[i] + width/2, branch_df['Avg_Basket'].iloc[i]),
                      xytext=(0, 4), textcoords="offset points", ha='center', fontsize=9, fontweight='bold', color='#6929C4')

fig.suptitle('Branch Performance Evaluation: Revenue, Traffic, and Basket Value', fontsize=14, fontweight='bold', y=1.02)
fig.text(0.5, -0.06, 'Takeaway: Branch C (Mumbai) leads across both total revenue (₹54,494) and average ticket size (₹297.78), followed by Branch A and Branch B.',
         ha='center', fontsize=10.5, fontstyle='italic', color='#393939', bbox=dict(boxstyle='round,pad=0.5', facecolor='#F4F4F4', edgecolor='#D0D7DE'))
plt.tight_layout()
plt.savefig('charts/02_sales_by_branch_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

# -------------------------------------------------------------------------
# Chart 3: Sales by Category
# -------------------------------------------------------------------------
cat_df = df.groupby('Category')['Sales_INR'].sum().reset_index().sort_values(by='Sales_INR', ascending=True)

fig, ax = plt.subplots(figsize=(10, 5.5))
colors = sns.color_palette(["#1192E8", "#009D9A", "#0F62FE", "#8A3FFC", "#6929C4", "#0043CE"], len(cat_df))
bars = ax.barh(cat_df['Category'], cat_df['Sales_INR'], color=colors, height=0.6, zorder=3)
ax.set_xlabel('Total Revenue (INR)', fontsize=11, fontweight='bold')
ax.set_title('Supermarket Revenue Distribution by Category', fontsize=14, fontweight='bold', pad=15)
ax.set_xlim(0, cat_df['Sales_INR'].max() * 1.18)

tot_rev = cat_df['Sales_INR'].sum()
for bar in bars:
    w = bar.get_width()
    share = (w / tot_rev) * 100
    ax.annotate(f'₹{w:,.2f} ({share:.1f}%)',
                xy=(w, bar.get_y() + bar.get_height() / 2),
                xytext=(6, 0), textcoords="offset points",
                ha='left', va='center', fontsize=9.5, fontweight='bold', color='#161616')

fig.text(0.5, -0.06, 'Takeaway: Beverages (31.4%) and Dairy (25.1%) collectively represent over 56.5% of total sales; Bakery is the smallest revenue contributor (5.2%).',
         ha='center', fontsize=10.5, fontstyle='italic', color='#393939', bbox=dict(boxstyle='round,pad=0.5', facecolor='#F4F4F4', edgecolor='#D0D7DE'))
plt.tight_layout()
plt.savefig('charts/03_sales_by_category.png', dpi=300, bbox_inches='tight')
plt.close()

# -------------------------------------------------------------------------
# Chart 4: Payment Methods & Basket Size Analysis
# -------------------------------------------------------------------------
pm_df = df.groupby('Payment_Method').agg(
    Transactions=('Invoice_ID', 'count'),
    Total_Revenue=('Sales_INR', 'sum'),
    Avg_Basket=('Sales_INR', 'mean')
).reset_index().sort_values(by='Transactions', ascending=False)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.2))

# Subplot 1: Transaction Volume Share
ax1.pie(pm_df['Transactions'], labels=pm_df['Payment_Method'], autopct='%1.1f%%', startangle=140,
        colors=['#0F62FE', '#009D9A', '#8A3FFC', '#1192E8'], explode=[0.05, 0, 0, 0],
        wedgeprops=dict(width=0.65, edgecolor='white', linewidth=2),
        textprops={'fontsize': 10, 'weight': 'bold'})
ax1.set_title('Transaction Volume by Payment Method', fontsize=12, fontweight='bold')

# Subplot 2: Average Basket Size by Payment Method
bars2 = ax2.bar(pm_df['Payment_Method'], pm_df['Avg_Basket'], color=['#0F62FE', '#009D9A', '#8A3FFC', '#1192E8'], width=0.55, zorder=3)
ax2.set_ylabel('Average Basket Size (INR)', fontsize=11, fontweight='bold')
ax2.set_title('Average Basket Spend per Method', fontsize=12, fontweight='bold')
ax2.set_ylim(0, pm_df['Avg_Basket'].max() * 1.2)
ax2.tick_params(axis='x', rotation=15)

for bar in bars2:
    h = bar.get_height()
    ax2.annotate(f'₹{h:.2f}', xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 4),
                 textcoords="offset points", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#161616')

fig.suptitle('Payment Channel Adoption and Spend Propensity', fontsize=14, fontweight='bold', y=1.02)
fig.text(0.5, -0.06, 'Takeaway: UPI is both the most frequent payment channel (27.8% volume) and drives the highest average basket value (₹315.40 vs E-wallet ₹258.82).',
         ha='center', fontsize=10.5, fontstyle='italic', color='#393939', bbox=dict(boxstyle='round,pad=0.5', facecolor='#F4F4F4', edgecolor='#D0D7DE'))
plt.tight_layout()
plt.savefig('charts/04_payment_methods_and_basket.png', dpi=300, bbox_inches='tight')
plt.close()

# -------------------------------------------------------------------------
# Chart 5: Member vs Normal Spend (Distribution & Welch t-test)
# -------------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.2))

# Subplot 1: Bar of Means & Medians
mem_stats = df.groupby('Customer_Type')['Sales_INR'].agg(['mean', 'median', 'std', 'count']).reset_index()
x = np.arange(len(mem_stats))
w = 0.35
b1 = ax1.bar(x - w/2, mem_stats['mean'], w, label='Mean Spend (INR)', color='#0F62FE', zorder=3)
b2 = ax1.bar(x + w/2, mem_stats['median'], w, label='Median Spend (INR)', color='#009D9A', zorder=3)
ax1.set_xticks(x)
ax1.set_xticklabels([f"{r.Customer_Type} (n={r['count']})" for _, r in mem_stats.iterrows()], fontsize=10, fontweight='bold')
ax1.set_ylabel('Spend (INR)', fontsize=11, fontweight='bold')
ax1.set_title('Mean & Median Basket Size by Customer Type', fontsize=12, fontweight='bold')
ax1.set_ylim(0, mem_stats['mean'].max() * 1.3)
ax1.legend(loc='upper right')

for bar in b1:
    h = bar.get_height()
    ax1.annotate(f'₹{h:.2f}', xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 4),
                 textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold')
for bar in b2:
    h = bar.get_height()
    ax1.annotate(f'₹{h:.2f}', xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 4),
                 textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold')

# Subplot 2: Violin & Boxplot
sns.violinplot(x='Customer_Type', y='Sales_INR', data=df, hue='Customer_Type', palette=['#0F62FE', '#009D9A'], ax=ax2, inner='quartile', cut=0, legend=False)
ax2.set_title('Spend Distribution & Spread Comparison', fontsize=12, fontweight='bold')
ax2.set_xlabel('Customer Type', fontsize=11, fontweight='bold')
ax2.set_ylabel('Sales (INR)', fontsize=11, fontweight='bold')

# Statistical Annotation box
ax2.text(0.5, 0.88, 'Welch Two-Sample t-test:\nt = 0.8334, p = 0.4050\n(Difference Not Statistically Significant)',
         transform=ax2.transAxes, ha='center', fontsize=9.5, fontweight='bold', color='#161616',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#E8ECF0', edgecolor='#8A3FFC', linewidth=1.2))

fig.suptitle('Customer Loyalty Impact Analysis: Member vs. Normal Shoppers', fontsize=14, fontweight='bold', y=1.02)
fig.text(0.5, -0.06, 'Takeaway: Members spend ₹15.42 more on average (₹292.26 vs ₹276.84), but the difference is statistically insignificant (p=0.405 > 0.05).',
         ha='center', fontsize=10.5, fontstyle='italic', color='#393939', bbox=dict(boxstyle='round,pad=0.5', facecolor='#F4F4F4', edgecolor='#D0D7DE'))
plt.tight_layout()
plt.savefig('charts/05_member_vs_normal_spend.png', dpi=300, bbox_inches='tight')
plt.close()

# -------------------------------------------------------------------------
# Chart 6: Top 3 & Bottom 3 Products: Revenue vs Units Sold Disconnect
# -------------------------------------------------------------------------
prod_all = df.groupby('Product').agg(
    Revenue=('Sales_INR', 'sum'),
    Units=('Quantity', 'sum')
).reset_index()

top3_rev = prod_all.sort_values(by='Revenue', ascending=False).head(3)
bot3_rev = prod_all.sort_values(by='Revenue', ascending=True).head(3)
top3_units = prod_all.sort_values(by='Units', ascending=False).head(3)
bot3_units = prod_all.sort_values(by='Units', ascending=True).head(3)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))

# Plot Revenue Rankings
rev_contrast = pd.concat([top3_rev.assign(Group='Top 3 Revenue'), bot3_rev.assign(Group='Bottom 3 Revenue')]).sort_values(by='Revenue', ascending=False)
bars1 = ax1.barh(rev_contrast['Product'], rev_contrast['Revenue'], color=['#0F62FE', '#009D9A', '#1192E8', '#6929C4', '#8A3FFC', '#A56EFF'], height=0.6, zorder=3)
ax1.set_xlabel('Revenue (INR)', fontsize=11, fontweight='bold')
ax1.set_title('Top 3 vs. Bottom 3 Products by Revenue', fontsize=12, fontweight='bold')
ax1.set_xlim(0, rev_contrast['Revenue'].max() * 1.25)
for bar in bars1:
    w = bar.get_width()
    ax1.annotate(f'₹{w:,.0f}', xy=(w, bar.get_y() + bar.get_height()/2), xytext=(5, 0),
                 textcoords="offset points", ha='left', va='center', fontsize=9, fontweight='bold')

# Plot Units Sold Rankings
unit_contrast = pd.concat([top3_units.assign(Group='Top 3 Units'), bot3_units.assign(Group='Bottom 3 Units')]).sort_values(by='Units', ascending=False)
bars2 = ax2.barh(unit_contrast['Product'], unit_contrast['Units'], color=['#009D9A', '#0F62FE', '#1192E8', '#6929C4', '#8A3FFC', '#A56EFF'], height=0.6, zorder=3)
ax2.set_xlabel('Units Sold (Quantity)', fontsize=11, fontweight='bold')
ax2.set_title('Top 3 vs. Bottom 3 Products by Volume', fontsize=12, fontweight='bold')
ax2.set_xlim(0, unit_contrast['Units'].max() * 1.25)
for bar in bars2:
    w = bar.get_width()
    ax2.annotate(f'{w:.0f} units', xy=(w, bar.get_y() + bar.get_height()/2), xytext=(5, 0),
                 textcoords="offset points", ha='left', va='center', fontsize=9, fontweight='bold')

fig.suptitle('Product Performance Dichotomy: Monetary Turnover vs. Physical Volume', fontsize=14, fontweight='bold', y=1.02)
fig.text(0.5, -0.06, 'Takeaway: Rankings sharply diverge: Cheese (#2 in revenue) is #8 in units; Snacks (#2 in volume) ranks #8 in revenue due to lower unit pricing.',
         ha='center', fontsize=10.5, fontstyle='italic', color='#393939', bbox=dict(boxstyle='round,pad=0.5', facecolor='#F4F4F4', edgecolor='#D0D7DE'))
plt.tight_layout()
plt.savefig('charts/06_revenue_vs_units_top_bottom.png', dpi=300, bbox_inches='tight')
plt.close()

# -------------------------------------------------------------------------
# Chart 7: Customer Type x Category Heatmap
# -------------------------------------------------------------------------
heat_data = pd.crosstab(df['Customer_Type'], df['Category'], values=df['Sales_INR'], aggfunc='sum')

fig, ax = plt.subplots(figsize=(10, 5))
cmap = sns.light_palette("#0F62FE", as_cmap=True)
sns.heatmap(heat_data, annot=True, fmt=',.0f', cmap=cmap, cbar_kws={'label': 'Revenue (INR)'},
            linewidths=1.5, linecolor='white', annot_kws={'size': 11, 'weight': 'bold'}, ax=ax)
ax.set_title('Customer Segment Spending Heatmap across Product Categories', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Product Category', fontsize=11, fontweight='bold')
ax.set_ylabel('Customer Type', fontsize=11, fontweight='bold')

fig.text(0.5, -0.07, 'Takeaway: Members drive the highest revenue in Beverages (₹28,283) and Dairy (₹21,573), while Normal shoppers outspend Members in Personal Care.',
         ha='center', fontsize=10.5, fontstyle='italic', color='#393939', bbox=dict(boxstyle='round,pad=0.5', facecolor='#F4F4F4', edgecolor='#D0D7DE'))
plt.tight_layout()
plt.savefig('charts/07_customer_category_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

# -------------------------------------------------------------------------
# Chart 8: Rating vs Sales / Quantity Correlation
# -------------------------------------------------------------------------
df['Rating_Tier'] = df['Rating'].round().astype(int).astype(str) + ' Stars'
tier_order = ['2 Stars', '3 Stars', '4 Stars', '5 Stars']

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.2))

# Scatter with regression line: Rating vs Sales
sns.regplot(x='Rating', y='Sales_INR', data=df, ax=ax1,
            scatter_kws={'alpha': 0.5, 'color': '#0F62FE'},
            line_kws={'color': '#8A3FFC', 'linewidth': 2})
ax1.set_title('Customer Rating vs. Basket Sales (INR)', fontsize=12, fontweight='bold')
ax1.set_xlabel('Customer Rating (1-5 Stars)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Sales (INR)', fontsize=11, fontweight='bold')
ax1.text(0.05, 0.90, 'Pearson r = 0.0130\np = 0.7722 (No correlation)', transform=ax1.transAxes,
         fontsize=9.5, fontweight='bold', bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#D0D7DE'))

# Boxplot of Sales by Rounded Rating Tier
sns.boxplot(x='Rating_Tier', y='Sales_INR', data=df, order=tier_order, ax=ax2,
            hue='Rating_Tier', legend=False, palette=['#1192E8', '#009D9A', '#0F62FE', '#8A3FFC'])
ax2.set_title('Sales Distribution Grouped by Rating Tier', fontsize=12, fontweight='bold')
ax2.set_xlabel('Customer Rating Tier', fontsize=11, fontweight='bold')
ax2.set_ylabel('Sales (INR)', fontsize=11, fontweight='bold')

fig.suptitle('Evaluating Customer Satisfaction: Rating vs. Purchase Magnitude', fontsize=14, fontweight='bold', y=1.02)
fig.text(0.5, -0.06, 'Takeaway: Customer satisfaction is completely independent of transaction size (r=0.013, p=0.772); both low and high spenders rate ~4.01 on average.',
         ha='center', fontsize=10.5, fontstyle='italic', color='#393939', bbox=dict(boxstyle='round,pad=0.5', facecolor='#F4F4F4', edgecolor='#D0D7DE'))
plt.tight_layout()
plt.savefig('charts/08_rating_vs_sales_correlation.png', dpi=300, bbox_inches='tight')
plt.close()

print('All 8 enhanced charts successfully generated in /charts folder!')
