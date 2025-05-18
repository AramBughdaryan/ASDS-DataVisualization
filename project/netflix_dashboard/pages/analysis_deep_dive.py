# netflix_dashboard/pages/analysis_deep_dive.py
import dash_bootstrap_components as dbc
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd

from data_loader import (
    GLOBAL_DF,
    get_genre_counts,
)  # Use the globally loaded and prepared DataFrame

MOVIE_COLOR = "#E50914"
TV_SHOW_COLOR = "#221F1F"
GENRE_COLOR_SCALE = px.colors.sequential.Viridis


def layout():
    if GLOBAL_DF is None:
        return dbc.Container([html.H3("Data could not be loaded for Deep Dive Page.")])

    all_ratings = sorted(GLOBAL_DF["rating"].dropna().unique().tolist())
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

    min_duration_movie = (
        int(GLOBAL_DF["duration_min"].min())
        if pd.notna(GLOBAL_DF["duration_min"].min())
        else 0
    )
    max_duration_movie = (
        int(GLOBAL_DF["duration_min"].max())
        if pd.notna(GLOBAL_DF["duration_min"].max())
        else 300
    )

    min_seasons_tv = (
        int(GLOBAL_DF["seasons"].min()) if pd.notna(GLOBAL_DF["seasons"].min()) else 1
    )
    max_seasons_tv = (
        int(GLOBAL_DF["seasons"].max()) if pd.notna(GLOBAL_DF["seasons"].max()) else 20
    )

    page_layout = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.H2("Detailed Analysis", className="text-center mb-4"),
                        width=12,
                    )
                ]
            ),
            # Row 1: Genre Analysis
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H5("Genre Analysis"),
                            dbc.Row(
                                [
                                    dbc.Col(dbc.Label("Content Type:"), width="auto"),
                                    dbc.Col(
                                        dcc.RadioItems(
                                            id="genre-content-type-radio",
                                            options=[
                                                {"label": "All", "value": "All"},
                                                {"label": "Movies", "value": "Movie"},
                                                {
                                                    "label": "TV Shows",
                                                    "value": "TV Show",
                                                },
                                            ],
                                            value="All",
                                            inline=True,
                                            labelStyle={"margin-right": "10px"},
                                        ),
                                        width="auto",
                                    ),
                                    dbc.Col(
                                        dbc.Label("Top N Genres:"),
                                        width="auto",
                                        className="ms-3",
                                    ),
                                    dbc.Col(
                                        dcc.Dropdown(
                                            id="genre-top-n-dropdown",
                                            options=[
                                                {"label": str(i), "value": i}
                                                for i in [5, 10, 15, 20, 25]
                                            ],
                                            value=15,
                                        ),
                                        width=2,
                                    ),
                                ]
                            ),
                            dcc.Graph(id="genre-analysis-bar"),
                        ],
                        width=12,
                        className="mb-4",
                    )
                ]
            ),
            # Row 2: Durations
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H5("Movie Duration Distribution"),
                            dbc.Label("Filter Movie Duration (minutes):"),
                            dcc.RangeSlider(
                                id="movie-duration-slider",
                                min=min_duration_movie,
                                max=max_duration_movie,
                                step=10,
                                value=[min_duration_movie, max_duration_movie],
                                marks={
                                    i: str(i)
                                    for i in range(
                                        min_duration_movie,
                                        max_duration_movie + 1,
                                        (
                                            60
                                            if (max_duration_movie - min_duration_movie)
                                            > 300
                                            else 30
                                        ),
                                    )
                                },
                                tooltip={"placement": "bottom", "always_visible": True},
                            ),
                            dcc.Graph(id="movie-duration-hist"),
                        ],
                        width=12,
                        lg=6,
                        className="mb-4",
                    ),
                    dbc.Col(
                        [
                            html.H5("TV Show Season Distribution"),
                            dbc.Label("Filter Max Number of Seasons:"),
                            dcc.Slider(
                                id="tv-season-slider",
                                min=min_seasons_tv,
                                max=max_seasons_tv,
                                step=1,
                                value=max_seasons_tv,
                                marks={
                                    i: str(i)
                                    for i in range(
                                        min_seasons_tv,
                                        max_seasons_tv + 1,
                                        (
                                            2
                                            if (max_seasons_tv - min_seasons_tv) > 10
                                            else 1
                                        ),
                                    )
                                },
                                tooltip={"placement": "bottom", "always_visible": True},
                            ),
                            dcc.Graph(id="tv-season-bar"),
                        ],
                        width=12,
                        lg=6,
                        className="mb-4",
                    ),
                ]
            ),
            # Row 3: Monthly Additions & Rating Distribution
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H5("Monthly Content Additions"),
                            dbc.Row(
                                [
                                    dbc.Col(dbc.Label("Select Year:"), width="auto"),
                                    dbc.Col(
                                        dcc.Dropdown(
                                            id="monthly-year-dropdown",
                                            options=[
                                                {"label": str(year), "value": year}
                                                for year in sorted(
                                                    GLOBAL_DF["year_added"]
                                                    .dropna()
                                                    .unique()
                                                    .astype(int),
                                                    reverse=True,
                                                )
                                            ],
                                            value=max_year_added,
                                        ),
                                        width=3,
                                    ),
                                    dbc.Col(
                                        dbc.Label("Content Type:"),
                                        width="auto",
                                        className="ms-3",
                                    ),
                                    dbc.Col(
                                        dcc.RadioItems(
                                            id="monthly-content-type-radio",
                                            options=[
                                                {"label": "Both", "value": "Both"},
                                                {"label": "Movies", "value": "Movie"},
                                                {
                                                    "label": "TV Shows",
                                                    "value": "TV Show",
                                                },
                                            ],
                                            value="Both",
                                            inline=True,
                                            labelStyle={"margin-right": "10px"},
                                        ),
                                        width="auto",
                                    ),
                                ]
                            ),
                            dcc.Graph(id="monthly-additions-line"),
                        ],
                        width=12,
                        lg=7,
                        className="mb-4",
                    ),
                    dbc.Col(
                        [
                            html.H5("Content Rating Distribution"),
                            dbc.Label("Filter Ratings:"),
                            dcc.Dropdown(  # Using Dropdown for multi-select as Checklist can get long
                                id="rating-filter-checklist",
                                options=[
                                    {"label": rating, "value": rating}
                                    for rating in all_ratings
                                ],
                                value=all_ratings,  # Default to all selected
                                multi=True,
                                placeholder="Select ratings...",
                            ),
                            dcc.Graph(id="rating-distribution-bar"),
                        ],
                        width=12,
                        lg=5,
                        className="mb-4",
                    ),
                ]
            ),
        ],
        fluid=True,
    )
    return page_layout


