"""
data_processing.py
-------------------
Loads the raw European bank customer dataset, validates it, cleans it,
and creates all derived segmentation fields used throughout the
Customer Segmentation & Churn Pattern Analytics project.

Usage:
    from src.data_processing import load_and_prepare_data
    df = load_and_prepare_data("data/European_Bank.csv")
"""

import pandas as pd
import numpy as np


def load_raw_data(path: str) -> pd.DataFrame:
    """Load the raw CSV file."""
    df = pd.read_csv(path)
    return df


def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic validation checks:
    - No nulls in key fields
    - Binary fields (HasCrCard, IsActiveMember, Exited) only contain 0/1
    - Geography and Gender contain expected categories
    """
    binary_cols = ["HasCrCard", "IsActiveMember", "Exited"]
    for col in binary_cols:
        bad = ~df[col].isin([0, 1])
        if bad.any():
            raise ValueError(f"Column {col} contains values other than 0/1")

    expected_geo = {"France", "Spain", "Germany"}
    unexpected_geo = set(df["Geography"].unique()) - expected_geo
    if unexpected_geo:
        raise ValueError(f"Unexpected Geography values found: {unexpected_geo}")

    expected_gender = {"Male", "Female"}
    unexpected_gender = set(df["Gender"].unique()) - expected_gender
    if unexpected_gender:
        raise ValueError(f"Unexpected Gender values found: {unexpected_gender}")

    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove non-analytical fields and duplicate records."""
    df = df.copy()

    # Drop non-analytical identifier field
    if "Surname" in df.columns:
        df = df.drop(columns=["Surname"])

    # Drop exact duplicate customer records, if any
    if "CustomerId" in df.columns:
        df = df.drop_duplicates(subset="CustomerId")

    return df


def add_segments(df: pd.DataFrame) -> pd.DataFrame:
    """Create all derived segmentation fields used in the analysis."""
    df = df.copy()

    # --- Age segmentation ---
    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=[0, 30, 45, 60, np.inf],
        labels=["<30", "30-45", "46-60", "60+"],
        right=True,
    )

    # --- Credit score bands ---
    df["CreditScoreBand"] = pd.cut(
        df["CreditScore"],
        bins=[0, 580, 700, np.inf],
        labels=["Low (<=580)", "Medium (581-700)", "High (701+)"],
    )

    # --- Tenure groups ---
    df["TenureGroup"] = pd.cut(
        df["Tenure"],
        bins=[-1, 2, 6, np.inf],
        labels=["New (0-2 yrs)", "Mid-term (3-6 yrs)", "Long-term (7+ yrs)"],
    )

    # --- Balance segments ---
    def balance_segment(bal):
        if bal == 0:
            return "Zero-balance"
        elif bal < 100000:
            return "Low-balance"
        else:
            return "High-balance"

    df["BalanceSegment"] = df["Balance"].apply(balance_segment)

    # --- High-value customer flag ---
    # High value = above-median balance AND above-median estimated salary
    balance_median = df["Balance"].median()
    salary_median = df["EstimatedSalary"].median()
    df["IsHighValue"] = np.where(
        (df["Balance"] >= balance_median) & (df["EstimatedSalary"] >= salary_median),
        "High-Value",
        "Standard",
    )

    # --- Engagement flag (combines activity + product count) ---
    df["EngagementLevel"] = np.where(
        (df["IsActiveMember"] == 1) & (df["NumOfProducts"] >= 2),
        "High Engagement",
        np.where(
            (df["IsActiveMember"] == 0) & (df["NumOfProducts"] == 1),
            "Low Engagement",
            "Medium Engagement",
        ),
    )

    return df


def load_and_prepare_data(path: str) -> pd.DataFrame:
    """Full pipeline: load -> validate -> clean -> segment."""
    df = load_raw_data(path)
    df = validate_data(df)
    df = clean_data(df)
    df = add_segments(df)
    return df


if __name__ == "__main__":
    data = load_and_prepare_data("data/European_Bank.csv")
    print(f"Prepared dataset shape: {data.shape}")
    print(data.head())
