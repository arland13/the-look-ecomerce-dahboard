import streamlit as st
from data import retention_df
import pandas as pd


def show_retention_sidebar():

    # =========================
    # LOAD DATA
    # =========================
    df_ret = retention_df.get_retention_df()

    m1 = df_ret[df_ret["months_since_first"] == 1].copy()

    avg_m1 = m1["retention_rate_pct"].mean()

    best_row = m1.loc[m1["retention_rate_pct"].idxmax()]

    latest_row = m1.sort_values("cohort_month").iloc[-1]

    # =========================
    # SIDEBAR TITLE
    # =========================
    st.sidebar.title("🔄 Retention Dashboard")

    # =========================
    # KPI METRICS
    # =========================
    st.sidebar.metric(
        "Avg M1 Retention",
        f"{avg_m1:.1f}%"
    )

    st.sidebar.metric(
        "Best Cohort",
        f"{best_row['retention_rate_pct']:.1f}%"
    )

    st.sidebar.metric(
        "Latest Cohort",
        f"{latest_row['retention_rate_pct']:.1f}%"
    )

    # =========================
    # COHORT FILTER
    # =========================
    cohort_options = sorted(df_ret["cohort_month"].unique())

    selected_cohort = st.sidebar.selectbox(
        "Select Cohort",
        cohort_options
    )

    # =========================
    # KPI EXPLANATION
    # =========================
    with st.sidebar.expander("📘 Cohort Retention Guide"):

        st.markdown("""
        ### What is a Cohort?

        A cohort is a group of users based on their first purchase month.

        ### Retention

        Retention measures how many users return in later months.

        ### Month Definitions

        - Month 0 → first purchase month
        - Month 1 → returned next month
        - Month 2 → returned after 2 months

        ### Why It Matters

        Higher retention usually means:
        - better customer loyalty
        - stronger product engagement
        - healthier business growth
        """)

    # =========================
    # INDUSTRY BENCHMARK
    # =========================
    with st.sidebar.expander("🏆 Ecommerce Benchmark"):

        st.markdown("""
        ### M1 Retention Benchmark

        - Poor: below 20%
        - Average: 20% - 35%
        - Strong: above 35%
        """)

    # =========================
    # HEATMAP LEGEND
    # =========================
    with st.sidebar.expander("🎨 Heatmap Colors"):

        st.markdown("""
        - Dark green = high retention
        - Orange = low retention
        """)

    # =========================
    # BUSINESS INSIGHT
    # =========================
    st.sidebar.info(
        """
        💡 Insight

        Retention usually drops sharply after Month 1.

        This often indicates onboarding or engagement problems.
        """
    )

    return selected_cohort
