from components import metric_cards, revenue_sidebar
from data import revenue_df
from components import revenue_charts
import streamlit as st

# Load CSS   
with open("styles/stylesheet.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("💰 Revenue KPIs")

growth = revenue_df.get_growth_df()

metric, selected_range = revenue_sidebar.render_sidebar(growth)

start_date, end_date = selected_range
growth_filtered = growth[
    (growth["order_month"] >= start_date) &
    (growth["order_month"] <= end_date)
]

selected_row = growth_filtered.iloc[-1]

# Top KPI
selected_period = f"{selected_row['order_month'].strftime('%B %Y')}"
st.caption(f"Selected period: {selected_period}")
c1, c2, c3 = st.columns(3)
with c1:
    metric_cards.metric_card(
        "GMV", 
        f"${selected_row['gmv']:,.0f}",
        selected_row["mom_growth_pct"],
        "%")
with c2:
    metric_cards.metric_card(
        "AOV", 
        f"${selected_row['aov']:,.2f}", 
        selected_row["aov_mom_change"])
with c3:
    metric_cards.metric_card(
        "YTD Revenue", 
        f"${selected_row['ytd_revenue']:,.0f}")

# AOV, GMV, and Orders trend

metric_title_map = {
    "GMV": "Gross Merchandise Value",
    "AOV": "Average Order Value",
    "Orders": "Number of Orders"
}

selected_metric_title = metric_title_map[metric]

# Dynamic Chart
st.markdown(
    f'<div class="section-header">{selected_metric_title} over time</div>',
    unsafe_allow_html=True
)

fig = revenue_charts.create_metric_chart(growth_filtered, metric)

st.plotly_chart(fig, use_container_width=True)  

# Growth chart 
st.markdown( 
    '<div class="section-header">' \
        'Revenue growth rate'
    '</div>', 
    unsafe_allow_html=True 
) 
fig2 = revenue_charts.create_growth_chart( growth_filtered ) 
st.plotly_chart(fig2, use_container_width=True)

# Dynamic table
st.markdown(
    '<div class="section-header">Monthly data table</div>',
    unsafe_allow_html=True
)

display_df = growth_filtered[
    [
        "order_month",
        "gmv",
        "aov",
        "num_orders",
        "mom_growth_pct",
        "yoy_growth_pct",
        "ytd_revenue"
    ]
].copy()

display_df["order_month"] = (
    display_df["order_month"]
    .dt.strftime("%Y-%m")
)

display_df.columns = [
    "Month",
    "GMV",
    "AOV",
    "Orders",
    "MoM %",
    "YoY %",
    "YTD Revenue"
]

st.dataframe(
    display_df.sort_values("Month", ascending=False)
    .reset_index(drop=True),
    use_container_width=True,
    hide_index=True
)