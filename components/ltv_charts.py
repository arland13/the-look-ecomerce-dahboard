import plotly.express as px

def ltv_distribution_chart(df_ltv):
    fig = px.histogram(
        df_ltv[df_ltv["ltv"] < df_ltv["ltv"].quantile(0.95)],
        x="ltv", nbins=50, 
        color_discrete_sequence=["#378ADD"]
    )

    fig.update_layout(
        height=300, margin=dict(l=0,r=0,t=10,b=0),
        plot_bgcolor="rgba(0,0,0,0)", 
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(tickprefix="$", showgrid=False),
        yaxis=dict(gridcolor="#f0f0f0"), bargap=0.05
    )

    return fig

def ltv_tier_chart(df_ltv):
    tier_df = df_ltv.copy()
    tier_df = tier_df.groupby("tier").agg(
        customers=("user_id_x","count"),
        avg_ltv=("ltv","mean"),
        avg_orders=("total_orders","mean")
    ).reset_index()
    colors = {"Bronze": "#B4B2A9", "Silver": "#85B7EB", "Gold": "#EF9F27", "Platinum": "#7F77DD"}
    fig = px.bar(
        tier_df, 
        x="tier", 
        y="avg_ltv", 
        color="tier",
        color_discrete_map=colors, 
        text_auto="$.2s"
        )
    fig.update_layout(
        height=300, 
        showlegend=False, 
        margin=dict(l=0,r=0,t=10,b=0),
        plot_bgcolor="rgba(0,0,0,0)", 
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="#f0f0f0", 
        tickprefix="$"),
        xaxis_title=""
        )
    
    return fig