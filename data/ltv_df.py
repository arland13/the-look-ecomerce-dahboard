import pandas as pd
from data import loader
import streamlit as st

@st.cache_data
def get_ltv_df():
    # load data frames
    orders_df = loader.get_orders_df('databases/orders.csv')
    order_items_df = loader.get_order_items_df('databases/order_items.csv')
    users_df = loader.get_users_df('databases/users.csv')
    
    orders_df["created_at"] = pd.to_datetime(
    orders_df["created_at"],
    format="ISO8601"
)
    
    merged_df = orders_df.merge(
    order_items_df,
    on="order_id",
    how="inner"
)
    
    merged_df = merged_df.merge(
    users_df,
    left_on="user_id_x",
    right_on="id",
    how="inner"
)
    
    filtered_df = merged_df[
    ~merged_df["status_x"].isin(["Cancelled", "Returned"])
]
    
    customer_summary = (
    filtered_df
    .groupby(["user_id_x", "country"], as_index=False)
    .agg(
        total_orders=("order_id", "nunique"),
        total_revenue=("sale_price", "sum"),
        first_order_date=("created_at", "min"),
        last_order_date=("created_at", "max")
    )
)
    
    customer_summary["last_order_date"] = pd.to_datetime(
    customer_summary["last_order_date"],
    format="ISO8601"
)
    
    customer_summary["first_order_date"] = pd.to_datetime(
    customer_summary["first_order_date"],
    format="ISO8601"
)

    customer_summary["active_months"] = (
    (
        customer_summary["last_order_date"].dt.year
        - customer_summary["first_order_date"].dt.year
    ) * 12
    +
    (
        customer_summary["last_order_date"].dt.month
        - customer_summary["first_order_date"].dt.month
    )
    + 1
)
    
  
    customer_summary["first_order_date"] = (
    customer_summary["first_order_date"].dt.date
)

    customer_summary["last_order_date"] = (
    customer_summary["last_order_date"].dt.date
)
    
    customer_summary["ltv"] = (
    customer_summary["total_revenue"]
    .round(2)
)
    
    customer_summary["avg_order_value"] = (
    customer_summary["total_revenue"]
    / customer_summary["total_orders"]
).round(2)
    
    customer_summary["avg_monthly_revenue"] = (
    customer_summary["total_revenue"]
    / customer_summary["active_months"]
).round(2)
    
    customer_summary["ltv_quartile"] = pd.qcut(
    customer_summary["total_revenue"],
    4,
    labels=[1, 2, 3, 4]
)
    
    quartile_labels = {
    1: "Bronze",
    2: "Silver",
    3: "Gold",
    4: "Platinum"
}

    customer_summary["tier"] = (
    customer_summary["ltv_quartile"]
    .astype(int)
    .map(quartile_labels)
)
    
    customer_ltv = customer_summary.sort_values(
    "ltv",
    ascending=False
)
    
    return customer_ltv