
SELECT
    SUM(CAST(Revenue AS REAL)) AS Total_Revenue,
    SUM(CAST(Expenses AS REAL)) AS Total_Expenses,
    SUM(CAST(Profit AS REAL)) AS Total_Profit
FROM Financial_Data;

SELECT
    strftime('%Y-%m', Date) AS Month,
    SUM(CAST(Revenue AS REAL)) AS Total_Revenue,
    SUM(CAST(Expenses AS REAL)) AS Total_Expenses,
    SUM(CAST(Profit AS REAL)) AS Total_Profit
FROM Financial_Data
GROUP BY strftime('%Y-%m', Date)
ORDER BY Month;

SELECT
    Department_ID,
    SUM(CAST(Revenue AS REAL)) AS Actual_Revenue,
    SUM(CAST(Budget_Revenue AS REAL)) AS Budget_Revenue,
    SUM(CAST(Expenses AS REAL)) AS Actual_Expenses,
    SUM(CAST(Budget_Expenses AS REAL)) AS Budget_Expenses,
    SUM(CAST(Revenue AS REAL))
      - SUM(CAST(Budget_Revenue AS REAL)) AS Revenue_Variance,
    SUM(CAST(Expenses AS REAL))
      - SUM(CAST(Budget_Expenses AS REAL)) AS Expense_Variance
FROM Financial_Data
GROUP BY Department_ID
ORDER BY Department_ID;

SELECT
    Department_ID,
    SUM(CAST(Revenue AS REAL)) AS Total_Revenue,
    SUM(CAST(Profit AS REAL)) AS Total_Profit,
    ROUND(
        SUM(CAST(Profit AS REAL)) * 100.0
        / NULLIF(SUM(CAST(Revenue AS REAL)), 0),
        2
    ) AS Profit_Margin_Percent
FROM Financial_Data
GROUP BY Department_ID
ORDER BY Profit_Margin_Percent DESC;
-- 1. Overall Financial Summary
SELECT
    COUNT(*) AS Total_Transactions,
    COUNT(DISTINCT Department_ID) AS Total_Departments,
    ROUND(SUM(CAST(Revenue AS REAL)), 2) AS Total_Revenue,
    ROUND(SUM(CAST(Expenses AS REAL)), 2) AS Total_Expenses,
    ROUND(SUM(CAST(Profit AS REAL)), 2) AS Total_Profit,
    ROUND(
        100.0 * SUM(CAST(Profit AS REAL))
        / NULLIF(SUM(CAST(Revenue AS REAL)), 0),
        2
    ) AS Overall_Profit_Margin
FROM Financial_Data;
-- 2. Department-wise Financial Analysis
SELECT
    Department_ID,
    SUM(CAST(Revenue AS REAL)) AS Total_Revenue,
    SUM(CAST(Expenses AS REAL)) AS Total_Expenses,
    SUM(CAST(Profit AS REAL)) AS Total_Profit
FROM Financial_Data
GROUP BY Department_ID
ORDER BY Total_Revenue DESC;
-- 3. Monthly Financial Analysis
SELECT
    strftime('%Y-%m', Date) AS Month,
    SUM(CAST(Revenue AS REAL)) AS Total_Revenue,
    SUM(CAST(Expenses AS REAL)) AS Total_Expenses,
    SUM(CAST(Profit AS REAL)) AS Total_Profit
FROM Financial_Data
GROUP BY strftime('%Y-%m', Date)
ORDER BY Month;
-- 4. Actual vs Budget Analysis
SELECT
    Department_ID,
    SUM(CAST(Revenue AS REAL)) AS Actual_Revenue,
    SUM(CAST(Budget_Revenue AS REAL)) AS Budget_Revenue,
    SUM(CAST(Revenue AS REAL))
        - SUM(CAST(Budget_Revenue AS REAL)) AS Revenue_Variance,
    SUM(CAST(Expenses AS REAL)) AS Actual_Expenses,
    SUM(CAST(Budget_Expenses AS REAL)) AS Budget_Expenses,
    SUM(CAST(Expenses AS REAL))
        - SUM(CAST(Budget_Expenses AS REAL)) AS Expense_Variance
FROM Financial_Data
GROUP BY Department_ID
ORDER BY Revenue_Variance DESC;
-- 5. Profit Margin Analysis by Department
SELECT
    Department_ID,
    ROUND(SUM(CAST(Revenue AS REAL)), 2) AS Total_Revenue,
    ROUND(SUM(CAST(Profit AS REAL)), 2) AS Total_Profit,
    ROUND(
        SUM(CAST(Profit AS REAL)) * 100.0
        / NULLIF(SUM(CAST(Revenue AS REAL)), 0),
        2
    ) AS Profit_Margin_Percentage
FROM Financial_Data
GROUP BY Department_ID
ORDER BY Profit_Margin_Percentage DESC;
-- 6. Revenue Performance Classification
SELECT
    Department_ID,
    SUM(CAST(Revenue AS REAL)) AS Actual_Revenue,
    SUM(CAST(Budget_Revenue AS REAL)) AS Budget_Revenue,
    CASE
        WHEN SUM(CAST(Revenue AS REAL))
             > SUM(CAST(Budget_Revenue AS REAL))
        THEN 'Above Budget'
        WHEN SUM(CAST(Revenue AS REAL))
             < SUM(CAST(Budget_Revenue AS REAL))
        THEN 'Below Budget'
        ELSE 'On Budget'
    END AS Revenue_Status
FROM Financial_Data
GROUP BY Department_ID
ORDER BY Actual_Revenue DESC;
-- 7. Missing Values Check
SELECT
    COUNT(*) AS Total_Records,
    SUM(CASE
        WHEN Transaction_ID IS NULL OR TRIM(Transaction_ID) = ''
        THEN 1 ELSE 0
    END) AS Missing_Transaction_ID,
    SUM(CASE
        WHEN Date IS NULL OR TRIM(Date) = ''
        THEN 1 ELSE 0
    END) AS Missing_Date,
    SUM(CASE
        WHEN Revenue IS NULL OR TRIM(Revenue) = ''
        THEN 1 ELSE 0
    END) AS Missing_Revenue,
    SUM(CASE
        WHEN Expenses IS NULL OR TRIM(Expenses) = ''
        THEN 1 ELSE 0
    END) AS Missing_Expenses
FROM Financial_Data;
-- 8. Duplicate Transactions Check
SELECT
    Transaction_ID,
    COUNT(*) AS Transaction_Count
FROM Financial_Data
GROUP BY Transaction_ID
HAVING COUNT(*) > 1
ORDER BY Transaction_Count DESC;
-- 9. Overall Financial Summary
SELECT
    COUNT(*) AS Total_Transactions,
    COUNT(DISTINCT Department_ID) AS Total_Departments,
    ROUND(SUM(CAST(Revenue AS REAL)), 2) AS Total_Revenue,
    ROUND(SUM(CAST(Expenses AS REAL)), 2) AS Total_Expenses,
    ROUND(SUM(CAST(Profit AS REAL)), 2) AS Total_Profit,
    ROUND(
        100.0 * SUM(CAST(Profit AS REAL))
        / NULLIF(SUM(CAST(Revenue AS REAL)), 0),
        2
    ) AS Overall_Profit_Margin
FROM Financial_Data;