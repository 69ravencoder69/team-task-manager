import plotly.express as px
import plotly.graph_objects as go


def status_pie(data: dict, title: str = "Tasks by Status"):
    if not data or sum(data.values()) == 0:
        return None
    fig = px.pie(
        names=list(data.keys()),
        values=list(data.values()),
        title=title,
        color_discrete_sequence=["#FFA726", "#42A5F5", "#66BB6A"],
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e0e0e0",
        title_font_color="#fff",
    )
    return fig


def priority_bar(data: dict, title: str = "Tasks by Priority"):
    if not data or sum(data.values()) == 0:
        return None
    fig = px.bar(
        x=list(data.keys()),
        y=list(data.values()),
        title=title,
        color=list(data.keys()),
        color_discrete_map={"low": "#66BB6A", "medium": "#FFA726", "high": "#EF5350"},
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e0e0e0",
        title_font_color="#fff",
        showlegend=False,
    )
    return fig


def assignee_bar(data: dict, title: str = "Tasks by Assignee"):
    if not data:
        return None
    fig = go.Figure(go.Bar(x=list(data.values()), y=list(data.keys()), orientation="h"))
    fig.update_layout(
        title=title,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e0e0e0",
        title_font_color="#fff",
    )
    fig.update_traces(marker_color="#6C63FF")
    return fig
