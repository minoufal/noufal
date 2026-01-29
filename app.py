import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- Page Config ----------------
st.set_page_config(page_title="Sales Analytics Dashboard", layout="wide")

# ---------------- Title ----------------
st.title("📊 Sales Analytics Dashboard")

# ---------------- Load Data ----------------
df = pd.read_csv("sales_data (5).csv")

# Remove unwanted columns
df = df.loc[:, ~df.columns.str.contains("Unnamed")]

# Convert date column
df["Sale_Date"] = pd.to_datetime(df["Sale_Date"], dayfirst=True, errors="coerce")

# ---------------- Sidebar Filters ----------------
st.sidebar.header("🔎 Filters")

region = st.sidebar.selectbox(
    "Select Region",
    options=["All"] + sorted(df["Region"].dropna().unique().tolist())
)

category = st.sidebar.selectbox(
    "Select Product Category",
    options=["All"] + sorted(df["Product_Category"].dropna().unique().tolist())
)

Sales_Rep = st.sidebar.selectbox(
    "Select sales_Rep",
    options=["All"] + sorted(df["Sales_Rep"].dropna().unique().tolist())
)

# ---------------- Apply Filters ----------------
filtered_df = df.copy()

if region != "All":
    filtered_df = filtered_df[filtered_df["Region"] == region]

if category != "All":
    filtered_df = filtered_df[filtered_df["Product_Category"] == category]

if Sales_Rep != "All":
    filtered_df = filtered_df[filtered_df["Sales_Rep"] == Sales_Rep]

# ---------------- KPIs ----------------
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales Amount",
    f"₹ {filtered_df['Sales_Amount'].sum():,.0f}"
)

col2.metric(
    "Total Quantity Sold",
    int(filtered_df["Quantity_Sold"].sum())
)

col3.metric(
    "Average Discount",
    f"{filtered_df['Discount'].mean():.2%}"
)

col4.metric(
    "Total Transactions",
    filtered_df.shape[0]
)

st.markdown("---")

# ---------------- Charts Row 1 ----------------
col5, col6 = st.columns(2)

with col5:
    fig_cat = px.bar(
        filtered_df,
        x="Product_Category",
        y="Sales_Amount",
        color="Product_Category",
        title="Sales by Product Category"
    )
    st.plotly_chart(fig_cat, use_container_width=True)

with col6:
    fig_region = px.pie(
        filtered_df,
        names="Region",
        values="Sales_Amount",
        title="Sales Distribution by Region"
    )
    st.plotly_chart(fig_region, use_container_width=True)

# ---------------- Sales Rep Performance (NEW CHART) ----------------
rep_sales = (
    filtered_df
    .groupby("Sales_Rep", as_index=False)["Sales_Amount"]
    .sum()
    .sort_values(by="Sales_Amount", ascending=False)
)

fig_rep = px.bar(
    rep_sales,
    x="Sales_Rep",
    y="Sales_Amount",
    title="Sales Rep wise Sales Amount",
    text_auto=True
)
st.plotly_chart(fig_rep, use_container_width=True)

# ---------------- Time Series ----------------
fig_time = px.line(
    filtered_df.sort_values("Sale_Date"),
    x="Sale_Date",
    y="Sales_Amount",
    title="Sales Trend Over Time"
)
st.plotly_chart(fig_time, use_container_width=True)



# ---------------- Table ----------------
st.markdown("### 📄 Filtered Sales Data")
st.dataframe(filtered_df)
