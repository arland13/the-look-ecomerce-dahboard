from components import metric_cards, overview_charts
from data import revenue_df
import streamlit as st
import pandas as pd
import streamlit as st

# Streamlit Config  
st.set_page_config(
    page_title="E-Commerce KPI Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS   
with open("styles/stylesheet.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load Data
growth = revenue_df.get_growth_df()
latest = growth.iloc[-1]
prev = growth.iloc[-2] if len(growth) > 1 else latest

st.title("📊 E-Commerce KPI Dashboard")
st.markdown(f"Data source: `bigquery-public-data.thelook_ecommerce` · Latest month: **{latest['order_month'].strftime('%B %Y')}**")

# Top KPI row
c1, c2, c3, c4 = st.columns(4)
with c1:
    metric_cards.metric_card("Gross Merchandise Value", f"${latest['gmv']:,.0f}", latest["mom_growth_pct"], "%")
with c2:
    metric_cards.metric_card("Average Order Value", f"${latest['aov']:,.2f}", latest["aov_mom_change"], "")
with c3:
    metric_cards.metric_card("MoM Revenue Growth", f"{latest['mom_growth_pct']:+.1f}%")
with c4:
    metric_cards.metric_card("YoY Revenue Growth", f"{latest['yoy_growth_pct']:+.1f}%" if pd.notna(latest['yoy_growth_pct']) else "N/A")

# GMV trend
st.markdown('<div class="section-header">GMV trend</div>', unsafe_allow_html=True)
fig = overview_charts.gmv_trend()
st.plotly_chart(fig, use_container_width=True)

# LTV + Churn split
c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="section-header">LTV distribution</div>', unsafe_allow_html=True)

    fig2 = overview_charts.ltv_distribution()

    st.plotly_chart(
        fig2,
        use_container_width=True,
        key="ltv_distribution_chart"
    )

with c2:
    st.markdown('<div class="section-header">Customer churn status</div>', unsafe_allow_html=True)

    fig3 = overview_charts.cust_churn_stat()

    st.plotly_chart(
        fig3,
        use_container_width=True,
        key="customer_churn_chart"
    )