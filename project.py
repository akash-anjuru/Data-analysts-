# Import required libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Display plots inside notebook
# %matplotlib inline


# Load CSV file

df = pd.read_csv("Nassau Candy Distributor.csv")

# Display first 5 rows

print(df.head())
print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns)

print("\nDataset Information:")
print(df.info())

# Count missing values

print("\nMissing Values:")
print(df.isnull().sum())

# Remove Missing Values
df.dropna(inplace=True)

# Remove duplicate rows
df.drop_duplicates(inplace=True)

# Remove records where sales are zero

df = df[df['Sales'] > 0]

# Remove records where profit is negative

df = df[df['Gross Profit'] >= 0]
print("Records with negative profit removed successfully")
# Convert Order Date

df['Order Date'] = pd.to_datetime(
    df['Order Date'],
    dayfirst=True
)

# Convert Ship Date

df['Ship Date'] = pd.to_datetime(
    df['Ship Date'],
    dayfirst=True
)

print("Date conversion successful")
print(df[['Order Date', 'Ship Date']].head())

#Gross margin calculation
df['Gross Margin %'] = (
    df['Gross Profit'] / df['Sales']
) * 100

print("\nGross Margin %:")
print(df[['Product Name','Gross Margin %']].head())

#profit per unit calculation
df['Profit Per Unit'] = (
    df['Gross Profit'] / df['Units']
)

print("\nProfit Per Unit:")
print(df[['Product Name','Profit Per Unit']].head())

# Top Products by Profit Per Unit

profit_per_unit_analysis = (
    df.groupby('Product Name')['Profit Per Unit']
    .mean()
    .sort_values(ascending=False)
)

print("\nTop Products by Profit Per Unit")
print(profit_per_unit_analysis.head(10))
profit_per_unit_analysis.head(10).plot(
    kind='bar'
)

plt.title("Top Products by Profit Per Unit")
plt.ylabel("Profit Per Unit")
plt.show()

#revenue per unit calculation
df['Revenue Contribution %'] = (
    df['Sales'] / df['Sales'].sum()
) * 100

print("\nRevenue Contribution %:")
print(df[['Product Name','Revenue Contribution %']].head())

#profit contribution calculation
df['Profit Contribution %'] = (
    df['Gross Profit'] / df['Gross Profit'].sum()
) * 100

print("\nProfit Contribution %:")
print(df[['Product Name','Profit Contribution %']].head())

# Margin Volatility KPI

margin_volatility = df['Gross Margin %'].std()

print("\nMargin Volatility:")
print(round(margin_volatility,2))

#Top Products by Gross Profit
top_profit_products = (
    df.groupby('Product Name')['Gross Profit']
    .sum()
    .sort_values(ascending=False)
)

print(top_profit_products.head(10))

#Visualization
top_profit_products.head(10).plot(
    kind='bar'
)

plt.title("Top 10 Products by Gross Profit")
plt.ylabel("Gross Profit")
plt.show()

#Top Products by Gross Margin
margin_products = (
    df.groupby('Product Name')['Gross Margin %']
    .mean()
    .sort_values(ascending=False)
)

print(margin_products.head(10))
margin_products.head(10).plot(
    kind='bar'
)

plt.title("Top 10 Products by Gross Margin")
plt.ylabel("Gross Margin %")
plt.show()

#High Sales vs High Profit Analysis
product_analysis = (
    df.groupby('Product Name')
    .agg({
        'Sales':'sum',
        'Gross Profit':'sum'
    })
    .reset_index()
)

print(
    product_analysis.sort_values(
        by='Sales',
        ascending=False
    ).head(10)
)

#Scatter Plot
sns.scatterplot(
    data=product_analysis,
    x='Sales',
    y='Gross Profit'
)

plt.title("Sales vs Profit")
plt.show()

#Division-Level Performance Analysis
division_analysis = (
    df.groupby('Division')
    .agg({
        'Sales':'sum',
        'Gross Profit':'sum',
        'Gross Margin %':'mean'
    })
)

print(division_analysis)

#Division Profit Chart
division_analysis['Gross Profit'].plot(
    kind='bar'
)

plt.title("Division-wise Gross Profit")
plt.show()

#Revenue vs Profit Comparison
division_analysis[['Sales','Gross Profit']].plot(
    kind='bar'
)

