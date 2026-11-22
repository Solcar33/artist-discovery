import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

CONTENT_DIR = Path("content")
TEMPLATES_DIR = Path("templates")
SITE_DIR = Path("docs")

env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(["html"]),
)


def build_artist_page(chemin):
    """Génère la page HTML d'une fiche JSON et renvoie son chemin"""
    with open(chemin, encoding="utf-8") as f:
        fiche =json.load(f)
        page = env.get_template("artist.html").render(fiche=fiche)
        sortie = SITE_DIR / "semaine" / f"{chemin.stem}.html"
        sortie.parent.mkdir(parents=True, exist_ok=True)
        sortie.write_text(page, encoding="utf-8")
        return sortie


if __name__ == "__main__":
    for chemin in sorted(CONTENT_DIR.glob("*.json")):
        print("Page générée :", build_artist_page(chemin))
