from data import ltv_df
from components import metric_cards, ltv_charts, ltv_sidebar
import streamlit as st

# Load CSS   
with open("styles/stylesheet.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("👤 Customer Lifetime Value")

df_ltv = ltv_df.get_ltv_df()
df_ltv = ltv_sidebar.render_ltv_sidebar(df_ltv)

avg_ltv   = df_ltv["ltv"].mean()
med_ltv   = df_ltv["ltv"].median()
top_ltv   = df_ltv["ltv"].quantile(0.9)
total_cust = len(df_ltv)


c1, c2, c3, c4 = st.columns(4)
with c1: metric_cards.metric_card("Average LTV", f"${avg_ltv:,.2f}")
with c2: metric_cards.metric_card("Median LTV",  f"${med_ltv:,.2f}")
with c3: metric_cards.metric_card("Top 10% LTV", f"${top_ltv:,.2f}")
with c4: metric_cards.metric_card("Total customers", f"{total_cust:,}")

c1, c2 = st.columns(2)

with c1:
    st.markdown(
        '<div class="section-header">' \
            'LTV distribution (histogram)'
        '</div>', unsafe_allow_html=True
        )
    fig = ltv_charts.ltv_distribution_chart(df_ltv)

    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown(
        '<div class="section-header">' \
            'Avg LTV by tier'
        '</div>', unsafe_allow_html=True
        )
    fig = ltv_charts.ltv_tier_chart(df_ltv)

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<div class="section-header">' \
            'Top 50 customers by LTV'
        '</div>', unsafe_allow_html=True)
    
    top50 = (
    df_ltv[[
        "user_id_x",
        "country",
        "ltv",
        "total_orders",
        "avg_order_value",
        "active_months",
        "tier"]].head(50)
    )

    top50.columns = [
        "User ID",
        "Country",
        "LTV",
        "Orders",
        "Avg Order",
        "Active Months",
        "Tier"
        ]

    st.dataframe(
        top50.reset_index(drop=True), 
        use_container_width=True, 
        hide_index=True
        )