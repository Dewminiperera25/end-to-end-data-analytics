
import pandas as pd

df = pd.read_csv("Financial_Data.csv")
df = df.dropna(subset=["Transaction_ID"]).copy()

numeric_columns = ["Revenue", "Expenses", "Profit"]

for col in numeric_columns:
    df[col] = pd.to_numeric(
        df[col].astype(str).str.replace(",", "", regex=False)
    )

# Correlation analysis
correlation_matrix = df[numeric_columns].corr()

print("===== CORRELATION MATRIX =====")
print(correlation_matrix.round(3))

print("\n===== REVENUE AND PROFIT CORRELATION =====")
print(round(correlation_matrix.loc["Revenue", "Profit"], 3))

print("\n===== EXPENSES AND PROFIT CORRELATION =====")
print(round(correlation_matrix.loc["Expenses", "Profit"], 3))

# Actual vs Budget Analysis

df["Revenue"] = pd.to_numeric(
    df["Revenue"].astype(str).str.replace(",", "", regex=False)
)

df["Budget_Revenue"] = pd.to_numeric(
    df["Budget_Revenue"].astype(str).str.replace(",", "", regex=False)
)

budget_analysis = df.groupby("Department_ID").agg(
    Actual_Revenue=("Revenue", "sum"),
    Budget_Revenue=("Budget_Revenue", "sum")
)

budget_analysis["Revenue_Gap"] = (
    budget_analysis["Actual_Revenue"]
    - budget_analysis["Budget_Revenue"]
)

budget_analysis["Achievement_%"] = (
    budget_analysis["Actual_Revenue"]
    / budget_analysis["Budget_Revenue"]
) * 100

print("\n===== ACTUAL VS BUDGET ANALYSIS =====")
print(budget_analysis.round(2))


# Expense Budget Analysis

df["Expenses"] = pd.to_numeric(
    df["Expenses"].astype(str).str.replace(",", "", regex=False)
)

df["Budget_Expenses"] = pd.to_numeric(
    df["Budget_Expenses"].astype(str).str.replace(",", "", regex=False)
)

expense_analysis = df.groupby("Department_ID").agg(
    Actual_Expenses=("Expenses", "sum"),
    Budget_Expenses=("Budget_Expenses", "sum")
)

expense_analysis["Budget_Savings"] = (
    expense_analysis["Budget_Expenses"]
    - expense_analysis["Actual_Expenses"]
)

expense_analysis["Budget_Utilization_%"] = (
    expense_analysis["Actual_Expenses"]
    / expense_analysis["Budget_Expenses"]
) * 100

print("\n===== EXPENSE BUDGET ANALYSIS =====")
print(expense_analysis.round(2))


import matplotlib.pyplot as plt

# Monthly Revenue and Profit Comparison
monthly_financials = df.groupby(
    pd.to_datetime(df["Date"]).dt.to_period("M")
).agg(
    Revenue=("Revenue", "sum"),
    Profit=("Profit", "sum")
)

monthly_financials.index = monthly_financials.index.astype(str)

plt.figure(figsize=(14, 6))

plt.plot(
    monthly_financials.index,
    monthly_financials["Revenue"],
    label="Revenue",
    marker="o"
)

plt.plot(
    monthly_financials.index,
    monthly_financials["Profit"],
    label="Profit",
    marker="o"
)

plt.title("Monthly Revenue vs Profit")
plt.xlabel("Month")
plt.ylabel("Amount")
plt.xticks(rotation=90)
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("monthly_revenue_vs_profit.png", dpi=300)
plt.show()


# Department-wise Profit Comparison

department_profit = df.groupby("Department_ID")["Profit"].sum()

department_profit = department_profit.sort_values(ascending=False)

plt.figure(figsize=(9, 5))

department_profit.plot(kind="bar")

plt.title("Total Profit by Department")
plt.xlabel("Department")
plt.ylabel("Total Profit")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("department_profit_comparison.png", dpi=300)
plt.show()

print("\n===== DEPARTMENT PROFIT RANKING =====")
print(department_profit.round(2))


# Key Business Insights

total_revenue = df["Revenue"].sum()
total_profit = df["Profit"].sum()
total_expenses = df["Expenses"].sum()

revenue_budget = df["Budget_Revenue"].sum()
expense_budget = df["Budget_Expenses"].sum()

profit_margin = (total_profit / total_revenue) * 100
revenue_achievement = (total_revenue / revenue_budget) * 100

department_summary = df.groupby("Department_ID").agg(
    Revenue=("Revenue", "sum"),
    Profit=("Profit", "sum"),
    Budget_Revenue=("Budget_Revenue", "sum")
)

department_summary["Profit_Margin_%"] = (
    department_summary["Profit"]
    / department_summary["Revenue"]
) * 100

top_profit_department = department_summary["Profit"].idxmax()
best_revenue_department = (
    department_summary["Revenue"] /
    department_summary["Budget_Revenue"]
).idxmax()

print("\n===== KEY BUSINESS INSIGHTS =====")
print(f"Total Revenue: {total_revenue:,.2f}")
print(f"Total Expenses: {total_expenses:,.2f}")
print(f"Total Profit: {total_profit:,.2f}")
print(f"Overall Profit Margin: {profit_margin:.2f}%")
print(f"Revenue Budget Achievement: {revenue_achievement:.2f}%")
print(f"Total Expense Budget Savings: {expense_budget - total_expenses:,.2f}")
print(f"Highest Profit Department: {top_profit_department}")
print(f"Best Revenue Target Achievement: {best_revenue_department}")


# Export Analysis Results to Excel

with pd.ExcelWriter("Financial_Analysis_Results.xlsx") as writer:

    # Overall financial summary
    overall_summary = pd.DataFrame({
        "Metric": [
            "Total Revenue",
            "Total Expenses",
            "Total Profit",
            "Profit Margin (%)",
            "Revenue Budget Achievement (%)",
            "Expense Budget Savings"
        ],
        "Value": [
            df["Revenue"].sum(),
            df["Expenses"].sum(),
            df["Profit"].sum(),
            (df["Profit"].sum() / df["Revenue"].sum()) * 100,
            (df["Revenue"].sum() / df["Budget_Revenue"].sum()) * 100,
            df["Budget_Expenses"].sum() - df["Expenses"].sum()
        ]
    })

    overall_summary.to_excel(
        writer, sheet_name="Overall Summary", index=False
    )

    # Department-wise performance
    department_summary = df.groupby("Department_ID").agg(
        Total_Revenue=("Revenue", "sum"),
        Total_Expenses=("Expenses", "sum"),
        Total_Profit=("Profit", "sum"),
        Budget_Revenue=("Budget_Revenue", "sum"),
        Budget_Expenses=("Budget_Expenses", "sum")
    )

    department_summary.to_excel(
        writer, sheet_name="Department Analysis"
    )

    # Monthly trends
    monthly_summary = df.groupby(
        pd.to_datetime(df["Date"]).dt.to_period("M")
    ).agg(
        Total_Revenue=("Revenue", "sum"),
        Total_Profit=("Profit", "sum")
    )

    monthly_summary.index = monthly_summary.index.astype(str)

    monthly_summary.to_excel(
        writer, sheet_name="Monthly Trends"
    )

print("\nExcel report exported successfully!")
