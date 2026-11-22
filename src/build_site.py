import json
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

CONTENT_DIR = Path("content")
TEMPLATES_DIR = Path("templates")
SITE_DIR = Path("docs")
STATIC_DIR = Path("static")

env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(["html"]),
)


def load_semaines():
    """Charge toutes les semaines, de la plus récente à la plus ancienne."""
    semaines = []
    for chemin in sorted(CONTENT_DIR.glob("*.json"), reverse=True):
        with open(chemin, encoding="utf-8") as f:
            data = json.load(f)
        if "decouvertes" not in data:  # ancien format : une seule fiche
            data = {"date": data.get("date", ""), "decouvertes": [data]}
        data["slug"] = chemin.stem
        semaines.append(data)
    return semaines


def build_semaine_page(semaine):
    """Génère la page d'une semaine et renvoie son chemin."""
    page = env.get_template("semaine.html").render(semaine=semaine)
    sortie = SITE_DIR / "semaines" / f"{semaine['slug']}.html"
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(page, encoding="utf-8")
    return sortie


def build_index(semaines):
    """Génère la page d'accueil qui liste toutes les semaines."""
    page = env.get_template("index.html").render(semaines=semaines)
    sortie = SITE_DIR / "index.html"
    sortie.write_text(page, encoding="utf-8")
    return sortie


def copy_static():
    """Copie les fichiers statiques (CSS...) dans le dossier du site."""
    SITE_DIR.mkdir(exist_ok=True)
    for fichier in STATIC_DIR.glob("*"):
        shutil.copy(fichier, SITE_DIR / fichier.name)


if __name__ == "__main__":
    copy_static()
    semaines = load_semaines()
    for semaine in semaines:
        print("Page générée :", build_semaine_page(semaine))
    print("Accueil généré :", build_index(semaines))
