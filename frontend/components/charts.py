import plotly.express as px
import plotly.graph_objects as go

GRAYSCALE = ["#6b7280", "#9ca3af", "#d1d5db", "#4b5563", "#374151"]


def _base_layout(fig, title: str = ""):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e5e5e5",
        title_font_color="#ffffff",
        title=title,
        legend=dict(font=dict(color="#e5e5e5")),
    )
    fig.update_xaxes(gridcolor="#333", zerolinecolor="#333")
    fig.update_yaxes(gridcolor="#333", zerolinecolor="#333")
    return fig


def status_pie(data: dict, title: str = ""):
    if not data or sum(data.values()) == 0:
        return None
    fig = px.pie(names=list(data.keys()), values=list(data.values()), color_discrete_sequence=GRAYSCALE)
    return _base_layout(fig, title or "Tasks by Status")


def priority_bar(data: dict, title: str = ""):
    if not data or sum(data.values()) == 0:
        return None
    fig = px.bar(x=list(data.keys()), y=list(data.values()), color_discrete_sequence=["#9ca3af"])
    fig.update_layout(showlegend=False)
    return _base_layout(fig, title or "Tasks by Priority")


def assignee_bar(data: dict, title: str = ""):
    if not data:
        return None
    fig = go.Figure(go.Bar(x=list(data.values()), y=list(data.keys()), orientation="h", marker_color="#9ca3af"))
    return _base_layout(fig, title or "Tasks by Assignee")
