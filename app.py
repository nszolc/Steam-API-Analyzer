import streamlit as st

from steam_api_analyzer import get_owned_games


@st.cache_data
def load_games():
    games = get_owned_games()
    games["hours_played"] = (games["playtime_forever"] / 60).round(1)
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
