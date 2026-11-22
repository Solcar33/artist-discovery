import json
from collections import Counter
from pathlib import Path

DATA_DIR = Path("data/my_spotify_data/Spotify Account Data")
MIN_MS = 30_000


def load_history():
    """Charge toules les écoutes des fichiers StramingHistory_music_*.json."""
    ecoutes = []
    for fichier in sorted(DATA_DIR.glob("StreamingHistory_music_*.json")):
        with open(fichier, encoding="utf-8") as f:
            ecoutes.extend(json.load(f))
    if not ecoutes:
        raise RuntimeError(
            f"Aucun historique trouvé dans {DATA_DIR}. "
            "Dans le cloud, vérifie le secret SPOTIFY_PROFILE_B64."
        )
    return ecoutes


def get_top_artists(ecoutes, n=10):
    """Retourne les n artistes les plus écoutés (écoutes de 30s ou plus)."""
    valides = [e for e in ecoutes if e["msPlayed"] >= MIN_MS]
    compteur = Counter(e["artistName"] for e in valides)
    return compteur.most_common(n)


def get_known_artists(ecoutes):
    """Tous les artistes déjà écoutés, même brièvement : à ne pas recommander"""
    return {e["artistName"] for e in ecoutes}