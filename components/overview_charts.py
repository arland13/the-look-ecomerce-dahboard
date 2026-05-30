import plotly.graph_objects as go
import plotly.express as px
from data import revenue_df, ltv_df, churn_df

def gmv_trend():
    #get data frame
    growth = revenue_df.get_growth_df()

    fig = go.Figure()
    fig.add_bar(
    x=growth["order_month"], 
    y=growth["gmv"], 
    name="GMV", 
    marker_color="#378ADD", 
    opacity=0.85
)
    fig.add_scatter(
    x=growth["order_month"], 
    y=growth["ytd_revenue"], 
    name="YTD Revenue",
    mode="lines", 
    line=dict(color="#1D9E75", 
    width=2.5)
)
    fig.update_layout(
    height=320, 
    margin=dict(l=0,r=0,t=10,b=0),
    legend=dict(orientation="h", y=1.1), 
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False),
    yaxis=dict(gridcolor="#f0f0f0", tickprefix="$")
)
    return fig

def ltv_distribution():
    # get data frame
    df_ltv = ltv_df.get_ltv_df()

    quartile_labels = {1: "Bronze", 2: "Silver", 3: "Gold", 4: "Platinum"}
    df_ltv["tier"] = df_ltv["ltv_quartile"].map(quartile_labels)
    tier_summary = df_ltv.groupby("tier")["ltv"].agg(["mean", "count"]).reset_index()
    tier_summary.columns = ["Tier", "Avg LTV", "Customers"]
    colors = {"Bronze": "#B4B2A9", "Silver": "#85B7EB", "Gold": "#EF9F27", "Platinum": "#7F77DD"}
    fig = px.bar(
        tier_summary, 
        x="Tier", 
        y="Avg LTV", 
        color="Tier",
        color_discrete_map=colors, 
        text_auto=".2s"
        )
    fig.update_layout(
        height=280, 
        showlegend=False, 
        margin=dict(l=0,r=0,t=10,b=0),
        plot_bgcolor="rgba(0,0,0,0)", 
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="#f0f0f0", tickprefix="$"), 
        xaxis_title=""
        )
    
    return fig

def cust_churn_stat():
    # get data frame
    df_churn = churn_df.get_churn_df()

    churn_counts = df_churn["churn_status"].value_counts().reset_index()
    churn_counts.columns = ["Status", "Count"]
    churn_colors = {"Active": "#1D9E75", "At Risk": "#EF9F27", "Churned": "#E24B4A"}
    fig = px.pie(
        churn_counts, 
        values="Count", 
        names="Status",
        color="Status", 
        color_discrete_map=churn_colors, 
        hole=0.55)
    fig.update_layout(
        height=280, 
        margin=dict(l=0,r=0,t=10,b=0),
        paper_bgcolor="rgba(0,0,0,0)", 
        legend=dict(orientation="h", y=-0.1)
        )
    fig.update_traces(textposition="outside", textinfo="percent+label")

    return fig