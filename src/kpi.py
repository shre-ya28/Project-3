"""
kpi.py
------
Reusable KPI calculation functions shared by the analysis notebook and
the Streamlit dashboard.
"""

import pandas as pd


def overall_churn_rate(df: pd.DataFrame) -> float:
    """% of customers who exited."""
    return round(df["Exited"].mean() * 100, 2)


def segment_churn_rate(df: pd.DataFrame, segment_col: str) -> pd.DataFrame:
    """Churn % by segment, plus segment size and share of total churners."""
    total_churners = df["Exited"].sum()

    grouped = df.groupby(segment_col, observed=True).agg(
        Customers=("Exited", "count"),
        Churned=("Exited", "sum"),
    )
    grouped["ChurnRate(%)"] = round(grouped["Churned"] / grouped["Customers"] * 100, 2)
    grouped["ShareOfTotalChurn(%)"] = round(grouped["Churned"] / total_churners * 100, 2)
    grouped = grouped.sort_values("ChurnRate(%)", ascending=False)
    return grouped.reset_index()


def high_value_churn_ratio(df: pd.DataFrame) -> float:
    """Churn rate among high-value customers only."""
    hv = df[df["IsHighValue"] == "High-Value"]
    if len(hv) == 0:
        return 0.0
    return round(hv["Exited"].mean() * 100, 2)


def geographic_risk_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    Regional churn exposure = churn rate weighted by each region's
    share of total customer base (a simple risk-exposure score).
    """
    geo = segment_churn_rate(df, "Geography")
    geo["CustomerShare(%)"] = round(geo["Customers"] / len(df) * 100, 2)
    geo["RiskIndex"] = round(geo["ChurnRate(%)"] * geo["CustomerShare(%)"] / 100, 2)
    return geo.sort_values("RiskIndex", ascending=False)


def engagement_drop_indicator(df: pd.DataFrame) -> pd.DataFrame:
    """Churn rate by activity status (inactive vs active members)."""
    grouped = df.groupby("IsActiveMember").agg(
        Customers=("Exited", "count"),
        Churned=("Exited", "sum"),
    )
    grouped["ChurnRate(%)"] = round(grouped["Churned"] / grouped["Customers"] * 100, 2)
    grouped.index = grouped.index.map({0: "Inactive", 1: "Active"})
    return grouped.reset_index().rename(columns={"IsActiveMember": "ActivityStatus"})


def revenue_at_risk(df: pd.DataFrame) -> dict:
    """Total balance held by churned customers -- a proxy for revenue/deposit risk."""
    churned = df[df["Exited"] == 1]
    return {
        "TotalBalanceAtRisk": round(churned["Balance"].sum(), 2),
        "AvgBalancePerChurnedCustomer": round(churned["Balance"].mean(), 2),
        "TotalChurnedCustomers": int(len(churned)),
        "TotalSalaryExposure": round(churned["EstimatedSalary"].sum(), 2),
    }