plt.title("Revenue vs Profit by Division")
plt.show()

# Cost vs Sales Scatter Analysis

plt.figure(figsize=(8,6))

sns.scatterplot(
    data=df,
    x='Cost',
    y='Sales'
)

plt.title("Cost vs Sales Analysis")
plt.xlabel("Cost")
plt.ylabel("Sales")
plt.show()

# Cost Heavy Margin Poor Products

cost_margin = (
    df.groupby('Product Name')
    .agg({
        'Cost':'sum',
        'Gross Margin %':'mean'
    })
)

cost_heavy_margin_poor = cost_margin[
    (cost_margin['Cost'] >
     cost_margin['Cost'].mean()) &
    (cost_margin['Gross Margin %'] < 20)
]

print("\nCost Heavy Margin Poor Products")
print(cost_heavy_margin_poor)

# Pricing Inefficiency Detection

pricing_issue = (
    df.groupby('Product Name')
    .agg({
        'Sales':'sum',
        'Gross Margin %':'mean'
    })
)

pricing_issue = pricing_issue[
    (pricing_issue['Sales'] >
     pricing_issue['Sales'].mean()) &
    (pricing_issue['Gross Margin %'] < 20)
]

print("\nPricing Inefficiency Products")
print(pricing_issue)

#Pareto Analysis (80/20 Rule)
pareto = (
    df.groupby('Product Name')['Gross Profit']
    .sum()
    .sort_values(ascending=False)
)

pareto_df = pareto.reset_index()

pareto_df['Cumulative Profit %'] = (
    pareto_df['Gross Profit'].cumsum()
    / pareto_df['Gross Profit'].sum()
) * 100

print(pareto_df.head())

#Pareto Chart
plt.figure(figsize=(12,6))

plt.bar(
    pareto_df['Product Name'],
    pareto_df['Gross Profit']
)

plt.plot(
    pareto_df['Cumulative Profit %'],
    marker='o'
)

plt.xticks(rotation=90)

plt.title("Pareto Analysis")
plt.show()

# Products contributing 80% of profit

profit_80_products = pareto_df[
    pareto_df['Cumulative Profit %'] <= 80
]

print("\nProducts Contributing 80% Profit")
print(profit_80_products)

# Products Contributing 80% Revenue

revenue_pareto = (
    df.groupby('Product Name')['Sales']
    .sum()
    .sort_values(ascending=False)
)

revenue_df = revenue_pareto.reset_index()

revenue_df['Cumulative Revenue %'] = (
    revenue_df['Sales'].cumsum()
    / revenue_df['Sales'].sum()
) * 100

revenue_80_products = revenue_df[
    revenue_df['Cumulative Revenue %'] <= 80
]

print("\nProducts Contributing 80% Revenue")
print(revenue_80_products)

#Margin Risk Products
#Products with Margin < 20%
margin_risk = (
    df.groupby('Product Name')['Gross Margin %']
    .mean()
)

risk_products = margin_risk[
    margin_risk < 20
]

print(risk_products)

#KPI Dashboard Table

kpi = pd.DataFrame({

    'KPI':[
        'Total Sales',
        'Total Profit',
        'Average Margin %',
        'Total Units',
        'Margin Volatility'
    ],

    'Value':[

        df['Sales'].sum(),
        df['Gross Profit'].sum(),
        round(df['Gross Margin %'].mean(),2),
        df['Units'].sum(),
        round(margin_volatility,2)

    ]
})

print(kpi)

# Save KPI Report

kpi.to_csv(
    "KPI_Report.csv",
    index=False
)

# Save Margin Risk Products

risk_products.to_csv(
    "Margin_Risk_Products.csv"
)

# Save Pricing Inefficiency Report

pricing_issue.to_csv(
    "Pricing_Inefficiency_Report.csv"
)

# Save Cost Heavy Margin Poor Products

cost_heavy_margin_poor.to_csv(
    "Cost_Heavy_Margin_Poor_Products.csv"
)

#Export Final Results
product_analysis.to_csv(
    "Product_Profitability_Report.csv",
    index=False
)


division_analysis.to_csv(
    "Division_Performance_Report.csv"
)

pareto_df.to_csv(
    "Pareto_Analysis_Report.csv",
    index=False
)

print("Reports Saved Successfully")