# --- Callbacks for Analysis Deep Dive Page ---
# Genre Analysis Bar Chart
@callback(
    Output("genre-analysis-bar", "figure"),
    [
        Input("genre-content-type-radio", "value"),
        Input("genre-top-n-dropdown", "value"),
    ],
)
def update_genre_analysis(content_type, top_n):
    if GLOBAL_DF is None:
        return px.scatter(title="Data not loaded")

    filtered_df = GLOBAL_DF.copy()
    if content_type != "All":
        filtered_df = GLOBAL_DF[GLOBAL_DF["type"] == content_type]

    genre_counts_df = get_genre_counts(filtered_df).head(top_n)

    fig = px.bar(
        genre_counts_df.sort_values(by="count", ascending=True),
        x="count",
        y="genre",
        orientation="h",
        title=f"Top {top_n} Genres ({content_type})",
        labels={"count": "Number of Titles", "genre": "Genre"},
        text="count",
        color="count",
        color_continuous_scale=GENRE_COLOR_SCALE,
    )
    fig.update_layout(title_x=0.5, yaxis_title="Genre", xaxis_title="Number of Titles")
    fig.update_traces(textposition="outside")
    return fig


# Movie Duration Histogram
@callback(
    Output("movie-duration-hist", "figure"), Input("movie-duration-slider", "value")
)
def update_movie_duration_hist(duration_range):
    if GLOBAL_DF is None:
        return px.scatter(title="Data not loaded")
    min_dur, max_dur = duration_range

    movies_df = GLOBAL_DF[
        (GLOBAL_DF["type"] == "Movie")
        & (GLOBAL_DF["duration_min"] >= min_dur)
        & (GLOBAL_DF["duration_min"] <= max_dur)
    ].copy()

    fig = px.histogram(
        movies_df,
        x="duration_min",
        title="Distribution of Movie Durations",
        labels={"duration_min": "Duration (minutes)"},
        marginal="box",
        color_discrete_sequence=[MOVIE_COLOR],
    )
    fig.update_layout(title_x=0.5, yaxis_title="Number of Movies")
    return fig


