import dash_bootstrap_components as dbc
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

from data_loader import GLOBAL_DF


MOVIE_COLOR = "#E50914"
TV_SHOW_COLOR = "#221F1F"
PRIMARY_COLOR_SCALE = px.colors.sequential.Reds
SECONDARY_COLOR_SCALE = px.colors.sequential.Blues


def layout():
    if GLOBAL_DF is None:
        return dbc.Container([html.H3("Data could not be loaded for Overview Page.")])

    min_year_added = (
        int(GLOBAL_DF["year_added"].min())
        if pd.notna(GLOBAL_DF["year_added"].min())
        else 2000
    )
    max_year_added = (
        int(GLOBAL_DF["year_added"].max())
        if pd.notna(GLOBAL_DF["year_added"].max())
        else 2025
    )

    unique_release_years = sorted(
        GLOBAL_DF["release_year"].dropna().unique().astype(int)
    )
    min_release_year = unique_release_years[0] if unique_release_years else 1920
    max_release_year = unique_release_years[-1] if unique_release_years else 2025

    page_layout = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.H2("Content Overview", className="text-center mb-4"),
                        width=12,
                    )
                ]
            ),
            # Row 1: Content Type Distribution & Top N Controls
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(id="content-type-pie"),
                        width=12,
                        lg=6,
                        className="mb-4",
                    ),
                    dbc.Col(
                        [
                            html.H5("Top N Controls"),
                            dbc.Label("Select N for Top Countries/Directors:"),
                            dcc.Slider(
                                id="top-n-slider",
                                min=3,
                                max=15,
                                step=1,
                                value=10,
                                marks={i: str(i) for i in range(3, 16, 2)},
                            ),
                            html.Br(),
                            dcc.Graph(id="top-countries-bar"),
                        ],
                        width=12,
                        lg=6,
                        className="mb-4",
                    ),
                ],
                align="center",
            ),
            # Row 2: Top Directors & Release Year Trend Controls
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(id="top-directors-bar"),
                        width=12,
                        lg=6,
                        className="mb-4",
                    ),
                    dbc.Col(
                        [
                            html.H5("Content Release Trend Controls"),
                            dbc.Label("Select Release Year Range:"),
                            dcc.RangeSlider(
                                id="release-year-slider",
                                min=min_release_year,
                                max=max_release_year,
                                step=1,
                                value=[
                                    max_release_year - 20,
                                    max_release_year,
                                ],  # Default to last 20 years
                                marks={
                                    year: str(year)
                                    for year in range(
                                        min_release_year,
                                        max_release_year + 1,
                                        (
                                            10
                                            if (max_release_year - min_release_year)
                                            > 50
                                            else 5
                                        ),
                                    )
                                },
                                tooltip={"placement": "bottom", "always_visible": True},
                            ),
                            html.Br(),
                            dcc.Graph(id="content-release-year-line"),
                        ],
                        width=12,
                        lg=6,
                        className="mb-4",
                    ),
                ],
                align="center",
            ),
            # Row 3: Trend of Content Types Added Over Years
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H5("Trend of Content Types Added to Netflix"),
                            dbc.Label("Select Year Added Range:"),
                            dcc.RangeSlider(
                                id="year-added-slider-overview",
                                min=min_year_added,
                                max=max_year_added,
                                step=1,
                                value=[min_year_added, max_year_added],
                                marks={
                                    year: str(year)
                                    for year in range(
                                        min_year_added,
                                        max_year_added + 1,
                                        (
                                            2
                                            if (max_year_added - min_year_added) > 10
                                            else 1
                                        ),
                                    )
                                },
                                tooltip={"placement": "bottom", "always_visible": True},
                            ),
                            dcc.Graph(id="content-types-added-trend-area"),
                        ],
                        width=12,
                        className="mb-4",
                    )
                ]
            ),
        ],
        fluid=True,
    )
    return page_layout


# --- Callbacks for Overview Page ---


