"""
Supermarket Sales Analysis
Run: python supermarket_sales_analysis.py
Install: pip install pandas matplotlib
Dataset: supermarket_sales_500_sample_transactions.csv
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
DATA = BASE / "supermarket_sales_500_sample_transactions.csv"
OUT = BASE / "charts"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA)
print("Shape:", df.shape)
print("\nMissing values:\n", df.isna().sum())
print("Duplicate rows:", df.duplicated().sum())

# Clean and validate
df = df.drop_duplicates().copy()
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["Unit_Price_INR"] = pd.to_numeric(df["Unit_Price_INR"], errors="coerce")
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
df = df.dropna(subset=["Product", "Quantity", "Unit_Price_INR", "Rating"])
df = df[(df["Quantity"] > 0) & (df["Unit_Price_INR"] >= 0) & df["Rating"].between(1, 5)]
df["Sales_INR"] = (df["Quantity"] * df["Unit_Price_INR"]).round(2)

print("\nTotal sales (INR):", round(df["Sales_INR"].sum(), 2))
print("Average transaction (INR):", round(df["Sales_INR"].mean(), 2))
print("Average rating:", round(df["Rating"].mean(), 2))
print("\nSales by product:\n", df.groupby("Product")["Sales_INR"].sum().sort_values(ascending=False))
print("\nSales by branch:\n", df.groupby(["Branch", "City"])["Sales_INR"].sum().sort_values(ascending=False))
print("\nSales by category:\n", df.groupby("Category")["Sales_INR"].sum().sort_values(ascending=False))
print("\nPayment counts:\n", df["Payment_Method"].value_counts())
print("\nAverage spend by customer type:\n", df.groupby("Customer_Type")["Sales_INR"].mean().round(2))

charts = [
    ("Product", "Sales by Product", "barh"),
    ("Category", "Sales by Category", "bar"),
    ("Payment_Method", "Transactions by Payment Method", "count"),
]
for col, title, kind in charts:
    plt.figure(figsize=(9, 5))
    if kind == "count":
        df[col].value_counts().plot(kind="bar")
        plt.ylabel("Transactions")
    else:
        df.groupby(col)["Sales_INR"].sum().sort_values().plot(kind=kind)
        plt.ylabel("Sales (INR)")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(OUT / (col.lower() + ".png"), dpi=160)
    plt.close()

plt.figure(figsize=(8,5))
df.groupby(["Branch", "City"])["Sales_INR"].sum().plot(kind="bar")
plt.title("Sales by Branch")
plt.ylabel("Sales (INR)")
plt.tight_layout()
plt.savefig(OUT / "branch.png", dpi=160)
plt.close()

print(f"\nCharts saved in: {OUT}")
