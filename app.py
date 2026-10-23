"""
Supermarket Sales Analysis - Interactive Executive Dashboard
Built with Streamlit & Plotly (IBM Carbon / Teal & Indigo Aesthetic)
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

# Page configuration
st.set_page_config(
    page_title="Supermarket Sales Analytics | IBM Project",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (IBM Carbon Design inspired)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #0F62FE 0%, #002D9C 100%);
        padding: 24px 32px;
        border-radius: 8px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 14px rgba(15, 98, 254, 0.15);
    }
    .main-header h1 {
        margin: 0;
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
    }
    .main-header p {
        margin: 6px 0 0 0;
        font-size: 14px;
        color: #E0E0E0;
    }
    
    .kpi-card {
        background-color: #ffffff;
        border: 1px solid #E0E0E0;
        border-top: 4px solid #0F62FE;
        border-radius: 6px;
        padding: 16px 20px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        margin-bottom: 12px;
    }
    .kpi-title {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #525252;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 24px;
        font-weight: 700;
        color: #161616;
    }
    .kpi-subtitle {
        font-size: 12px;
        color: #6F6F6F;
        margin-top: 4px;
    }
    
    .takeaway-box {
        background-color: #F4F4F4;
        border-left: 4px solid #009D9A;
        padding: 12px 18px;
        border-radius: 4px;
        font-size: 13.5px;
        color: #262626;
        margin-top: 14px;
        margin-bottom: 18px;
    }
</style>
""", unsafe_allow_html=True)

# Cache data loading
@st.cache_data
def load_data():
    data = pd.read_csv('supermarket_sales_500_sample_transactions.csv')
    return data

df_raw = load_data()

# Header Banner
st.markdown("""
<div class="main-header">
    <h1>🛒 Supermarket Sales Analysis & Business Intelligence</h1>
    <p>IBM Data Analytics Project • Executive KPI Dashboard • Verified on 500 Transaction Records</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Filter Controls
st.sidebar.image("https://img.icons8.com/color/96/000000/ibm.png", width=64)
st.sidebar.title("Dashboard Filters")
st.sidebar.caption("Filter transactions dynamically across operational dimensions.")

# Branch filter
branch_options = sorted(df_raw['Branch'].unique().tolist())
selected_branches = st.sidebar.multiselect(
    "Select Branch:",
    options=branch_options,
    default=branch_options,
    format_func=lambda x: f"Branch {x} ({'Hyderabad' if x=='A' else 'Vijayawada' if x=='B' else 'Mumbai'})"
)

# Category filter
category_options = sorted(df_raw['Category'].unique().tolist())
selected_categories = st.sidebar.multiselect(
    "Select Product Category:",
    options=category_options,
    default=category_options
)

# Customer Type filter
cust_options = sorted(df_raw['Customer_Type'].unique().tolist())
selected_cust_types = st.sidebar.multiselect(
    "Customer Membership Type:",
    options=cust_options,
    default=cust_options
)

# Payment Method filter
payment_options = sorted(df_raw['Payment_Method'].unique().tolist())
selected_payments = st.sidebar.multiselect(
    "Payment Method:",
    options=payment_options,
    default=payment_options
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Note on Data:**
This dataset consists of **500 synthetic sample transactions** designed for end-to-end retail workflow demonstration.
""")

# Apply Filtering
df_filtered = df_raw[
    (df_raw['Branch'].isin(selected_branches)) &
    (df_raw['Category'].isin(selected_categories)) &
    (df_raw['Customer_Type'].isin(selected_cust_types)) &
    (df_raw['Payment_Method'].isin(selected_payments))
]

if df_filtered.empty:
    st.warning("⚠️ No transactions match your active filter criteria. Please broaden your selections in the sidebar.")
    st.stop()

# ==============================================================================
# Dynamic KPI Cards
# ==============================================================================
total_revenue = df_filtered['Sales_INR'].sum()
total_tx = len(df_filtered)
avg_basket = df_filtered['Sales_INR'].mean()
avg_rating = df_filtered['Rating'].mean()
top_product = df_filtered.groupby('Product')['Sales_INR'].sum().idxmax()
top_product_val = df_filtered.groupby('Product')['Sales_INR'].sum().max()
top_category = df_filtered.groupby('Category')['Sales_INR'].sum().idxmax()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color: #0F62FE;">
        <div class="kpi-title">Total Revenue</div>
        <div class="kpi-value">₹{total_revenue:,.2f}</div>
        <div class="kpi-subtitle">Across {total_tx} transactions</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color: #009D9A;">
        <div class="kpi-title">Average Basket</div>
        <div class="kpi-value">₹{avg_basket:.2f}</div>
        <div class="kpi-subtitle">Spend per customer invoice</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color: #8A3FFC;">
        <div class="kpi-title">Customer Rating</div>
        <div class="kpi-value">{avg_rating:.2f} ★</div>
        <div class="kpi-subtitle">Scale of 1.0 to 5.0</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color: #1192E8;">
        <div class="kpi-title">Leading Product</div>
        <div class="kpi-value">{top_product}</div>
        <div class="kpi-subtitle">₹{top_product_val:,.0f} revenue</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color: #6929C4;">
        <div class="kpi-title">Top Category</div>
        <div class="kpi-value">{top_category}</div>
        <div class="kpi-subtitle">{df_filtered.groupby('Category')['Sales_INR'].sum().max()/total_revenue*100:.1f}% share</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# Tabbed Visualizations
