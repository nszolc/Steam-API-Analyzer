from pathlib import Path

import matplotlib.pyplot as plt
import streamlit as st

from steam_api_analyzer import get_genres, get_owned_games


@st.cache_data
def load_games():
    games = get_owned_games()
    games["hours_played"] = (games["playtime_forever"] / 60).round(1)
    genres = get_genres(games["appid"], Path("data/genres_cache.json"))
    games["genres"] = games["appid"].map(genres)
    return games


st.title("My Steam Library")

games = load_games()

total_hours = games["hours_played"].sum()
never_launched = len(games[games["playtime_forever"] == 0])
never_launched_share = never_launched / len(games)

col1, col2, col3 = st.columns(3)
col1.metric("Games", len(games))
col2.metric("Total Hours Played", f"{total_hours:.0f} h")
col3.metric("Never Launched", f"{never_launched} ({never_launched_share:.0%})")

top10 = games.sort_values("hours_played", ascending=False).head(10)

st.subheader("Most Played Games")
fig, ax = plt.subplots()
ax.barh(top10["name"], top10["hours_played"])
ax.invert_yaxis()
ax.set_xlabel("Hours Played")
ax.spines[["top", "right"]].set_visible(False)
ax.bar_label(ax.containers[0], fmt="%.1f", padding=3)
fig.tight_layout()
st.pyplot(fig)

games_exploded = games.explode("genres", ignore_index=True)
genre_hours = games_exploded.groupby("genres")["hours_played"].sum().sort_values(ascending=False)

st.subheader("Hours Played by Genre (a game counts in each of its genres)")
fig, ax = plt.subplots()
ax.barh(genre_hours.index, genre_hours.values)
ax.invert_yaxis()
ax.set_xlabel("Hours Played")
ax.spines[["top", "right"]].set_visible(False)
ax.bar_label(ax.containers[0], fmt="%.1f", padding=3)
fig.tight_layout()
st.pyplot(fig)
