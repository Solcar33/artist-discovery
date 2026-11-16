import json
from collections import Counter
from pathlib import Path

DATA_DIR = Path("Data/my_spotify_data/Spotify Account Data")
MIN_MS = 30_000 #seuil de 30s : en dessous, on considère que le titre est passé

ecoutes = []
for fichier in sorted(DATA_DIR.glob("StreamingHistory_music_*.json")):
    with open(fichier, encoding="utf-8") as f:
        ecoutes.extend(json.load(f))

print("Total d'écoutes :", len(ecoutes))

ecoutes_valides = [e for e in ecoutes if e["msPlayed"] >= MIN_MS]
print("Écoutes valides :", len(ecoutes_valides))

compteur = Counter(e["artistName"] for e in ecoutes_valides)
for artiste, nb in compteur.most_common(10):
    print(f"{nb:>5}  {artiste}")