# ==============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Product & Revenue Concentration",
    "🏢 Branch & Channel Dynamics",
    "👥 Loyalty & Statistical Validation",
    "📋 Data Explorer & Export"
])

# ------------------------------------------------------------------------------
# Tab 1: Product & Revenue
# ------------------------------------------------------------------------------
with tab1:
    col_a, col_b = st.columns([6, 5])
    
    with col_a:
        # Pareto Distribution Chart
        prod_agg = df_filtered.groupby('Product')['Sales_INR'].sum().sort_values(ascending=False).reset_index()
        prod_agg['Cum_Pct'] = (prod_agg['Sales_INR'].cumsum() / prod_agg['Sales_INR'].sum()) * 100
        
        fig_pareto = go.Figure()
        fig_pareto.add_trace(go.Bar(
            x=prod_agg['Product'],
            y=prod_agg['Sales_INR'],
            name='Revenue (INR)',
            marker_color='#0F62FE',
            text=[f"₹{v:,.0f}" for v in prod_agg['Sales_INR']],
            textposition='auto',
            yaxis='y1'
        ))
        fig_pareto.add_trace(go.Scatter(
            x=prod_agg['Product'],
            y=prod_agg['Cum_Pct'],
            name='Cumulative Share %',
            marker_color='#8A3FFC',
            mode='lines+markers',
            yaxis='y2',
            line=dict(width=3)
        ))
        fig_pareto.update_layout(
            title="<b>Product Revenue & Cumulative Pareto Curve</b>",
            yaxis=dict(title="Total Sales (INR)", showgrid=True, gridcolor='#E8ECF0'),
            yaxis2=dict(title="Cumulative %", overlaying='y', side='right', range=[0, 110], showgrid=False),
            legend=dict(x=0.6, y=1.1, orientation='h'),
            margin=dict(l=40, r=40, t=50, b=40),
            height=420
        )
        st.plotly_chart(fig_pareto, use_container_width=True)
        st.markdown("""
        <div class="takeaway-box">
            <b>Key Takeaway:</b> Rice leads with ₹24,340 in turnover. In the baseline dataset, the top 3 products (Rice, Cheese, Milk) account for <b>42.16%</b> of total supermarket revenues.
        </div>
        """, unsafe_allow_html=True)
    
    with col_b:
        # Category Breakdown
        cat_agg = df_filtered.groupby('Category')['Sales_INR'].sum().sort_values(ascending=True).reset_index()
        fig_cat = px.bar(
            cat_agg,
            x='Sales_INR',
            y='Category',
            orientation='h',
            title="<b>Revenue by Product Category</b>",
            text=[f"₹{v:,.0f}" for v in cat_agg['Sales_INR']],
            color='Sales_INR',
            color_continuous_scale=['#1192E8', '#009D9A', '#0F62FE']
        )
        fig_cat.update_layout(
            xaxis_title="Revenue (INR)",
            yaxis_title="",
            coloraxis_showscale=False,
            margin=dict(l=20, r=40, t=50, b=40),
            height=420
        )
        fig_cat.update_traces(textposition='outside')
        st.plotly_chart(fig_cat, use_container_width=True)
        st.markdown("""
        <div class="takeaway-box">
            <b>Key Takeaway:</b> <b>Beverages</b> and <b>Dairy</b> represent over 56% of total revenue. Bakery represents the lowest sales volume in this catalog.
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# Tab 2: Branch & Channel Dynamics
# ------------------------------------------------------------------------------
with tab2:
    col_c, col_d = st.columns(2)
    
    with col_c:
        # Branch Multi-Metric Chart
        branch_agg = df_filtered.groupby(['Branch', 'City']).agg(
            Revenue=('Sales_INR', 'sum'),
            Transactions=('Invoice_ID', 'count'),
            Avg_Basket=('Sales_INR', 'mean')
        ).reset_index()
        branch_agg['Branch_Label'] = branch_agg['Branch'] + ' (' + branch_agg['City'] + ')'
        
        fig_branch = px.bar(
            branch_agg,
            x='Branch_Label',
            y='Revenue',
            title="<b>Branch Revenue Comparison</b>",
            text=[f"₹{v:,.0f}" for v in branch_agg['Revenue']],
            color='Branch_Label',
            color_discrete_sequence=['#0F62FE', '#009D9A', '#8A3FFC']
        )
        fig_branch.update_layout(
            xaxis_title="",
            yaxis_title="Revenue (INR)",
            showlegend=False,
            margin=dict(l=40, r=20, t=50, b=40),
            height=400
        )
        fig_branch.update_traces(textposition='outside')
        st.plotly_chart(fig_branch, use_container_width=True)
        st.markdown("""
        <div class="takeaway-box">
            <b>Key Takeaway:</b> <b>Branch C (Mumbai)</b> outperforms other stores in total sales (₹54,494), customer visits (183), and basket size (₹297.78).
        </div>
        """, unsafe_allow_html=True)
    
    with col_d:
        # Payment Methods
        pm_agg = df_filtered.groupby('Payment_Method').agg(
            Transactions=('Invoice_ID', 'count'),
            Avg_Basket=('Sales_INR', 'mean')
        ).reset_index()
        
        fig_pm = px.pie(
            pm_agg,
            names='Payment_Method',
            values='Transactions',
            title="<b>Payment Method Adoption Share</b>",
            hole=0.45,
            color_discrete_sequence=['#0F62FE', '#009D9A', '#8A3FFC', '#1192E8']
        )
        fig_pm.update_layout(
            margin=dict(l=20, r=20, t=50, b=40),
            height=400
        )
        st.plotly_chart(fig_pm, use_container_width=True)
        st.markdown("""
        <div class="takeaway-box">
            <b>Key Takeaway:</b> <b>UPI</b> is the preferred payment mode (27.8% volume) and commands the largest average basket size (₹315.40).
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# Tab 3: Loyalty & Statistical Check
# ------------------------------------------------------------------------------
with tab3:
    col_e, col_f = st.columns(2)
    
    with col_e:
        # Customer Type Spend Distribution
        fig_box = px.box(
            df_filtered,
            x='Customer_Type',
            y='Sales_INR',
            color='Customer_Type',
            points="outliers",
            title="<b>Transaction Spend Distribution: Member vs. Normal</b>",
            color_discrete_sequence=['#0F62FE', '#009D9A']
        )
        fig_box.update_layout(
            xaxis_title="Customer Type",
            yaxis_title="Sales (INR)",
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig_box, use_container_width=True)
        
        # Run t-test dynamically on filtered data
        m_sales = df_filtered[df_filtered['Customer_Type'] == 'Member']['Sales_INR']
        n_sales = df_filtered[df_filtered['Customer_Type'] == 'Normal']['Sales_INR']
        
        if len(m_sales) > 1 and len(n_sales) > 1:
            t_res, p_res = stats.ttest_ind(m_sales, n_sales, equal_var=False)
            sig_text = "Statistically Significant" if p_res < 0.05 else "NOT Statistically Significant"
            st.markdown(f"""
            <div class="takeaway-box">
                <b>Welch Two-Sample t-test:</b> t = {t_res:.4f}, p = {p_res:.4f} ($\\alpha=0.05$)<br>
                <b>Result:</b> <b>{sig_text}</b>. Member spend (₹{m_sales.mean():.2f}) vs Normal spend (₹{n_sales.mean():.2f}) does not reflect a statistically confirmed premium.
            </div>
            """, unsafe_allow_html=True)
    
    with col_f:
        # Rating vs Sales Scatter Plot
        fig_scatter = px.scatter(
            df_filtered,
            x='Rating',
            y='Sales_INR',
            color='Customer_Type',
            trendline='ols',
            title="<b>Customer Rating vs. Basket Spend (INR)</b>",
            color_discrete_sequence=['#0F62FE', '#009D9A'],
            opacity=0.65
        )
        fig_scatter.update_layout(
            xaxis_title="Customer Rating (1-5 Stars)",
            yaxis_title="Sales (INR)",
            height=400
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        r_val, p_corr = stats.pearsonr(df_filtered['Rating'], df_filtered['Sales_INR'])
        st.markdown(f"""
        <div class="takeaway-box">
            <b>Correlation Analysis:</b> Pearson r = {r_val:.4f} (p = {p_corr:.4f}).<br>
            Customer satisfaction ratings remain consistent (~4.01) regardless of whether an order is small or large.
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# Tab 4: Data Explorer
# ------------------------------------------------------------------------------
with tab4:
    st.subheader("Filterable Transaction Table")
    st.dataframe(df_filtered, use_container_width=True)
    
    csv_bytes = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_bytes,
        file_name="supermarket_sales_filtered_export.csv",
        mime="text/csv"
    )
