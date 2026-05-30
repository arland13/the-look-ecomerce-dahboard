from data import loader
import pandas as pd
import streamlit as st

@st.cache_data
def get_growth_df():
    
    # load data frames
    orders_df = loader.get_orders_df('databases/orders.csv')
    order_items_df = loader.get_order_items_df('databases/order_items.csv')

    orders_df["created_at"] = pd.to_datetime(
    orders_df["created_at"],
    format="ISO8601")

    merged_df = orders_df.merge(
    order_items_df,
    on="order_id",
    how="inner")

    filtered_df = merged_df[
    ~merged_df["status_x"].isin(["Cancelled", "Returned"])]

    filtered_df["order_month"] = (
    filtered_df["created_at_x"]
    .dt.to_period("M")
    .dt.to_timestamp())

    filtered_df["order_month"] = (
    filtered_df["created_at_x"]
    .dt.to_period("M")
    .dt.to_timestamp())

    monthly_orders_df = (
    filtered_df
    .groupby(["order_month", "order_id"], as_index=False)
    ["sale_price"]
    .sum())

    monthly_orders_df = monthly_orders_df.rename(columns={
    "sale_price": "order_revenue"})
    
    monthly_summary_df = (
    monthly_orders_df
    .groupby("order_month", as_index=False)
    .agg(
        num_orders=("order_id", "count"),
        gmv=("order_revenue", "sum"),
        aov=("order_revenue", "mean")))
    
    monthly_summary_df["gmv"] = monthly_summary_df["gmv"].round(2)
    monthly_summary_df["aov"] = monthly_summary_df["aov"].round(2)
    monthly_summary_df = monthly_summary_df.sort_values("order_month")
    monthly_summary_df["prev_month_gmv"] = (monthly_summary_df["gmv"].shift(1))
    monthly_summary_df["same_month_last_year"] = (monthly_summary_df["gmv"].shift(12))
    monthly_summary_df["prev_month_aov"] = (monthly_summary_df["aov"].shift(1))

    monthly_summary_df["mom_growth_pct"] = (
    (monthly_summary_df["gmv"] - monthly_summary_df["prev_month_gmv"])
    * 100/ monthly_summary_df["prev_month_gmv"]).round(1)

    monthly_summary_df["yoy_growth_pct"] = (
    (monthly_summary_df["gmv"] - monthly_summary_df["same_month_last_year"])
    * 100
    / monthly_summary_df["same_month_last_year"]).round(1)

    monthly_summary_df["aov_mom_change"] = (
    monthly_summary_df["aov"] - monthly_summary_df["prev_month_aov"]).round(2)

    monthly_summary_df["year"] = monthly_summary_df["order_month"].dt.year

    monthly_summary_df["ytd_revenue"] = (
    monthly_summary_df
    .groupby("year")["gmv"]
    .cumsum()
    .round(2))

    return monthly_summary_df

