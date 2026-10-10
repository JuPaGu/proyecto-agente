import sys

import requests

API = "https://es.wikipedia.org/w/api.php"
HEADERS = {"User-Agent": "proyecto-agente-universidad/0.1 (estudiante; contacto: tu@correo.com)"}

consulta = " ".join(sys.argv[1:])
params = {"action": "opensearch", "format": "json", "search": consulta, "limit": 8}
r = requests.get(API, params=params, headers=HEADERS, timeout=30)
r.raise_for_status()
for titulo in r.json()[1]:
    print(titulo)