import streamlit as st

def sidebar_info():

    with st.sidebar:

        st.markdown("## KPI Definitions")

        with st.expander("What do these mean?"):

            st.markdown("""
            **Active**  
            Customers ordering regularly.

            **At Risk**  
            Customers nearing churn threshold.

            **Churned**  
            Customers inactive beyond threshold.
            """)
