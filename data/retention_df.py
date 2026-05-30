import pandas as pd
from data import loader
import streamlit as st

@st.cache_data
def get_retention_df():
    # load data frames
    orders_df = loader.get_orders_df('databases/orders.csv')

    orders_df["created_at"] = pd.to_datetime(
    orders_df["created_at"],
    format="ISO8601"
)
    
    cohort = (
    orders_df.groupby("user_id")["created_at"]
    .min()
    .dt.to_period("M")
    .dt.to_timestamp()
    .reset_index(name="cohort_month")
)
    
    activity = (
    orders_df.assign(
        activity_month=orders_df["created_at"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )
    [["user_id", "activity_month"]]
    .drop_duplicates()
)
    
    cohort_size = (
    cohort.groupby("cohort_month")["user_id"]
    .count()
    .reset_index(name="cohort_users")
)
    
    retention = (
    cohort.merge(activity, on="user_id")
    .merge(cohort_size, on="cohort_month")
)

    # months difference
    retention["months_since_first"] = (
    (retention["activity_month"].dt.year - retention["cohort_month"].dt.year) * 12
    + (retention["activity_month"].dt.month - retention["cohort_month"].dt.month)
)

    # filter conditions
    retention = retention[
    (retention["months_since_first"].between(0, 11)) &
    (
        retention["cohort_month"] >=
        (pd.Timestamp.today().normalize() - pd.DateOffset(months=18))
    )
]

    # final aggregation
    retention = (
    retention.groupby(
        ["cohort_month", "cohort_users", "months_since_first"]
    )["user_id"]
    .nunique()
    .reset_index(name="retained_users")
)

    # retention %
    retention["retention_rate_pct"] = round(
    retention["retained_users"] * 100 / retention["cohort_users"],
    1
)

    # order by
    retention = retention.sort_values(
    ["cohort_month", "months_since_first"]
)
    return retention