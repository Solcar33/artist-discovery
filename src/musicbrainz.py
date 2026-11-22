import time

import requests

BASE_URL = "https://musicbrainz.org/ws/2/"
HEADERS = {"User-Agent": "artist-discovery/0.1 (projet d'apprentissage"}


def _appeler(chemin, **params):
    """Appelle l'API MusicBrainz et renvoie le JSON décodé."""
    params = {"fmt": "json", **params}
    attente = 2
    for tentative in range(5):
        reponse = requests.get(BASE_URL + chemin, params=params, headers=HEADERS, timeout=10)
        time.sleep(1)  # limite : 1 requête par seconde
        if reponse.status_code != 503:
            break
        time.sleep(attente)  # serveur surchargé : on patiente de plus en plus
        attente *= 2
    if reponse.status_code != 200:
        raise RuntimeError(
            f"MusicBrainz a répondu avec le code {reponse.status_code} : {reponse.text[:200]}"
        )
    return reponse.json()


def find_artist(nom):
    """Cherche un artiste par son nom. Renvoie le meillleur résultat, ou None."""
    data = _appeler("artist", query=f'artist:"{nom}"', limit=1)
    if not data["artists"]:
        return None
    return data["artists"][0]

def get_artist_links(mbid):
    """Renvoie les liens d'un artiste, regroupés par type (site officiel, réseaux...)"""
    data = _appeler(f"artist/{mbid}", inc="url-rels")
    liens = {}
    for relation in data.get("relations", []):
        if "url" in relation:
            liens.setdefault(relation["type"], []).append(relation["url"]["resource"])
    return liens


if __name__ == "__main__":
    artiste = find_artist("Althea & Donna")
    print (artiste["name"], artiste["score"], artiste["id"])
    for type_lien, urls in get_artist_links(artiste["id"]).items():
        print(type_lien, urls)
