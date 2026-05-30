from data import churn_df
import plotly.express as px

def churn_breakdown():
    df_churn = churn_df.get_churn_df()

    churn_counts = df_churn["churn_status"].value_counts()

    df_pie = churn_counts.reset_index()
    df_pie.columns = ["Status", "Count"]

    churn_colors = {
        "Active": "#1D9E75",
        "At Risk": "#EF9F27",
        "Churned": "#E24B4A"
    }

    fig = px.pie(
        df_pie,
        values="Count",
        names="Status",
        color="Status",
        color_discrete_map=churn_colors,
        hole=0.6
    )

    fig.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)"
    )

    return fig

def revenue_at_risk():
    df_churn = churn_df.get_churn_df()
    churn_colors = {"Active": "#1D9E75", "At Risk": "#EF9F27", "Churned": "#E24B4A"}

    rev_by_status = df_churn.groupby("churn_status")["total_revenue"].sum().reset_index()
    rev_by_status.columns = ["Status", "Revenue"]
    fig = px.bar(
        rev_by_status, 
        x="Status", 
        y="Revenue", 
        color="Status",
        color_discrete_map=churn_colors, 
        text_auto="$.3s"
        )
    fig.update_layout(
        height=300, 
        showlegend=False, 
        margin=dict(l=0,r=0,t=10,b=0),
        plot_bgcolor="rgba(0,0,0,0)", 
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="#f0f0f0", tickprefix="$"), 
        xaxis_title=""
        )
    return fig

def days_since_last_order():
    df_churn = churn_df.get_churn_df()
    churn_colors = {"Active": "#1D9E75", "At Risk": "#EF9F27", "Churned": "#E24B4A"}

    fig = px.histogram(
        df_churn, 
        x="days_since_last_order", 
        color="churn_status",
        color_discrete_map=churn_colors, 
        nbins=60,
        labels={"days_since_last_order": "Days since last order", "churn_status": "Status"})
    fig.add_vline(
        x=90,  
        line_dash="dash", 
        line_color="#EF9F27", 
        annotation_text="At-risk threshold (90d)", 
        annotation_position="top right", 
        annotation_yshift=0
    )
    fig.add_vline(
        x=180, line_dash="dash", 
        line_color="#E24B4A", 
        annotation_text="Churned threshold (180d)",
        annotation_position="top left",
        annotation_yshift=-20
    )
    fig.update_layout(
        height=280, 
        margin=dict(l=0,r=0,t=10,b=0),
        plot_bgcolor="rgba(0,0,0,0)", 
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="#f0f0f0"), 
        xaxis=dict(showgrid=False),
        legend=dict(orientation="h", y=1.1), 
        bargap=0.05
        )
    
    return fig