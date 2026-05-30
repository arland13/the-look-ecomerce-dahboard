import streamlit as st

def render_sidebar(growth):

    # ================= #
    # Date Boundaries   #
    # ================= #
    min_date = growth["order_month"].min().to_pydatetime()
    max_date = growth["order_month"].max().to_pydatetime()

    # ================= #
    # Sidebar UI        #
    # ================= #
    st.sidebar.title("📊 Revenue Analytics")

    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 Filters")
    with st.sidebar:

        metric = st.selectbox(
            "Metric",
            ["GMV", "AOV", "Orders"]
        )

        selected_range = st.slider(
            "Select Period",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            format="MMM YYYY"
        )

        st.divider()

        with st.expander("📘 KPI Definitions"):

            st.markdown("""
            **GMV (Gross Merchandise Value)**  
            Total revenue generated from all orders before deductions.

            **AOV (Average Order Value)**  
            Average amount spent per order.

            Formula:
            AOV = Revenue ÷ Number of Orders

            **YTD (Year-to-Date Revenue)**  
            Total accumulated revenue from the beginning of the year until the selected month.
            """)

    return metric, selected_range
