import json
from pathlib import Path

DATA_DIR = Path("data/my_spotify_data/Spotify Account Data")
fichier = DATA_DIR / "StreamingHistory_music_0.json"

with open(fichier, encoding="utf-8") as f:
    historique = json.load(f)

print("Type :", type(historique))
print("Nombre d'écoutes :", len(historique))
print("Clés d'une écoute :", list(historique[0].keys()))