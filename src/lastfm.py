import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("LASTFM_API_KEY")
BASE_URL = "https://ws.audioscrobbler.com/2.0/"

def _appeler(methode, **params):
    """Appelle l'API Last.fm et renvoie le JSON décodé."""
    if not API_KEY:
        raise RuntimeError("LASTFM_API_KEY introuvable : vérifie le fichier .env")

    params = {"method": methode, "api_key": API_KEY, "format": "json", **params}
    reponse = requests.get(BASE_URL, params=params, timeout=10)
    if reponse.status_code != 200:
        raise RuntimeError(f"Last.fm a répondu avec le code {reponse.status_code}")

    data = reponse.json()
    if "error" in data:
        raise RuntimeError(f"Erreur Last.fm {data['error']} : {data['message']}")
    return data


def get_similar_artists(artiste, limit=10):
    """Retourne les artistes similaires à `artiste` selon Last.fm."""
    data = _appeler("artist.getsimilar", artist=artiste, limit=limit)
    return data["similarartists"]["artist"]


def get_artist_info(artiste):
    """Retourne les infos principales d'un artiste selon Last.fm."""
    data = _appeler("artist.getinfo", artist=artiste, autocorrect=1)
    info = data["artist"]
    return {
        "nom": info["name"],
        "mbid": info.get("mbid", ""),
        "auditeurs": int(info["stats"]["listeners"]),
        "ecoutes": int(info["stats"]["playcount"]),
        "tags": [tag["name"] for tag in info["tags"]["tag"]],
        "bio": info["bio"]["summary"],
        "url": info["url"],
    }


if __name__ == "__main__":
    info = get_artist_info("Massive Attack")
    print(info["nom"], info["auditeurs"], info["ecoutes"])
    print(info["tags"][:3])
    print(info["mbid"])