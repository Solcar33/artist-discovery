import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("LASTFM_API_KEY")
BASE_URL = "https://ws.audioscrobbler.com/2.0/"

def get_similar_artists(artiste, limit=10):
    """Retourne les artistes similaires à 'artiste' selon last.fm"""
    if not API_KEY:
        raise RuntimeError("LASTFM_API_KEY introuvable : vérifie le fichier .env")

    params = {
        "method": "artist.getsimilar",
        "artist": artiste,
        "api_key": API_KEY,
        "format": "json",
        "limit": limit,
    }
    reponse = requests.get(BASE_URL, params=params, timeout=10)
    if reponse.status_code != 200:
        raise RuntimeError(f"last.fm a répondu avec le code {reponse.status_code}")

    data = reponse.json()
    if "error" in data:
        raise RuntimeError(f"Erreur last.fm {data['error']} : {data['message']}")
    return data["similarartists"]["artist"]


if __name__ == "__main__":
    for a in get_similar_artists("Foo Fighters", 5):
        print(a["name"], a["match"])
        