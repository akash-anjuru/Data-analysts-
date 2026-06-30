import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Configuration
st.set_page_config(
    page_title="Nassau Candy Profitability Dashboard",
    layout="wide"
)

# Title
st.title("📊 Nassau Candy Distributor Dashboard")

# Load Dataset
df = pd.read_csv("Nassau Candy Distributor.csv")

# Data Cleaning
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

df = df[df['Sales'] > 0]
df = df[df['Gross Profit'] >= 0]

# Date Conversion
df['Order Date'] = pd.to_datetime(
    df['Order Date'],
    dayfirst=True,
    errors='coerce'
)

df['Ship Date'] = pd.to_datetime(
    df['Ship Date'],
    dayfirst=True,
    errors='coerce'
)

# Calculated Columns
df['Gross Margin %'] = (
    df['Gross Profit'] / df['Sales']
) * 100

df['Profit Per Unit'] = (
    df['Gross Profit'] / df['Units']
)

# Sidebar Filters
st.sidebar.header("Filters")

division_filter = st.sidebar.multiselect(
    "Select Division",
    df['Division'].unique(),
    default=df['Division'].unique()
)

margin_filter = st.sidebar.slider(
    "Minimum Margin %",
    0,
    100,
    0
)

product_search = st.sidebar.text_input(
    "Search Product"
)

start_date = st.sidebar.date_input(
    "Start Date",
    df['Order Date'].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    df['Order Date'].max()
)

# Apply Filters
filtered_df = df[
    (df['Division'].isin(division_filter))
    &
    (df['Gross Margin %'] >= margin_filter)
    &
    (df['Order Date'] >= pd.to_datetime(start_date))
    &
    (df['Order Date'] <= pd.to_datetime(end_date))
]

if product_search:
    filtered_df = filtered_df[
        filtered_df['Product Name']
        .str.contains(
            product_search,
            case=False,
            na=False
        )
    ]

# KPI Section
st.subheader("📌 Key Performance Indicators")

margin_volatility = (
    filtered_df['Gross Margin %'].std()
)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Sales",
    f"${filtered_df['Sales'].sum():,.0f}"
)

col2.metric(
    "Total Profit",
    f"${filtered_df['Gross Profit'].sum():,.0f}"
)

col3.metric(
    "Average Margin %",
    round(filtered_df['Gross Margin %'].mean(), 2)
)

col4.metric(
    "Units Sold",
    int(filtered_df['Units'].sum())
)

col5.metric(
    "Margin Volatility",
    round(margin_volatility, 2)
)

# Top Products by Gross Profit
st.subheader("🏆 Top 10 Products by Gross Profit")

top_profit = (
    filtered_df.groupby('Product Name')
    ['Gross Profit']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(10,5))

top_profit.plot(
    kind='bar',
    ax=ax
)

ax.set_ylabel("Gross Profit")

st.pyplot(fig)

# Top Products by Gross Margin
st.subheader("📈 Top 10 Products by Gross Margin")

top_margin = (
    filtered_df.groupby('Product Name')
    ['Gross Margin %']
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(10,5))

top_margin.plot(
    kind='bar',
    ax=ax
)

ax.set_ylabel("Gross Margin %")

st.pyplot(fig)

# Top Products by Profit Per Unit
st.subheader("💵 Top Products by Profit Per Unit")

profit_unit = (
    filtered_df.groupby('Product Name')
    ['Profit Per Unit']
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(10,5))

profit_unit.plot(
    kind='bar',
    ax=ax
)

st.pyplot(fig)

# Sales vs Profit Analysis
st.subheader("📊 Sales vs Gross Profit")

product_analysis = (
    filtered_df.groupby('Product Name')
    .agg({
        'Sales':'sum',
        'Gross Profit':'sum'
    })
    .reset_index()
)

fig, ax = plt.subplots(figsize=(8,5))

sns.scatterplot(
    data=product_analysis,
    x='Sales',
    y='Gross Profit',
    ax=ax
)

st.pyplot(fig)

# Division Performance
st.subheader("🏢 Division Performance")

division_analysis = (
    filtered_df.groupby('Division')
    .agg({
        'Sales':'sum',
        'Gross Profit':'sum'
    })
)

fig, ax = plt.subplots(figsize=(8,5))

division_analysis['Gross Profit'].plot(
    kind='bar',
    ax=ax
)

st.pyplot(fig)

# Revenue vs Profit by Division
st.subheader("📉 Revenue vs Profit by Division")

st.dataframe(
    division_analysis
)

# Cost vs Sales
if 'Cost' in filtered_df.columns:

    st.subheader("💰 Cost vs Sales Analysis")

    fig, ax = plt.subplots(figsize=(8,5))

    sns.scatterplot(
        data=filtered_df,
        x='Cost',
        y='Sales',
        ax=ax
    )

    st.pyplot(fig)

# Pricing Inefficiency
st.subheader("⚠ Pricing Inefficiency Products")

pricing_issue = (
    filtered_df.groupby('Product Name')
    .agg({
        'Sales':'sum',
        'Gross Margin %':'mean'
    })
)

pricing_issue = pricing_issue[
    (pricing_issue['Sales'] >
     pricing_issue['Sales'].mean())
    &
    (pricing_issue['Gross Margin %'] < 20)
]

if pricing_issue.empty:
    st.info(
        "No pricing inefficiency products found based on current criteria."
    )
else:
    st.dataframe(
        pricing_issue.reset_index()
    )
# Margin Risk Products
st.subheader("🚨 Margin Risk Products")

margin_risk = (
    filtered_df.groupby('Product Name')
    ['Gross Margin %']
    .mean()
)

risk_products = margin_risk[
    margin_risk < 20
]

st.dataframe(
    risk_products.reset_index()
)

# Pareto Analysis
st.subheader("📊 Pareto Analysis (80/20 Rule)")

pareto = (
    filtered_df.groupby('Product Name')
    ['Gross Profit']
    .sum()
    .sort_values(ascending=False)
)

pareto_df = pareto.reset_index()

pareto_df['Cumulative Profit %'] = (
    pareto_df['Gross Profit'].cumsum()
    /
    pareto_df['Gross Profit'].sum()
) * 100

st.dataframe(
    pareto_df.head(20)
)

# Raw Data
st.subheader("📋 Dataset Preview")

st.dataframe(
    filtered_df.head(50)
)

st.success(
    "Dashboard Loaded Successfully"
)
st.markdown("---")
st.markdown(
    "Developed by Akash | Data Analysis Internship Project | Nassau Candy Distributor Profitability Analysis"
)