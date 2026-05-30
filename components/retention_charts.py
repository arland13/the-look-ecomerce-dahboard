from data import retention_df
import plotly.graph_objects as go
import pandas as pd

def retention_heatmap():
        df_ret = retention_df.get_retention_df()

        # Pivot to heatmap
        pivot = df_ret.pivot_table(
        index="cohort_month",
        columns="months_since_first",
        values="retention_rate_pct"
    )
        fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=[f"Month {i}" for i in pivot.columns],
        y=pivot.index,
        colorscale=[
            [0.0, "#FAECE7"], [0.3, "#F0997B"],
            [0.6, "#1D9E75"], [1.0, "#085041"]
        ],
        text=[[f"{v:.1f}%" if pd.notna(v) else "" for v in row] for row in pivot.values],
        texttemplate="%{text}",
        textfont=dict(size=11),
        showscale=True,
        colorbar=dict(title="Retention %", ticksuffix="%"),
    ))
        fig.update_layout(
        height=max(300, len(pivot) * 32 + 80),
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(side="top"),
    )
        return fig
        
def retention_trend():
    df_ret = retention_df.get_retention_df()
    m1 = df_ret[df_ret["months_since_first"] == 1].copy()
    m1["cohort_month"] = pd.to_datetime(m1["cohort_month"])
    fig = go.Figure()
    fig.add_scatter(
        x=m1["cohort_month"], 
        y=m1["retention_rate_pct"],
        mode="lines+markers", 
        name="M1 Retention",
        line=dict(color="#1D9E75", width=2.5), 
        marker=dict(size=7)
        )
    fig.add_hline(
        y=m1["retention_rate_pct"].mean(), 
        line_dash="dash",
        line_color="#adb5bd", 
        annotation_text="Average"
        )
    fig.update_layout(
        height=260, 
        margin=dict(l=0,r=0,t=10,b=0),
        plot_bgcolor="rgba(0,0,0,0)", 
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(
              gridcolor="#f0f0f0", 
              ticksuffix="%"
              ),
        xaxis=dict(showgrid=False))
    
    return fig