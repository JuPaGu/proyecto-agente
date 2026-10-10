import re
import time
import unicodedata
from pathlib import Path

import requests

API = "https://es.wikipedia.org/w/api.php"
# Wikipedia pide identificarse en el User-Agent. Pon tu correo real.
HEADERS = {"User-Agent": "proyecto-agente-universidad/0.1 (estudiante; contacto: tu@correo.com)"}
OUT = Path(__file__).resolve().parent.parent / "corpus"
OUT.mkdir(exist_ok=True)

TITULOS = [
    # Sistema solar y planetas
    "Sistema Solar", "Sol", "Mercurio (planeta)", "Venus (planeta)", "Tierra",
    "Luna", "Marte (planeta)", "Júpiter (planeta)", "Saturno (planeta)",
    "Urano (planeta)", "Neptuno (planeta)", "Plutón (planeta enano)", "Cinturón de asteroides",
    "Cinturón de Kuiper",
    # Objetos celestes
    "Agujero negro", "Estrella", "Galaxia", "Vía Láctea", "Nebulosa", "Supernova",
    "Estrella de neutrones", "Enana blanca", "Cometa", "Asteroide", "Exoplaneta",
    "Púlsar", "Cuásar",
    # Misiones y telescopios
    "Programa Apolo", "Apolo 11", "Sputnik 1", "Voyager 1", "Voyager 2",
    "Estación Espacial Internacional", "Telescopio espacial Hubble",
    "Telescopio espacial James Webb",
    # Teorías y conceptos
    "Big Bang", "Materia oscura", "Energía oscura", "Relatividad general",
    "Expansión del universo", "Inflación cósmica", "Ondas gravitacionales",
    "Paradoja de Fermi", "Ecuación de Drake", "Universo observable",
    # Historia y protagonistas
    "Carrera espacial", "NASA", "Agencia Espacial Europea", "Yuri Gagarin",
    "Neil Armstrong",
]


def descargar(titulo):
    params = {
        "action": "query", "format": "json", "prop": "extracts|info",
        "explaintext": 1, "exsectionformat": "plain", "redirects": 1,
        "inprop": "url", "titles": titulo,
    }
    r = requests.get(API, params=params, headers=HEADERS, timeout=30)
    r.raise_for_status()
    page = next(iter(r.json()["query"]["pages"].values()))
    if "missing" in page or not page.get("extract"):
        return None
    return page["title"], page["fullurl"], page["extract"]


def nombre_archivo(titulo):
    sin_tildes = unicodedata.normalize("NFKD", titulo).encode("ascii","ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", sin_tildes.lower()).strip("_") + ".txt"


def main():
    fallidos = []
    for titulo in TITULOS:
        try:
            resultado = descargar(titulo)
        except requests.RequestException as e:
            print(f"ERROR de red en {titulo!r}: {e}")
            fallidos.append(titulo)
            continue
        if resultado is None:
            print(f"NO ENCONTRADO: {titulo!r}")
            fallidos.append(titulo)
            continue
        titulo_real, url, texto = resultado
        contenido = (
            f"TÍTULO: {titulo_real}\nFUENTE: {url}\n"
            f"LICENCIA: CC BY-SA 4.0 (Wikipedia)\n\n{texto}"
        )
        (OUT / nombre_archivo(titulo_real)).write_text(contenido, encoding="utf-8")
        print(f"OK ({len(texto):>6} caracteres): {titulo_real}")
        time.sleep(0.5)  # cortesía con el servidor

    print(f"\nDescargados: {len(TITULOS) - len(fallidos)} de {len(TITULOS)}")
    if fallidos:
        print("Fallidos:", fallidos)


if __name__ == "__main__":
    main()