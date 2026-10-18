from pathlib import Path
import requests
import gzip
import json

# Etape 1 : création path et fichier réception données

folder = Path("data/")
folder.mkdir(exist_ok=True)
file = folder / "structure.json"

# Etape 2 récupération données URL

url = "https://www.data.gouv.fr/api/1/datasets/finess-structures-1"

response = requests.get(url)
response.raise_for_status()

# print(response.content)

data = response.json()

# print(data.keys()) --> resources, created_at, geopf etc a lot of metadata
# print(type(data)) --> dict

# Etape 3 : récupération 2ème url contenant les données brutes

for resource in data["resources"] : 
    if "journalier" in resource["url"] : 
        url_inside = resource["url"]
        # on ne télécharge pas encore le fichier ! Donc on peut pas gzip là, il faut TELECHARGER LE FICHIER donc : re request.get
        print(f"Url journalier : {url}")

# Etape 4 : téléchargement fichier .json.gz

response_ui = requests.get(url_inside)
response_ui.raise_for_status()

# Etape 5 : sauvegarde fichier compréssé 

with open(file, "wb") as f :
    # on peut pas print le response_ui.content car content = bytes et on peut pas .json() car c'est un fichier compréssé
    # wb donc car content = bytes
    f.write(response_ui.content)

# Etape 6 : décompression + lecture fichier

with gzip.open(file, "rt", encoding="utf-8") as f : 
    # r = rt, c'est le mode par défaut et tu veux le lire en text
    # de 2 tu veux le lire en text pas en binaire
    content = f.read(100)
    f.seek(0)
    data = json.load(f) 

"""
Autre information : 
- si lors du with gzip.open on fait : content = f.read(100) avant le data = json.load(f) 
on va prendre les 100 premiers charactères et le load commencera au 101 ième
f.seek(0) fait un retour au début du fichier
"""
