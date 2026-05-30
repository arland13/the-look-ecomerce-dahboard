import plotly.graph_objects as go

def create_metric_chart(growth_filtered, metric):

    metric_map = {
        "GMV": "gmv",
        "AOV": "aov",
        "Orders": "num_orders"
    }

    selected_metric = metric_map[metric]

    # Dynamic formatting
    if metric in ["GMV", "AOV"]:
        tickprefix = "$"
    else:
        tickprefix = ""

    fig = go.Figure()

    # GMV = line
    if metric == "GMV":
        fig.add_scatter(
            x=growth_filtered["order_month"],
            y=growth_filtered[selected_metric],
            mode="lines",
            name=metric,
            line=dict(width=3)
        )

    # AOV = line + markers
    elif metric == "AOV":
        fig.add_scatter(
            x=growth_filtered["order_month"],
            y=growth_filtered[selected_metric],
            mode="lines+markers",
            name=metric,
            line=dict(width=2.5),
            marker=dict(size=6)
        )

    # Orders = bar
    elif metric == "Orders":
        fig.add_bar(
            x=growth_filtered["order_month"],
            y=growth_filtered[selected_metric],
            name=metric,
            opacity=0.85
        )

    fig.update_layout(
        height=320,
        margin=dict(l=0, r=0, t=10, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(
            gridcolor="#f0f0f0",
            tickprefix=tickprefix
        )
    )

    return fig


def create_growth_chart(growth_filtered):

    fig = go.Figure()

    fig.add_bar(
        x=growth_filtered["order_month"],
        y=growth_filtered["mom_growth_pct"],
        name="MoM %",
        marker_color="#378ADD",
        opacity=0.8
    )

    fig.add_scatter(
        x=growth_filtered["order_month"],
        y=growth_filtered["yoy_growth_pct"],
        name="YoY %",
        mode="lines+markers",
        line=dict(
            color="#D85A30",
            width=2.5
        ),
        marker=dict(size=6)
    )

    fig.add_hline(
        y=0,
        line_width=1,
        line_dash="dash",
        line_color="#adb5bd"
    )

    fig.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=10, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(
            gridcolor="#f0f0f0",
            ticksuffix="%"
        ),
        xaxis=dict(showgrid=False),
        legend=dict(
            orientation="h",
            y=1.1
        )
    )

    return fig