# Content Type Pie Chart
@callback(
    Output("content-type-pie", "figure"), Input("url", "pathname")
)  # Trigger on page load
def update_content_type_pie(
    _,
):  # Input can be dummy if no specific filter from this page
    if GLOBAL_DF is None:
        return px.scatter(title="Data not loaded")
    content_counts = GLOBAL_DF["type"].value_counts()
    fig = px.pie(
        names=content_counts.index,
        values=content_counts.values,
        title="Movie vs. TV Show Distribution",
        color_discrete_map={"Movie": MOVIE_COLOR, "TV Show": TV_SHOW_COLOR},
        hole=0.3,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(title_x=0.5, legend_title_text="Content Type")
    return fig


# Top N Countries Bar Chart
@callback(Output("top-countries-bar", "figure"), Input("top-n-slider", "value"))
def update_top_countries_bar(top_n):
    if GLOBAL_DF is None:
        return px.scatter(title="Data not loaded")
    # Simplified: considers the first country listed
    country_counts = (
        GLOBAL_DF["country"]
        .dropna()
        .apply(lambda x: x.split(",")[0].strip())
        .value_counts()
        .head(top_n)
    )
    fig = px.bar(
        x=country_counts.index,
        y=country_counts.values,
        title=f"Top {top_n} Countries Producing Content",
        labels={"x": "Country", "y": "Number of Titles"},
        text_auto=True,
        color_discrete_sequence=[SECONDARY_COLOR_SCALE[5]],  # A blue shade
    )
    fig.update_layout(title_x=0.5, xaxis_tickangle=-30)
    fig.update_traces(textposition="outside")
    return fig


# Top N Directors Bar Chart
@callback(Output("top-directors-bar", "figure"), Input("top-n-slider", "value"))
def update_top_directors_bar(top_n):
    if GLOBAL_DF is None:
        return px.scatter(title="Data not loaded")
    directors_count = GLOBAL_DF["director"].dropna().value_counts().head(top_n)
    fig = px.bar(
        x=directors_count.index,
        y=directors_count.values,
        title=f"Top {top_n} Directors by Number of Titles",
        labels={"x": "Director", "y": "Number of Titles"},
        text_auto=True,
        color_discrete_sequence=[PRIMARY_COLOR_SCALE[5]],  # A red shade
    )
    fig.update_layout(title_x=0.5, xaxis_tickangle=-45)
    fig.update_traces(textposition="outside")
    return fig


# Content Release Over Years Line Chart
@callback(
    Output("content-release-year-line", "figure"), Input("release-year-slider", "value")
)
def update_content_release_line(year_range):
    if GLOBAL_DF is None:
        return px.scatter(title="Data not loaded")
    min_year, max_year = year_range
    filtered_df = GLOBAL_DF[
        (GLOBAL_DF["release_year"] >= min_year)
        & (GLOBAL_DF["release_year"] <= max_year)
    ]
    released_year_counts = filtered_df["release_year"].value_counts().sort_index()
    fig = px.line(
        x=released_year_counts.index,
        y=released_year_counts.values,
        title="Content Release Trend (by Original Release Year)",
        labels={"x": "Release Year", "y": "Number of Titles"},
        markers=True,
        color_discrete_sequence=["#FFA07A"],  # Light Salmon
    )
    fig.update_layout(title_x=0.5)
    return fig


# Trend of Content Types Added to Netflix (Area Chart)
@callback(
    Output("content-types-added-trend-area", "figure"),
    Input("year-added-slider-overview", "value"),
)
def update_content_types_added_trend(year_range):
    if GLOBAL_DF is None:
        return px.scatter(title="Data not loaded")
    min_year, max_year = year_range

    df_filtered = GLOBAL_DF[
        (GLOBAL_DF["year_added"] >= min_year) & (GLOBAL_DF["year_added"] <= max_year)
    ]

    type_trend = (
        df_filtered.groupby(["year_added", "type"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    if "Movie" not in type_trend.columns:
        type_trend["Movie"] = 0
    if "TV Show" not in type_trend.columns:
        type_trend["TV Show"] = 0

    fig = px.area(
        type_trend,
        x="year_added",
        y=["Movie", "TV Show"],
        title="Trend of Movies vs. TV Shows Added to Netflix",
        labels={
            "year_added": "Year Added to Netflix",
            "value": "Number of Titles Added",
            "variable": "Content Type",
        },
        color_discrete_map={"Movie": MOVIE_COLOR, "TV Show": TV_SHOW_COLOR},
    )
    fig.update_layout(title_x=0.5, legend_title_text="Content Type")
    return fig
