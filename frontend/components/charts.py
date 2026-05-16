import plotly.express as px
import plotly.graph_objects as go

# Vibrant, bright color palette for charts
BRIGHT_PALETTE = ["#FF3366", "#33FF99", "#3366FF", "#FF9933", "#CC33FF", "#00FFFF", "#FFFF33"]


def _base_layout(fig, title: str = ""):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e5e5e5",
        title_font_color="#ffffff",
        title=title,
        legend=dict(font=dict(color="#e5e5e5")),
        margin=dict(l=20, r=20, t=40, b=20),
    )
    fig.update_xaxes(gridcolor="#333", zerolinecolor="#333")
    fig.update_yaxes(gridcolor="#333", zerolinecolor="#333")
    return fig


def status_pie(data: dict, title: str = ""):
    if not data or sum(data.values()) == 0:
        return None
    # Use distinct bright colors for different statuses
    fig = px.pie(
        names=list(data.keys()),
        values=list(data.values()),
        color_discrete_sequence=BRIGHT_PALETTE,
        hole=0.4
    )
    return _base_layout(fig, title or "Tasks by Status")


def priority_bar(data: dict, title: str = ""):
    if not data or sum(data.values()) == 0:
        return None
    # Map priorities to specific bright colors if possible, otherwise use palette
    fig = px.bar(
        x=list(data.keys()),
        y=list(data.values()),
        color=list(data.keys()),
        color_discrete_sequence=BRIGHT_PALETTE
    )
    fig.update_layout(showlegend=False)
    return _base_layout(fig, title or "Tasks by Priority")


def assignee_bar(data: dict, title: str = ""):
    if not data:
        return None
    # Horizontal bar chart with vibrant colors
    fig = px.bar(
        x=list(data.values()),
        y=list(data.keys()),
        orientation="h",
        color=list(data.keys()),
        color_discrete_sequence=BRIGHT_PALETTE
    )
    fig.update_layout(showlegend=False)
    return _base_layout(fig, title or "Tasks by Assignee")
