import streamlit as st


def render_ltv_sidebar(df):
    st.sidebar.title("👤 Customer Analytics")

    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 Filters")

    # Country filter
    countries = sorted(df["country"].dropna().unique())

    selected_countries = st.sidebar.multiselect(
        "Country",
        options=countries,
        default=countries
    )

    # Tier filter
    tiers = sorted(df["tier"].dropna().unique())

    selected_tiers = st.sidebar.multiselect(
        "Customer Tier",
        options=tiers,
        default=tiers
    )

    # LTV range
    min_ltv = float(df["ltv"].min())
    max_ltv = float(df["ltv"].max())

    selected_ltv = st.sidebar.slider(
        "LTV Range",
        min_value=min_ltv,
        max_value=max_ltv,
        value=(min_ltv, max_ltv)
    )

    # Minimum orders
    min_orders = st.sidebar.number_input(
        "Minimum Orders",
        min_value=1,
        value=1,
        step=1
    )

    # Minimum active months
    min_active_months = st.sidebar.number_input(
        "Minimum Active Months",
        min_value=1,
        value=1,
        step=1
    )

    st.sidebar.markdown("---")

    # KPI info
    with st.sidebar.expander("ℹ️ KPI Definitions"):
        st.markdown("""
        - **LTV** = Total customer revenue
        - **AOV** = Average order value
        - **Top 10% LTV** = Highest-value customers
        - **Active Months** = Customer lifespan
        """)

    # Apply filters
    filtered_df = df[
        (df["country"].isin(selected_countries)) &
        (df["tier"].isin(selected_tiers)) &
        (df["ltv"] >= selected_ltv[0]) &
        (df["ltv"] <= selected_ltv[1]) &
        (df["total_orders"] >= min_orders) &
        (df["active_months"] >= min_active_months)
    ]

    st.sidebar.markdown("---")

    return filtered_df