# TV Show Season Bar Chart
@callback(Output("tv-season-bar", "figure"), Input("tv-season-slider", "value"))
def update_tv_season_bar(max_seasons):
    if GLOBAL_DF is None:
        return px.scatter(title="Data not loaded")

    tv_show_df = GLOBAL_DF[
        (GLOBAL_DF["type"] == "TV Show") & (GLOBAL_DF["seasons"] <= max_seasons)
    ].copy()
    season_counts = tv_show_df["seasons"].value_counts().reset_index()
    season_counts.columns = ["seasons", "count"]
    season_counts = season_counts.sort_values("seasons")

    fig = px.bar(
        season_counts,
        x="seasons",
        y="count",
        title=f"Distribution of TV Show Seasons (Up to {max_seasons} Seasons)",
        labels={"seasons": "Number of Seasons", "count": "Number of TV Shows"},
        text_auto=True,
        color_discrete_sequence=[TV_SHOW_COLOR],
    )
    fig.update_layout(title_x=0.5, xaxis=dict(tickmode="linear", dtick=1))
    fig.update_traces(textposition="outside")
    return fig


# Monthly Content Additions Line Chart
@callback(
    Output("monthly-additions-line", "figure"),
    [
        Input("monthly-year-dropdown", "value"),
        Input("monthly-content-type-radio", "value"),
    ],
)
def update_monthly_additions_line(selected_year, content_type):
    if GLOBAL_DF is None:
        return px.scatter(title="Data not loaded")

    df_year_filtered = GLOBAL_DF[GLOBAL_DF["year_added"] == selected_year]

    if content_type != "Both":
        df_type_filtered = df_year_filtered[
            df_year_filtered["type"] == content_type
        ].copy()
        monthly_counts = (
            df_type_filtered.groupby(["month_name_added", "month_added"])
            .size()
            .reset_index(name="count")
        )
        monthly_counts = monthly_counts.sort_values("month_added")

        fig = px.line(
            monthly_counts,
            x="month_name_added",
            y="count",
            title=f"{content_type}s Added in {selected_year}",
            labels={"month_name_added": "Month", "count": "Number of Titles"},
            markers=True,
            color_discrete_sequence=[
                MOVIE_COLOR if content_type == "Movie" else TV_SHOW_COLOR
            ],
        )
    else:
        monthly_counts_unstacked = (
            df_year_filtered.groupby(["month_name_added", "month_added", "type"])
            .size()
            .unstack(fill_value=0)
            .reset_index()
        )
        monthly_counts_unstacked = monthly_counts_unstacked.sort_values("month_added")

        # Ensure both Movie and TV Show columns exist
        if "Movie" not in monthly_counts_unstacked:
            monthly_counts_unstacked["Movie"] = 0
        if "TV Show" not in monthly_counts_unstacked:
            monthly_counts_unstacked["TV Show"] = 0

        fig = px.line(
            monthly_counts_unstacked,
            x="month_name_added",
            y=["Movie", "TV Show"],
            title=f"Content Added in {selected_year}",
            labels={
                "month_name_added": "Month",
                "value": "Number of Titles",
                "variable": "Content Type",
            },
            markers=True,
            color_discrete_map={"Movie": MOVIE_COLOR, "TV Show": TV_SHOW_COLOR},
        )

    fig.update_layout(title_x=0.5, legend_title_text="Content Type")
    return fig


# Rating Distribution Bar Chart
@callback(
    Output("rating-distribution-bar", "figure"),
    Input("rating-filter-checklist", "value"),
)
def update_rating_distribution_bar(selected_ratings):
    if GLOBAL_DF is None:
        return px.scatter(title="Data not loaded")

    if not selected_ratings:  # Handle case where no ratings are selected
        filtered_df = pd.DataFrame(columns=["rating", "count"])
    else:
        filtered_df = GLOBAL_DF[GLOBAL_DF["rating"].isin(selected_ratings)]

    rating_counts = filtered_df["rating"].value_counts().reset_index()
    rating_counts.columns = ["rating", "count"]

    fig = px.bar(
        rating_counts,
        x="rating",
        y="count",
        title="Distribution of Content Ratings",
        labels={"rating": "Rating", "count": "Number of Titles"},
        text_auto=True,
        color="count",
        color_continuous_scale=px.colors.sequential.Plasma,
    )
    fig.update_layout(title_x=0.5, xaxis={"categoryorder": "total descending"})
    fig.update_traces(textposition="outside")
    return fig
