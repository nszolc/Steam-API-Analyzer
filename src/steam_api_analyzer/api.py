"""Client for the Steam Web API."""

import json
import os
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

OWNED_GAMES_URL = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
APP_DETAILS_URL = "https://store.steampowered.com/api/appdetails"


def load_credentials() -> tuple[str, str]:
    """Read STEAM_API_KEY and STEAM_ID from the environment or a .env file."""
    load_dotenv()
    api_key = os.getenv("STEAM_API_KEY")
    steam_id = os.getenv("STEAM_ID")
    if not api_key or not steam_id:
        raise RuntimeError("STEAM_API_KEY and STEAM_ID must be set (see .env.example).")
    return api_key, steam_id


def fetch_owned_games(api_key: str, steam_id: str, timeout: float = 10) -> list[dict[str, Any]]:
    """Return the raw list of games owned by the account."""
    params: dict[str, str | int] = {
        "key": api_key,
        "steamid": steam_id,
        "include_appinfo": 1,
        "include_played_free_games": 1,
        "format": "json",
    }
    response = requests.get(OWNED_GAMES_URL, params=params, timeout=timeout)
    response.raise_for_status()

    # A private "Game details" setting still returns 200 OK, just with an empty response.
    games: list[dict[str, Any]] | None = response.json().get("response", {}).get("games")
    if games is None:
        raise RuntimeError(
            "The API returned no games. Make sure 'Game details' is set to Public "
            "in the Steam profile privacy settings."
        )
    return games


def get_owned_games() -> pd.DataFrame:
    """Fetch owned games using credentials from .env and return them as a DataFrame."""
    api_key, steam_id = load_credentials()
    return pd.DataFrame(fetch_owned_games(api_key, steam_id))


def fetch_genres(appid: int, timeout: float = 10) -> list[str]:
    """Return genre names for one game from the Steam Store API."""
    params = {"appids": appid}
    response = requests.get(APP_DETAILS_URL, params=params, timeout=timeout)
    response.raise_for_status()

    app: dict[str, Any] = response.json().get(str(appid), {})
    # Apps no longer in the store return {"success": false} without a "data" key.
    if not app.get("success"):
        return []

    genres: list[dict[str, str]] = app["data"].get("genres", [])
    return [g["description"] for g in genres]


def get_genres(appids, cache_path: Path) -> dict[int, list[str]]:
    """Return genres for each appid, using a JSON file as a cache."""
    if cache_path.exists():
        cache = json.loads(cache_path.read_text())
    else:
        cache: dict = {}

    for appid in appids:
        key = str(appid)
        if key not in cache:
            cache[key] = fetch_genres(appid)
            # Save after every request so a failure halfway keeps what was already fetched.
            cache_path.write_text(json.dumps(cache, indent=2))
    genres_int = {int(key): value for key, value in cache.items()}
    return genres_int
