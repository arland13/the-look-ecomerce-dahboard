from components import retention_charts, retention_sidebar
import streamlit as st

# Load CSS   
with open("styles/stylesheet.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar 
selected_cohort = retention_sidebar.show_retention_sidebar()

# Main Page
st.title("🔄 Monthly Retention (Cohort)")

# Pivot to heatmap
st.markdown('<div class="section-header">Cohort retention heatmap</div>', unsafe_allow_html=True)
fig = retention_charts.retention_heatmap()
st.plotly_chart(fig, use_container_width=True)

# Month-1 retention trend
st.markdown('<div class="section-header">Month-1 retention trend</div>', unsafe_allow_html=True)
fig2 = retention_charts.retention_trend()
st.plotly_chart(fig2, use_container_width=True)