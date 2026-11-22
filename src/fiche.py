import json
from datetime import date
from pathlib import Path

import requests

from lastfm import get_artist_info
from musicbrainz import find_artist, get_artist_links
from recommand import get_candidates, pick_artist_of_the_week
from wikipedia import get_wikipedia_summary

CONTENT_DIR = Path("content")


def _essayer(source, fonction, *args):
    """Appelle 'fonction'. Si la source est en panne, renvoie None au lieu de planter."""
    try:
        return fonction(*args)
    except RuntimeError as erreur:  # nos propres messages : sans clés
        print(f"{source} indisponible : {erreur}")
    except requests.RequestException as erreur:
        # on affiche que le type : le détail contient l'URL, donc la clé Last.fm
        print(f"{source} indisponible : {type(erreur).__name__}")
    return None


def build_fiche(nom, favoris):
    """Assemble la fiche d'un artiste à partir de toutes les sources."""
    fiche = {"nom": nom, "favoris": favoris, "date": date.today().isoformat()}

    info = _essayer("Last.fm", get_artist_info, nom)
    fiche["lastfm"] = info

    mbid = info["mbid"] if info else ""
    if not mbid:
        trouve = _essayer("MusicBrainz (recherche)", find_artist, nom)
        if trouve and trouve["score"] >= 90:
            mbid = trouve["id"]

    liens = (
        _essayer("MusicBrainz (liens)", get_artist_links, mbid)
        if mbid
        else None
    )
    fiche["liens"] = liens or {}

    fiche["wikipedia"] = None
    if fiche["liens"].get("wikidata"):
        qid = fiche["liens"]["wikidata"][0].rsplit("/", 1)[-1]
        resume = _essayer("Wikipedia", get_wikipedia_summary, qid)
        if resume:
            texte, url, langue = resume
            fiche["wikipedia"] = {"texte": texte, "url": url, "langue": langue}
    return fiche


def save_fiche(fiche):
    """Enregistre la fiche dans content/ sous le nom AAAA-Wss.json."""
    CONTENT_DIR.mkdir(exist_ok=True)
    annee, semaine, _ = date.today().isocalendar()
    chemin = CONTENT_DIR / f"{annee}-W{semaine:02d}.json"
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(fiche, f, ensure_ascii=False, indent=2)
    return chemin


if __name__ == "__main__":
    candidats = get_candidates()
    nom, score, favoris = pick_artist_of_the_week(candidats)
    fiche = build_fiche(nom, favoris)
    print("Fiche enregistrée :", save_fiche(fiche))