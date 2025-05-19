# netflix_dashboard/data_loader.py
import os
import pandas as pd
import numpy as np
from collections import Counter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "netflix.csv")
print("DATA PATH", DATA_PATH)


def load_and_prepare_data(file_path=DATA_PATH):
    """Loads and prepares the Netflix dataset."""
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found. Please check the path.")
        return None

    # Convert 'date_added' to datetime objects
    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")

    # Create a normalized title column for deduplication
    df["normalized_title"] = df["title"].str.lower().str.strip()
    df = df.drop_duplicates(subset="normalized_title", keep="first")

    if "show_id" in df.columns:
        df["show_id"] = df["show_id"].str.replace("s", "", regex=False).astype(int)

    # Extract year and month from 'date_added'
    df["year_added"] = df["date_added"].dt.year
    df["month_added"] = df["date_added"].dt.month
    df["month_name_added"] = df["date_added"].dt.strftime("%B")  # Full month name

    # Clean duration for Movies
    movie_mask = df["type"] == "Movie"
    if "duration" in df.columns:
        df.loc[movie_mask, "duration_min"] = pd.to_numeric(
            df.loc[movie_mask, "duration"].str.replace(" min", "", regex=False),
            errors="coerce",
        )

        # Clean duration for TV Shows (number of seasons)
        tv_show_mask = df["type"] == "TV Show"
        df.loc[tv_show_mask, "seasons"] = pd.to_numeric(
            df.loc[tv_show_mask, "duration"].str.split(" ").str[0], errors="coerce"
        )
        df["seasons"] = df["seasons"].astype("Int64")  # Use nullable integer type

    # Process 'listed_in' for genre analysis
    if "listed_in" in df.columns:
        df["genres_list"] = df["listed_in"].dropna().str.split(", ")
    else:
        df["genres_list"] = pd.Series([[] for _ in range(len(df))])

    # Drop columns no longer needed immediately for dashboarding, but keep processed ones
    df.drop(columns=["normalized_title"], inplace=True, errors="ignore")
    # We keep 'date_added' as it might be useful for time-series components

    # Handle missing values in key numeric/categorical columns for plotting
    df["year_added"] = df["year_added"].astype("Int64")
    df["month_added"] = df["month_added"].astype("Int64")
    df["release_year"] = df["release_year"].astype("Int64")

    df["country"] = df["country"].replace("Not Given", np.nan)
    df["director"] = df["director"].replace("Not Given", np.nan)
    df["rating"] = df["rating"].replace("Not Given", np.nan)

    return df


# Load data once globally for the app to use
GLOBAL_DF = load_and_prepare_data()


def get_genre_counts(df_filtered):
    """Helper to get genre counts from a pre-filtered DataFrame."""
    if (
        "genres_list" not in df_filtered.columns
        or df_filtered["genres_list"].isnull().all()
    ):
        return pd.DataFrame(columns=["genre", "count"])

    all_genres = [
        genre for sublist in df_filtered["genres_list"].dropna() for genre in sublist
    ]
    genre_counts = Counter(all_genres)
    return pd.DataFrame(genre_counts.items(), columns=["genre", "count"]).sort_values(
        by="count", ascending=False
    )


if __name__ == "__main__":
    # Test the loader
    df_test = load_and_prepare_data()
    if df_test is not None:
        print("Data loaded and prepared successfully!")
        print(f"\nShape: {df_test.shape}")
        print("\nInfo:")
        df_test.info()
        print("\nFirst 5 rows:")
        print(df_test.head())
        print("\nMovie duration example:")
        print(
            df_test[df_test["type"] == "Movie"][
                ["title", "duration", "duration_min"]
            ].head()
        )
        print("\nTV Show seasons example:")
        print(
            df_test[df_test["type"] == "TV Show"][
                ["title", "duration", "seasons"]
            ].head()
        )
        print("\nGenre list example:")
        print(df_test[["title", "listed_in", "genres_list"]].head())
        print("\nGenre counts (overall):")
        print(get_genre_counts(df_test).head())
    else:
        print("Failed to load data.")
