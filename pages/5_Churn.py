import streamlit as st
from data import churn_df
from components import metric_cards, churn_charts, churn_sidebar

# Sidebar
churn_sidebar.sidebar_info()

# Load CSS   
with open("styles/stylesheet.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("⚠️ Churn Classification")

df_churn = churn_df.get_churn_df()
churn_counts = df_churn["churn_status"].value_counts()
total = len(df_churn)

c1, c2, c3 = st.columns(3)
with c1:
    n = churn_counts.get("Active", 0)
    metric_cards.metric_card("Active customers", f"{n:,}", n / total * 100, "% of base")
with c2:
    n = churn_counts.get("At Risk", 0)
    metric_cards.metric_card("At-risk customers", f"{n:,}", -(n / total * 100), "% of base")
with c3:
    n = churn_counts.get("Churned", 0)
    metric_cards.metric_card("Churned customers", f"{n:,}", -(n / total * 100), "% of base")

c1, c2 = st.columns(2)
with c1:
    st.markdown('<div class="section-header">Churn breakdown</div>', unsafe_allow_html=True)
    fig = churn_charts.churn_breakdown()
    st.plotly_chart(fig, use_container_width=True)
with c2:
    st.markdown('<div class="section-header">Revenue at risk by segment</div>', unsafe_allow_html=True)
    fig2 = churn_charts.revenue_at_risk()
    st.plotly_chart(fig2, use_container_width=True)

# Days since last order distribution
st.markdown('<div class="section-header">Days since last order</div>', unsafe_allow_html=True)
fig3 = churn_charts.days_since_last_order()
st.plotly_chart(fig3, use_container_width=True)

# High-value churned customers
st.markdown('<div class="section-header">High-value churned customers (re-engagement targets)</div>', unsafe_allow_html=True)
high_value_churned = df_churn[df_churn["churn_status"] == "Churned"] \
    .nlargest(20, "total_revenue")[["user_id","last_order_date","days_since_last_order","total_orders","total_revenue"]]
high_value_churned.columns = ["User ID","Last Order","Days Inactive","Orders","Total Revenue"]
st.dataframe(high_value_churned.reset_index(drop=True), use_container_width=True, hide_index=True)
