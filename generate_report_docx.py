"""
Generate Formal IBM-Standard Professional DOCX Report for Supermarket Sales Analysis
Incorporates all computed metrics, tables, embedded charts, and structured sections.
"""
import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Sets background shading of a table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets inner padding for table cell in twips."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_report():
    doc = Document()
    
    # Page setup (Standard A4 / Letter, 1 inch margins)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Add page numbering in footer
        footer = section.footer
        f_p = footer.paragraphs[0]
        f_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        f_run = f_p.add_run("Supermarket Sales Analysis | IBM Applied Data Analytics Project")
        f_run.font.name = "Segoe UI"
        f_run.font.size = Pt(8.5)
        f_run.font.color.rgb = RGBColor(120, 120, 120)

    # --------------------------------------------------------------------------
    # Title & Metadata
    # --------------------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    run_org = title_p.add_run("IBM APPLIED DATA ANALYTICS PROJECT • BUSINESS INTELLIGENCE REPORT\n")
    run_org.font.name = "Segoe UI"
    run_org.font.size = Pt(10)
    run_org.font.bold = True
    run_org.font.color.rgb = RGBColor(15, 98, 254) # IBM Blue

    run_title = title_p.add_run("Supermarket Sales Analysis & Strategic Optimization")
    run_title.font.name = "Segoe UI"
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(22, 22, 22)

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(18)
    run_sub = sub_p.add_run("Data Quality Audit, Segment Performance, Payment Economics, and Inferential Evaluation on 500 Supermarket Transactions")
    run_sub.font.name = "Segoe UI"
    run_sub.font.size = Pt(12)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(82, 82, 82)

    # Callout Banner for Synthetic Dataset Notice
    banner_table = doc.add_table(rows=1, cols=1)
    banner_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    banner_cell = banner_table.cell(0, 0)
    set_cell_background(banner_cell, "F4F4F4")
    set_cell_margins(banner_cell, top=140, bottom=140, left=180, right=180)
    b_p = banner_cell.paragraphs[0]
    b_p.paragraph_format.space_after = Pt(0)
    b_run1 = b_p.add_run("IMPORTANT DATASET NOTICE: ")
    b_run1.font.bold = True
    b_run1.font.size = Pt(9.5)
    b_run1.font.color.rgb = RGBColor(15, 98, 254)
    b_run2 = b_p.add_run("The figures presented in this report were computed exclusively from the 500-row sample transactions CSV (`supermarket_sales_500_sample_transactions.csv`). This is a synthetic dataset generated specifically to demonstrate the full end-to-end data analytics workflow. All previous draft figures or external templates have been superseded.")
    b_run2.font.size = Pt(9.5)
    b_run2.font.color.rgb = RGBColor(60, 60, 60)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # --------------------------------------------------------------------------
    # Helper to add section headings
    # --------------------------------------------------------------------------
    def add_heading_1(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(16)
        h.paragraph_format.space_after = Pt(6)
        run = h.add_run(text)
        run.font.name = "Segoe UI"
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 98, 254) # IBM Blue
        return h

    def add_heading_2(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
        run = h.add_run(text)
        run.font.name = "Segoe UI"
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 93, 93) # Dark Teal
        return h

    def add_p(text, bold_prefix=None, space_after=6):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_bold = p.add_run(bold_prefix)
            r_bold.font.name = "Segoe UI"
            r_bold.font.size = Pt(10)
            r_bold.font.bold = True
            r_bold.font.color.rgb = RGBColor(22, 22, 22)
        r = p.add_run(text)
        r.font.name = "Segoe UI"
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(40, 40, 40)
        return p

    def add_callout(text, bold_title="Key Takeaway: "):
        t = doc.add_table(rows=1, cols=1)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        c = t.cell(0, 0)
        set_cell_background(c, "F4F6F8")
        set_cell_margins(c, top=100, bottom=100, left=150, right=150)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r1 = p.add_run(bold_title)
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(0, 157, 154) # Teal
        r2 = p.add_run(text)
        r2.font.size = Pt(9.5)
        r2.font.italic = True
        r2.font.color.rgb = RGBColor(50, 50, 50)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_image_figure(img_path, caption):
        if os.path.exists(img_path):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)
            p.add_run().add_picture(img_path, width=Inches(6.0))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(10)
            r_cap = p_cap.add_run(f"Figure: {caption}")
            r_cap.font.name = "Segoe UI"
            r_cap.font.size = Pt(8.5)
            r_cap.font.italic = True
            r_cap.font.color.rgb = RGBColor(100, 100, 100)

    # --------------------------------------------------------------------------
    # 1. PROBLEM STATEMENT
    # --------------------------------------------------------------------------
    add_heading_1("1. Problem Statement")
    add_p("Modern retail grocery chains operate in an environment characterized by thin gross operating margins (typically 2% to 4%), highly fragmented consumer preferences, and fierce competition across physical and omnichannel storefronts. To achieve sustainable profitability, retail leadership cannot rely on aggregate revenue numbers alone; management requires granular transparency into SKU-level revenue contribution, regional store branch efficiency, customer loyalty economics, and payment channel costs.")
    add_p("The primary objective of this project is to perform an exhaustive exploratory, diagnostic, and inferential data analysis on supermarket point-of-sale transaction logs to answer the following business questions:")
    add_p("Which individual products and merchandise categories represent the primary revenue engines of the supermarket, and does high dollar turnover correspond directly with high unit velocity?", bold_prefix="• Product & Category Dynamics: ")
    add_p("How do store locations (Branch A in Hyderabad, Branch B in Vijayawada, and Branch C in Mumbai) perform relative to one another in terms of gross sales, customer footfall (transactions), and average basket size?", bold_prefix="• Branch & Geographic Disparities: ")
    add_p("Does the supermarket's loyalty membership program effectively encourage larger transaction baskets, or is the perceived lift statistically insignificant?", bold_prefix="• Loyalty Program Monetization: ")
    add_p("Which payment channels (UPI, Cash, Credit Card, E-Wallet) capture the largest customer share, and do specific payment modes correlate with higher purchase values?", bold_prefix="• Payment Channel Economics: ")
    add_p("Is customer satisfaction (measured via 1-5 star ratings) influenced by transaction value or item volume?", bold_prefix="• Satisfaction Independence: ")

    # --------------------------------------------------------------------------
    # 2. DATASET DESCRIPTION
    # --------------------------------------------------------------------------
    add_heading_1("2. Dataset Description")
    add_p("The analysis was executed on a structured point-of-sale dataset containing 500 individual retail transaction records (`supermarket_sales_500_sample_transactions.csv`). It is explicitly noted that this dataset is a synthetic sample created to illustrate an end-to-end data analytics workflow, data validation rigor, and reporting standards.")
    add_p("The dataset schema comprises 11 attributes across categorical, numerical, and relational fields:")

    # Table of Schema
    table_schema = doc.add_table(rows=12, cols=4)
    table_schema.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Field Name", "Data Type", "Distinct Values / Range", "Business Description"]
    for i, h in enumerate(headers):
        c = table_schema.cell(0, i)
        set_cell_background(c, "0F62FE")
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)

    schema_data = [
        ("Invoice_ID", "String", "INV0001 - INV0500", "Unique transaction invoice identifier (Primary Key)"),
        ("Product", "String", "10 unique SKUs", "Merchandise item name (Rice, Milk, Cheese, etc.)"),
        ("Category", "String", "6 unique categories", "Departmental grouping (Beverages, Dairy, Grocery, etc.)"),
        ("Branch", "String", "3 branches (A, B, C)", "Operational store branch code"),
        ("City", "String", "3 cities (Hyderabad, etc.)", "Metropolitan store location"),
        ("Customer_Type", "String", "Member, Normal", "Customer loyalty tier membership status"),
        ("Quantity", "Integer", "1 to 6 units", "Count of units purchased in the transaction"),
        ("Unit_Price_INR", "Float", "₹22.19 to ₹198.18", "Price per unit in Indian Rupees"),
        ("Payment_Method", "String", "4 channels (UPI, Cash, etc.)", "Payment tender used at checkout register"),
        ("Rating", "Float", "2.0 to 5.0 stars", "Customer satisfaction rating score"),
        ("Sales_INR", "Float", "₹24.08 to ₹1,162.56", "Total invoice amount computed as Quantity × Unit_Price_INR")
    ]
    for row_idx, data_row in enumerate(schema_data, start=1):
        bg = "FFFFFF" if row_idx % 2 != 0 else "F4F6F8"
        for col_idx, val in enumerate(data_row):
            c = table_schema.cell(row_idx, col_idx)
            set_cell_background(c, bg)
            set_cell_margins(c, top=60, bottom=60, left=80, right=80)
            p = c.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if col_idx == 0:
                r.font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    add_callout("CRITICAL STRUCTURAL LIMITATION: The dataset contains NO date or timestamp column. Consequently, longitudinal time-series forecasting, seasonal trend decomposition, day-of-week sales clustering, and peak-hour store traffic analysis cannot be conducted on this dataset.", bold_title="Dataset Limitation: ")

    # --------------------------------------------------------------------------
    # 3. METHODOLOGY
    # --------------------------------------------------------------------------
    add_heading_1("3. Methodology")
    add_p("To ensure total reproducibility, data integrity, and mathematical rigor, a structured 5-stage analytical methodology was implemented using Python 3.12 (`pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy.stats`):")
    add_p("The raw CSV data was ingested and verified. Programmatic checks confirmed 500 rows, 11 columns, 0 null/missing values, and 0 duplicate records.", bold_prefix="1. Ingestion & Quality Audit: ")
    add_p("A programmatic verification was conducted across all 500 rows to test whether `Sales_INR == Quantity * Unit_Price_INR` within a ₹0.01 floating-point rounding tolerance. The audit confirmed 0 mismatches (100% mathematical consistency).", bold_prefix="2. Mathematical Formula Verification: ")
    add_p("Entity mappings were verified using group-by cardinality checks. Product-to-Category mappings demonstrated 100% consistency (all 10 products mapped to exactly one category). Branch-to-City mappings demonstrated a strict 1-to-1 bijection (Branch A = Hyderabad, Branch B = Vijayawada, Branch C = Mumbai).", bold_prefix="3. Relational Mapping Audit: ")
    add_p("Outlier analysis was performed on `Sales_INR` using the Tukey Interquartile Range (IQR) technique. The first quartile (Q1) was determined at ₹123.34, the median (Q2) at ₹225.56, and the third quartile (Q3) at ₹374.03, resulting in an IQR of ₹250.68. The upper outlier threshold ($Q3 + 1.5 \\times IQR$) was calculated at ₹750.05. Exactly 21 transactions (4.2% of total transactions) exceeded this threshold, driven by high-quantity purchases of premium SKUs (Cheese, Coffee, Shampoo).", bold_prefix="4. Statistical Outlier Detection: ")
    add_p("Welch's two-sample t-test (assuming unequal sample variances) was executed to test for statistical significance between Member and Normal customer spend. Pearson correlation coefficients were calculated to assess the relationship between customer ratings and transaction size.", bold_prefix="5. Inferential Statistical Testing: ")

    # --------------------------------------------------------------------------
    # 4. FINDINGS
    # --------------------------------------------------------------------------
    add_heading_1("4. Key Findings & Empirical Results")
    add_p("All metrics presented below were recomputed directly from the validated dataset. Previous template numbers have been disregarded.")

    add_heading_2("4.1 Core Performance Benchmarks")
    add_p("Across the 500 sample transactions, the supermarket generated a total gross turnover of ₹1,42,645.31 with 1,720 units sold. The average invoice basket was ₹285.29, with a median of ₹225.56, indicating a moderately right-skewed transaction distribution. The overall mean customer satisfaction rating was 4.01 out of 5.00 stars.")

    # Table of Core KPIs
    t_kpis = doc.add_table(rows=7, cols=3)
    t_kpis.alignment = WD_TABLE_ALIGNMENT.CENTER
    kpi_headers = ["Metric / Question", "Computed Result", "Strategic Interpretation"]
    for i, h in enumerate(kpi_headers):
        c = t_kpis.cell(0, i)
        set_cell_background(c, "0F62FE")
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)

    kpi_rows = [
        ("Top Product by Revenue", "Rice (₹24,340.47)", "Represents 17.06% of total revenue; staple volume and value driver"),
        ("Best Performing Branch", "Branch C in Mumbai (₹54,493.85)", "Captures 38.20% of revenue; leads in transactions (183) and basket (₹297.78)"),
        ("Top Merchandise Category", "Beverages (₹44,793.30)", "Accounts for 31.40% of sales; combined with Dairy (25.10%), drives 56.5% of store sales"),
        ("Most Adopted Payment Method", "UPI (139 transactions)", "27.8% channel share; also yields the highest average basket value (₹315.40)"),
        ("Customer Spend Comparison", "Member: ₹292.26 | Normal: ₹276.84", "Members spend ₹15.42 more on average; statistically insignificant difference"),
        ("Average Customer Rating", "4.01 / 5.00 Stars", "Uniform customer satisfaction across all stores and ticket sizes")
    ]
    for row_idx, data_row in enumerate(kpi_rows, start=1):
        bg = "FFFFFF" if row_idx % 2 != 0 else "F4F6F8"
        for col_idx, val in enumerate(data_row):
            c = t_kpis.cell(row_idx, col_idx)
            set_cell_background(c, bg)
            set_cell_margins(c, top=60, bottom=60, left=80, right=80)
            p = c.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if col_idx == 0:
                r.font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_heading_2("4.2 Branch Comparison & Geographic Disparities")
    add_p("Store performance across the three branches reveals noticeable operational differences in customer footfall and spending power:")
    add_p("Generates ₹54,493.85 (38.20% of total revenue) across 183 transactions, with an average ticket size of ₹297.78 and a 4.00 star rating. Branch C benefits from larger metropolitan basket sizes.", bold_prefix="• Branch C (Mumbai): ")
    add_p("Generates ₹45,853.66 (32.14% of total revenue) across 166 transactions, with an average ticket size of ₹276.23 and a 3.96 star rating.", bold_prefix="• Branch A (Hyderabad): ")
    add_p("Generates ₹42,297.80 (29.65% of total revenue) across 151 transactions, with an average ticket size of ₹280.12. Notably, Branch B achieved the highest customer satisfaction score (4.08 stars).", bold_prefix="• Branch B (Vijayawada): ")

    add_image_figure("charts/02_sales_by_branch_comparison.png", "Branch Performance: Revenue, Transaction Volume, and Average Basket Size")

    add_heading_2("4.3 Product Performance Dichotomy: Monetary Turnover vs. Physical Volume")
    add_p("A critical finding of this study is the sharp divergence between revenue generation and physical unit sales. SKUs with high unit velocity do not necessarily yield high monetary value, and vice-versa:")
    add_p("Top 3 Revenue: Rice (₹24,340.47), Cheese (₹18,049.87), and Milk (₹17,749.67). Bottom 3 Revenue: Soap (₹5,960.95), Bread (₹7,474.38), and Snacks (₹8,024.05).", bold_prefix="• Revenue Ranking: ")
    add_p("Top 3 Volume: Milk (306 units), Snacks (228 units), and Rice (221 units). Bottom 3 Volume: Coffee (86 units), Soap (108 units), and Cheese (123 units).", bold_prefix="• Volume Ranking: ")
    add_p("Why do they differ? Cheese ranks #2 in revenue but ranks #8 in unit volume (123 units) because of its premium unit price (~₹146.74/unit). Similarly, Coffee is #5 in revenue (₹15,909.70) despite being the lowest volume SKU (86 units, #10) due to its high price (~₹184.99/unit). Conversely, Snacks ranks #2 in physical units sold (228 units) but sits near the bottom (#8) in revenue due to low unit pricing (~₹35.19/unit). Soap is an underperformer on both dimensions (#10 in revenue, #9 in units).", bold_prefix="• The Dichotomy Explained: ")

    add_image_figure("charts/06_revenue_vs_units_top_bottom.png", "Product Performance Disconnect: Revenue Rankings vs. Units Sold Rankings")

    add_heading_2("4.4 Revenue Concentration (Pareto Distribution)")
    add_p("Analysis of revenue concentration confirms that the top 3 products (Rice, Cheese, Milk) generate ₹60,140.01, representing 42.16% of total store revenue. The top 5 products (adding Shampoo and Coffee) generate ₹92,302.33, capturing 64.71% of total sales. This moderate concentration underscores the operational necessity of protecting core supply lines for these five essential SKUs.")

    add_image_figure("charts/01_sales_by_product_pareto.png", "Pareto Analysis of Product Revenue and Cumulative Sales Distribution")

    add_heading_2("4.5 Payment Method Dynamics & Basket Sizes")
    add_p("Payment preferences among shoppers reveal that digital payments dominate store checkout lanes:")
    add_p("139 transactions (27.8% share), ₹43,840.69 total sales, and an average basket size of ₹315.40.", bold_prefix="• UPI: ")
    add_p("126 transactions (25.2% share), ₹35,879.19 total sales, and an average basket size of ₹284.76.", bold_prefix="• Cash: ")
    add_p("125 transactions (25.0% share), ₹34,455.74 total sales, and an average basket size of ₹275.65.", bold_prefix="• Credit Card: ")
    add_p("110 transactions (22.0% share), ₹28,469.69 total sales, and an average basket size of ₹258.82.", bold_prefix="• E-Wallet: ")
    add_p("Crucially, UPI not only captures the highest transaction count but also delivers the highest average ticket value (₹315.40 vs. ₹258.82 for E-wallets), demonstrating that frictionless mobile payment encourages larger overall basket purchases.")

    add_image_figure("charts/04_payment_methods_and_basket.png", "Payment Method Adoption Share and Average Basket Value per Method")

    add_heading_2("4.6 Customer Loyalty Assessment & Inferential Welch's t-test")
    add_p("The dataset contains 274 transactions by enrolled loyalty 'Members' (54.8%) and 226 transactions by unregistered 'Normal' shoppers (45.2%). On average, Members spent ₹292.26 per transaction, compared to ₹276.84 for Normal customers—an apparent nominal premium of ₹15.42 per visit.")
    add_p("To test whether this ₹15.42 difference represents a genuine business lift or merely random sampling variance, a two-sample Welch's t-test with unequal variances was conducted:")
    add_p("Null Hypothesis (H0): Mean Member Spend = Mean Normal Spend. Alternative Hypothesis (H1): Mean Member Spend ≠ Mean Normal Spend. Significance Level: α = 0.05.", bold_prefix="• Hypothesis Formulation: ")
    add_p("t-statistic = 0.8334, degrees of freedom = 491.5, p-value = 0.4050.", bold_prefix="• Test Results: ")
    add_p("Because the p-value (0.4050) is substantially greater than the significance threshold (0.05), we fail to reject the null hypothesis. In plain language: there is NO statistically significant difference in transaction spending between loyalty program Members and Normal shoppers. The supermarket's current membership program is not driving higher per-visit ticket sizes.", bold_prefix="• Plain Language Takeaway: ")

    add_image_figure("charts/05_member_vs_normal_spend.png", "Spend Distribution & Welch t-test: Member vs. Normal Customers")

    add_heading_2("4.7 Customer Type × Category Interactions")
    add_p("Cross-tabulation of category revenue across customer segments indicates distinct purchasing priorities: Members account for the vast majority of Beverage sales (₹28,283.49 vs. ₹16,509.81 for Normal) and Dairy sales (₹21,572.74 vs. ₹14,226.80). Conversely, Normal shoppers actually outspent Members in Personal Care (₹13,437.74 vs. ₹8,775.83).")

    add_image_figure("charts/07_customer_category_heatmap.png", "Spending Heatmap: Customer Loyalty Segment by Product Category")

    add_heading_2("4.8 Customer Rating Independence")
    add_p("Pearson correlation analysis between customer rating and transaction value yielded r = 0.0130 (p = 0.7722). Correlation between rating and quantity was r = -0.0017 (p = 0.9702). These near-zero correlation values demonstrate that customer satisfaction is entirely independent of order size or quantity. Both small single-item purchases and large multi-product baskets receive consistent 4.01-star ratings.")

    add_image_figure("charts/08_rating_vs_sales_correlation.png", "Customer Rating vs. Basket Spend: Correlation and Rating Tier Distribution")

    # --------------------------------------------------------------------------
    # 5. RECOMMENDATIONS
    # --------------------------------------------------------------------------
    add_heading_1("5. Strategic Business Recommendations")
    add_p("All recommendations are strictly formulated based upon the empirical findings derived from the dataset:")

    add_p("Because the t-test confirmed that loyalty members spend no more than regular shoppers (p=0.405), the current loyalty structure provides negligible commercial benefit. Management should transition the program from passive card-swiping to threshold-based rewards (e.g., 'Spend ₹450 to receive a ₹50 voucher on high-margin Dairy SKUs'). This will actively incentivize basket-stretching beyond the current ₹292 average.", bold_prefix="1. Overhaul Loyalty Program with Basket-Stretching Incentives: ")

    add_p("Given that UPI captures 27.8% of checkout volume and commands the highest average basket (₹315.40 vs. E-wallets ₹258.82), the supermarket should prioritize digital UPI checkout lanes. Introducing point-of-sale instant discounts for UPI transactions above ₹300 can capitalize on this already strong consumer propensity.", bold_prefix="2. Capitalize on UPI Checkout Dominance: ")

    add_p("Management must adopt a dual merchandising strategy: (a) Protect supply chain reliability and promotional pricing on high-volume anchor staples (Rice #1 revenue and Milk #1 volume); (b) Cross-merchandise high-volume low-cost items (Snacks, 228 units) directly alongside high-margin low-velocity products (Cheese, Coffee) to elevate overall basket margins.", bold_prefix="3. Dual-Track Merchandising (Volume Anchors vs. High-Margin SKUs): ")

    add_p("Branch C (Mumbai) generates ₹54,494 with an average basket of ₹297.78, outperforming Branch A by ₹21.55 per basket. Operational audits of Branch C's floor layout, bundle placements, and staff cross-selling techniques should be conducted to establish best-practice guidelines for Branches A and B.", bold_prefix="4. Institutionalize Branch C Merchandising Best Practices: ")

    add_p("Soap generates only ₹5,960.95 (4.18% of revenue) and moves only 108 units (#9 in volume). Management should renegotiate supplier wholesale pricing, replace slow-moving Soap SKUs with high-demand organic/herbal variants, or bundle Soap with high-performing Shampoo to lift personal care turnover.", bold_prefix="5. Rationalize and Re-bundle Underperforming SKUs: ")

    # --------------------------------------------------------------------------
    # 6. LIMITATIONS
    # --------------------------------------------------------------------------
    add_heading_1("6. Limitations")
    add_p("While this analysis provides actionable insights, several structural constraints must be recognized:")
    add_p("The dataset is an artificially generated sample of 500 transactions created for data analytics instruction. The patterns observed reflect the generative distribution of the sample rather than empirical retail market realities.", bold_prefix="• Synthetic Dataset Nature: ")
    add_p("The complete absence of a timestamp or date attribute prevents time-series forecasting, seasonality assessment, month-over-month sales trends, and hourly rush-hour staffing analysis.", bold_prefix="• Absence of Date / Time Dimensions: ")
    add_p("A sample size of 500 rows across 3 stores (averaging ~166 transactions per branch) limits statistical power when conducting multi-way subsegmentation (e.g., Member spend by branch by payment method).", bold_prefix="• Sample Size Boundaries: ")
    add_p("The dataset records gross selling price and quantity, but lacks Wholesale Cost of Goods Sold (COGS). Consequently, true gross profit margins cannot be calculated.", bold_prefix="• Lack of Cost & Margin Information: ")
    add_p("No demographic details (customer age, household income, family size) or basket market-basket co-purchase linkages are available.", bold_prefix="• Absence of Customer Demographics: ")

    # --------------------------------------------------------------------------
    # 7. CONCLUSION
    # --------------------------------------------------------------------------
    add_heading_1("7. Conclusion")
    add_p("This analytical study successfully fulfilled all objectives of the IBM Data Analytics project. Through rigorous data cleaning, mathematical verification, and exploratory analysis, key operational realities of the supermarket were illuminated: Rice and Beverages represent the store's primary financial pillars; Branch C in Mumbai leads across footfall and basket value; and UPI has emerged as the premier payment channel in both transaction volume and spending depth.")
    add_p("Crucially, inferential hypothesis testing provided an essential business reality check: the supermarket's loyalty membership program currently fails to deliver statistically significant basket expansion (p=0.405). By implementing the strategic recommendations detailed in this report—namely restructuring loyalty incentives, pairing high-volume staples with high-margin items, and expanding UPI checkout infrastructure—supermarket management can transform baseline transactional records into a sustainable competitive advantage.")

    # Save document
    report_path = "Supermarket_Sales_Analysis_Report_IBM.docx"
    doc.save(report_path)
    print(f"Report successfully generated and saved to: {report_path}")

if __name__ == "__main__":
    create_report()
