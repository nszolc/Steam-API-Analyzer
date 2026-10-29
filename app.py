from pathlib import Path

import matplotlib.pyplot as plt
import streamlit as st

from steam_api_analyzer import get_genres, get_owned_games

plt.rcParams.update(
    {
        "figure.facecolor": "#1e1530",
        "axes.facecolor": "#1e1530",
        "axes.edgecolor": "#ece6f7",
        "axes.labelcolor": "#ece6f7",
        "text.color": "#ece6f7",
        "xtick.color": "#ece6f7",
        "ytick.color": "#ece6f7",
        "axes.prop_cycle": plt.cycler(color=["#b794f6"]),
    }
)


@st.cache_data
def load_games():
    games = get_owned_games()
    games["hours_played"] = (games["playtime_forever"] / 60).round(1)
    genres = get_genres(games["appid"], Path("data/genres_cache.json"))
    games["genres"] = games["appid"].map(genres)
    return games


st.set_page_config(page_title="My Steam Library", page_icon="🎮", layout="wide")

st.title("My Steam Library")


games = load_games()
games_exploded = games.explode("genres", ignore_index=True)
all_genres = sorted(games_exploded["genres"].dropna().unique())
st.sidebar.header("Filters")
min_hours = st.sidebar.slider("Minimum hours played", 0, int(games["hours_played"].max()), 0)
filtered = games[games["hours_played"] >= min_hours]
selected_genres = st.sidebar.multiselect("Genres", all_genres, all_genres)

if len(selected_genres) < len(all_genres):
    matching_appids = games_exploded[games_exploded["genres"].isin(selected_genres)][
        "appid"
    ].unique()
    filtered = filtered[filtered["appid"].isin(matching_appids)]

if filtered.empty:
    st.warning("There is no filtered data to display. Please adjust the filters in the sidebar.")
    st.stop()


total_hours = filtered["hours_played"].sum()
never_launched = len(filtered[filtered["playtime_forever"] == 0])
never_launched_share = never_launched / len(filtered)


col1, col2, col3 = st.columns(3)
col1.metric("Games", len(filtered))
col2.metric("Total Hours Played", f"{total_hours:.0f} h")
col3.metric("Never Launched", f"{never_launched} ({never_launched_share:.0%})")

top10 = filtered.sort_values("hours_played", ascending=False).head(10)

st.subheader("Most Played Games")
st.caption("Top 10 games by total playtime.")
fig, ax = plt.subplots(figsize=(10, 4))
ax.barh(top10["name"], top10["hours_played"])
ax.invert_yaxis()
ax.set_xlabel("Hours Played")
ax.spines[["top", "right"]].set_visible(False)
ax.bar_label(ax.containers[0], fmt="%.1f", padding=3)
fig.tight_layout()
st.pyplot(fig)

filtered_exploded = filtered.explode("genres", ignore_index=True)
genre_hours = filtered_exploded.groupby("genres")["hours_played"].sum().sort_values(ascending=False)

st.subheader("Hours Played by Genre")
st.caption("A game counts in each of its genres, so the hours add up to more than the total.")
fig, ax = plt.subplots(figsize=(10, 4))
ax.barh(genre_hours.index, genre_hours.values)
ax.invert_yaxis()
ax.set_xlabel("Hours Played")
ax.spines[["top", "right"]].set_visible(False)
ax.bar_label(ax.containers[0], fmt="%.1f", padding=3)
fig.tight_layout()
st.pyplot(fig)
