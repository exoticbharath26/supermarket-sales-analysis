# Supermarket Sales Analysis — IBM Applied Data Analytics Project

## Project Overview
This project presents an end-to-end retail data analytics workflow built on supermarket point-of-sale transaction data. The project encompasses rigorous data quality audits, mathematical validation, exploratory data analysis (EDA), business intelligence aggregation, inferential statistical testing (Welch's t-test), interactive dashboard development, and a publication-quality executive business report.

> **Dataset Declaration:** The transaction log (`supermarket_sales_500_sample_transactions.csv`) comprises 500 synthetic sample records created specifically to demonstrate an end-to-end data analytics workflow. All calculations presented in this repository were computed directly from this CSV.

---

## Key Business Insights & Validated Findings
All figures are computed directly from `supermarket_sales_500_sample_transactions.csv`:
- **Total Revenue:** ₹1,42,645.31 across 500 transactions (1,720 physical units sold).
- **Top Product by Revenue:** **Rice** generates ₹24,340.47 (17.06% of store revenue).
- **Best Performing Branch:** **Branch C in Mumbai** dominates with ₹54,493.85 (38.20% revenue share, 183 transactions, ₹297.78 average basket).
- **Top Product Category:** **Beverages** generates ₹44,793.30 (31.40% share); together with Dairy (25.10%), these two departments drive 56.5% of total sales.
- **Leading Payment Method:** **UPI** is the most adopted method (139 transactions, 27.8% share) and commands the largest average basket size (₹315.40 vs. E-wallets ₹258.82).
- **Customer Loyalty Assessment (Welch's t-test):** Members spend an average of ₹292.26 vs. Normal customers ₹276.84 (+₹15.42 nominal difference). A two-sample Welch's t-test ($t = 0.8334, p = 0.4050 > 0.05$) confirms that this difference is **statistically insignificant**. Current membership does not yield larger basket sizes.
- **Product Revenue vs. Volume Disconnect:** Cheese is #2 in revenue (₹18,049.87) but #8 in unit volume (123 units) due to premium unit price; Snacks is #2 in volume (228 units) but #8 in revenue due to low price point.
- **Customer Satisfaction:** Uniform across spending levels ($r = 0.0130, p = 0.7722$), averaging 4.01 / 5.00 stars.

---

## Repository Structure & Deliverables

```
├── supermarket_sales_500_sample_transactions.csv  # Base transactional dataset (500 rows)
├── supermarket_sales_analysis.ipynb              # Executed Jupyter Notebook with complete analysis & outputs
├── app.py                                        # Interactive Streamlit Executive Dashboard
├── Supermarket_Sales_Analysis_Report_IBM.docx    # Formal Word Business Report (IBM structure)
├── analysis_results.json                         # Comprehensive machine-readable JSON metrics
├── generate_charts.py                            # Script generating all 8 enhanced charts
├── build_notebook.py                             # Script building and executing the Jupyter Notebook
├── generate_report_docx.py                       # Script assembling the Word Report
├── charts/                                       # 8 High-resolution (300 DPI) publication charts
│   ├── 01_sales_by_product_pareto.png
│   ├── 02_sales_by_branch_comparison.png
│   ├── 03_sales_by_category.png
│   ├── 04_payment_methods_and_basket.png
│   ├── 05_member_vs_normal_spend.png
│   ├── 06_revenue_vs_units_top_bottom.png
│   ├── 07_customer_category_heatmap.png
│   └── 08_rating_vs_sales_correlation.png
└── README.md                                     # Project documentation & summary
```

---

## How to Run & Reproduce

### 1. Environment Installation
Ensure Python 3.10+ is installed, then install required analytical packages:
```bash
pip install pandas numpy matplotlib seaborn scipy python-docx streamlit plotly statsmodels nbformat nbclient ipykernel
```

### 2. Run the Interactive Streamlit Dashboard
Launch the interactive web application with multi-select sidebar filters, dynamic KPI metric cards, and interactive charts:
```bash
streamlit run app.py
```

### 3. Open the Jupyter Notebook
Open `supermarket_sales_analysis.ipynb` in VS Code or Jupyter Lab:
```bash
jupyter lab supermarket_sales_analysis.ipynb
```

### 4. Regenerate All Visualizations & Report
```bash
python generate_charts.py
python build_notebook.py
python generate_report_docx.py
```

---

## Technical Audit & Validation Summary
1. **Mathematical Validation:** `Sales_INR == Quantity * Unit_Price_INR` checked on all 500 rows $\rightarrow$ 0 mismatches.
2. **Entity Consistency:** Product-to-Category (10 mappings) and Branch-to-City (3 mappings) are 100% bijective and consistent.
3. **Outlier Detection:** Tukey IQR on `Sales_INR` ($Q1 = ₹123.34, Q3 = ₹374.03, IQR = ₹250.68, Upper Cutoff = ₹750.05$) identified 21 premium high-ticket transactions.
4. **Statistical Testing:** Welch's t-test with unequal variances to evaluate loyalty lift ($p = 0.4050$).
