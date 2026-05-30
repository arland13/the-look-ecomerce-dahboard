import pandas as pd
import numpy as np
from data import loader
import streamlit as st

@st.cache_data
def get_churn_df():
    # load data frames
    orders_df = loader.get_orders_df('databases/orders.csv')
    order_items_df = loader.get_order_items_df('databases/order_items.csv')

    valid_orders = orders_df[
    ~orders_df["status"].isin(["Cancelled", "Returned"])
].copy()
    
    order_revenue = (
    order_items_df
    .groupby("order_id", as_index=False)["sale_price"]
    .sum()
    .rename(columns={"sale_price": "order_revenue"})
)
    
    merged = valid_orders.merge(order_revenue, on="order_id", how="left")

    merged["created_at"] = pd.to_datetime(
    merged["created_at"],
    format="ISO8601"
).dt.tz_localize(None)

    customer_metrics = (
    merged.groupby("user_id")
    .agg(
        last_order_date=("created_at", "max"),
        total_orders=("order_id", "nunique"),
        total_revenue=("order_revenue", "sum")
    )
    .reset_index()
)

    last_purchases = customer_metrics["days_since_last_order"] = (
    pd.Timestamp.today().normalize()
    - customer_metrics["last_order_date"]
).dt.days
    
    customer_metrics["days_since_last_order"] = (
    pd.Timestamp.today().normalize()
    - pd.to_datetime(customer_metrics["last_order_date"])
).dt.days
    
    customer_metrics["total_revenue"] = (
    customer_metrics["total_revenue"].round(2)
)

    customer_metrics["churn_status"] = np.select(
    [
        customer_metrics["days_since_last_order"] <= 90,
        customer_metrics["days_since_last_order"] <= 180
    ],
    [
        "Active",
        "At Risk"
    ],
    default="Churned"
)

    result = (
    customer_metrics[
        [
            "user_id",
            "last_order_date",
            "days_since_last_order",
            "total_orders",
            "total_revenue",
            "churn_status"
        ]
    ]
    .sort_values("days_since_last_order")
)
    
    return result