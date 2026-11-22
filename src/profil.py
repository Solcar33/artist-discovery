import base64
import gzip
import json
import os
from pathlib import Path

from history import load_history, get_top_artists, get_known_artists

ENV_VAR = "SPOTIFY_PROFILE_B64"


def build_profile(nb_top=50):
    """Résume l'historique : les artistes les plus écoutés et tous les artistes connus."""
    ecoutes = load_history()
    return {
        "top": [[nom, nb] for nom, nb in get_top_artists(ecoutes, nb_top)],
        "connus": sorted(get_known_artists(ecoutes)),
    }


def encode_profile(profil):
    """Comp^resse et encore le profile en un texte ccourt (pour un secret GitHub)."""
    brut = json.dumps(profil, ensure_ascii=False).encode("utf-8")
    return base64.b64encode(gzip.compress(brut)).decode("ascii")


def decode_profile(texte):
    """Opération inverse de encode_profile."""
    brut = gzip.decompress(base64.b64decode(texte))
    return json.loads(brut.decode("utf-8"))


def get_profile():
    """Profil depuis le secret (cloud) s'il existe, sinon depuis l'historique local."""
    texte = os.getenv(ENV_VAR)
    if texte:
        return decode_profile(texte)
    return build_profile()


if __name__ == "__main__":
    texte = encode_profile(build_profile())
    chemin = Path("data") / "profile.b64"
    chemin.write_text(texte, encoding="ascii")
    print(f"Profil écrit dans {chemin} ({len(texte)} caractères, limite GitHub : 48000)")