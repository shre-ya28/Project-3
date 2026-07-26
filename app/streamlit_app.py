"""
Streamlit Web Application
Customer Segmentation & Churn Pattern Analytics in European Banking

Run with:
    streamlit run app/streamlit_app.py
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_processing import load_and_prepare_data
from src.kpi import (
    overall_churn_rate,
    segment_churn_rate,
    high_value_churn_ratio,
    geographic_risk_index,
    engagement_drop_indicator,
    revenue_at_risk,
)

# --------------------------------------------------------------------------
# Page configuration
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="European Bank | Churn Analytics",
    page_icon="🏦",
    layout="wide",
)

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "European_Bank.csv")


@st.cache_data
def get_data(path: str) -> pd.DataFrame:
    return load_and_prepare_data(path)


df = get_data(DATA_PATH)

# --------------------------------------------------------------------------
# Sidebar — segment filters
# --------------------------------------------------------------------------
st.sidebar.title("🏦 Filters")
st.sidebar.caption("Drill down the customer base by segment")

geo_filter = st.sidebar.multiselect(
    "Geography", options=sorted(df["Geography"].unique()), default=sorted(df["Geography"].unique())
)
gender_filter = st.sidebar.multiselect(
    "Gender", options=sorted(df["Gender"].unique()), default=sorted(df["Gender"].unique())
)
age_filter = st.sidebar.multiselect(
    "Age Group", options=list(df["AgeGroup"].cat.categories), default=list(df["AgeGroup"].cat.categories)
)
tenure_filter = st.sidebar.multiselect(
    "Tenure Group", options=list(df["TenureGroup"].cat.categories), default=list(df["TenureGroup"].cat.categories)
)
balance_filter = st.sidebar.multiselect(
    "Balance Segment", options=sorted(df["BalanceSegment"].unique()), default=sorted(df["BalanceSegment"].unique())
)
value_filter = st.sidebar.multiselect(
    "Customer Value", options=sorted(df["IsHighValue"].unique()), default=sorted(df["IsHighValue"].unique())
)
active_filter = st.sidebar.multiselect(
    "Activity Status", options=["Active", "Inactive"], default=["Active", "Inactive"]
)

active_map = {"Active": 1, "Inactive": 0}
active_values = [active_map[a] for a in active_filter]

filtered = df[
    df["Geography"].isin(geo_filter)
    & df["Gender"].isin(gender_filter)
    & df["AgeGroup"].isin(age_filter)
    & df["TenureGroup"].isin(tenure_filter)
    & df["BalanceSegment"].isin(balance_filter)
    & df["IsHighValue"].isin(value_filter)
    & df["IsActiveMember"].isin(active_values)
]

st.sidebar.markdown("---")
st.sidebar.metric("Customers in current filter", f"{len(filtered):,}")

if filtered.empty:
    st.warning("No customers match the selected filters. Please broaden your selection.")
    st.stop()

# --------------------------------------------------------------------------
# Header
# --------------------------------------------------------------------------
st.title("🏦 Customer Segmentation & Churn Pattern Analytics")
st.caption("European Central Bank — Retail Banking Churn Intelligence Dashboard")

tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Overall Summary", "🌍 Geography Explorer", "👥 Age & Tenure", "💎 High-Value Customers"]
)

# --------------------------------------------------------------------------
# TAB 1 — Overall churn summary
# --------------------------------------------------------------------------
with tab1:
    st.subheader("Overall Churn Summary")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Overall Churn Rate", f"{overall_churn_rate(filtered)}%")
    c2.metric("Total Customers", f"{len(filtered):,}")
    c3.metric("Churned Customers", f"{int(filtered['Exited'].sum()):,}")
    risk = revenue_at_risk(filtered)
    c4.metric("Balance at Risk", f"€{risk['TotalBalanceAtRisk']:,.0f}")

    col1, col2 = st.columns(2)
    with col1:
        pie_df = filtered["Exited"].map({0: "Retained", 1: "Churned"}).value_counts().reset_index()
        pie_df.columns = ["Status", "Count"]
        fig = px.pie(pie_df, names="Status", values="Count", hole=0.45,
                     color="Status", color_discrete_map={"Retained": "#4C72B0", "Churned": "#DD8452"},
                     title="Retained vs Churned")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        gender_kpi = segment_churn_rate(filtered, "Gender")
        fig = px.bar(gender_kpi, x="Gender", y="ChurnRate(%)", color="Gender",
                     text="ChurnRate(%)", title="Churn Rate by Gender")
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Credit Score Band vs Churn")
    cs_kpi = segment_churn_rate(filtered, "CreditScoreBand")
    fig = px.bar(cs_kpi, x="CreditScoreBand", y="ChurnRate(%)", text="ChurnRate(%)",
                 title="Churn Rate by Credit Score Band", color="CreditScoreBand")
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Number of Products vs Churn")
    prod_kpi = segment_churn_rate(filtered, "NumOfProducts")
    fig = px.bar(prod_kpi, x="NumOfProducts", y="ChurnRate(%)", text="ChurnRate(%)",
                 title="Churn Rate by Number of Products Held")
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------------------------------
# TAB 2 — Geography-wise churn visualization
# --------------------------------------------------------------------------
with tab2:
    st.subheader("Geography-wise Churn Visualization")

    geo_kpi = geographic_risk_index(filtered)
    st.dataframe(geo_kpi, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(geo_kpi, x="Geography", y="ChurnRate(%)", text="ChurnRate(%)",
                     color="Geography", title="Churn Rate by Country")
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.bar(geo_kpi, x="Geography", y="RiskIndex", text="RiskIndex",
                     color="Geography", title="Geographic Risk Index (Churn Rate x Customer Share)")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Geography × Age Group Interaction")
    pivot = filtered.pivot_table(index="Geography", columns="AgeGroup", values="Exited",
                                  aggfunc="mean", observed=True) * 100
    fig = px.imshow(pivot.round(1), text_auto=True, color_continuous_scale="YlOrRd",
                     labels=dict(color="Churn Rate (%)"), title="Churn Rate (%): Geography x Age Group")
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------------------------------
# TAB 3 — Age & tenure churn comparison
# --------------------------------------------------------------------------
with tab3:
    st.subheader("Age & Tenure Churn Comparison")

    col1, col2 = st.columns(2)
    with col1:
        age_kpi = segment_churn_rate(filtered, "AgeGroup")
        fig = px.bar(age_kpi, x="AgeGroup", y="ChurnRate(%)", text="ChurnRate(%)",
                     color="AgeGroup", title="Churn Rate by Age Group")
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        ten_kpi = segment_churn_rate(filtered, "TenureGroup")
        fig = px.bar(ten_kpi, x="TenureGroup", y="ChurnRate(%)", text="ChurnRate(%)",
                     color="TenureGroup", title="Churn Rate by Tenure Group")
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Engagement Drop Indicator (Activity vs Churn)")
    eng_kpi = engagement_drop_indicator(filtered)
    fig = px.bar(eng_kpi, x="ActivityStatus", y="ChurnRate(%)", text="ChurnRate(%)",
                 color="ActivityStatus", title="Active vs Inactive Members — Churn Rate")
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Balance Segment vs Churn")
    bal_kpi = segment_churn_rate(filtered, "BalanceSegment")
    fig = px.bar(bal_kpi, x="BalanceSegment", y="ChurnRate(%)", text="ChurnRate(%)",
                 color="BalanceSegment", title="Churn Rate by Balance Segment")
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------------------------------
# TAB 4 — High-value customer churn explorer
# --------------------------------------------------------------------------
with tab4:
    st.subheader("High-Value Customer Churn Explorer")
    st.caption("High-value = balance and estimated salary both at or above the dataset median.")

    c1, c2, c3 = st.columns(3)
    c1.metric("High-Value Churn Ratio", f"{high_value_churn_ratio(filtered)}%")
    hv_customers = filtered[filtered["IsHighValue"] == "High-Value"]
    c2.metric("High-Value Customers", f"{len(hv_customers):,}")
    c3.metric("High-Value Churned", f"{int(hv_customers['Exited'].sum()):,}")

    col1, col2 = st.columns(2)
    with col1:
        hv_kpi = segment_churn_rate(filtered, "IsHighValue")
        fig = px.bar(hv_kpi, x="IsHighValue", y="ChurnRate(%)", text="ChurnRate(%)",
                     color="IsHighValue", title="Churn Rate: High-Value vs Standard")
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.scatter(filtered, x="Balance", y="EstimatedSalary",
                          color=filtered["Exited"].map({0: "Retained", 1: "Churned"}),
                          opacity=0.5, title="Balance vs Estimated Salary (colored by churn)",
                          labels={"color": "Status"})
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Revenue Risk from Churn")
    risk = revenue_at_risk(filtered)
    r1, r2 = st.columns(2)
    r1.metric("Total Balance at Risk", f"€{risk['TotalBalanceAtRisk']:,.0f}")
    r2.metric("Avg. Balance per Churned Customer", f"€{risk['AvgBalancePerChurnedCustomer']:,.0f}")

    st.markdown("#### High-Value Churner Detail")
    st.dataframe(
        hv_customers[hv_customers["Exited"] == 1][
            ["CustomerId", "Geography", "Gender", "Age", "Balance", "EstimatedSalary",
             "NumOfProducts", "IsActiveMember", "TenureGroup"]
        ].sort_values("Balance", ascending=False),
        use_container_width=True,
    )

st.markdown("---")
st.caption("Customer Segmentation & Churn Pattern Analytics in European Banking · Unified Mentor Project")
