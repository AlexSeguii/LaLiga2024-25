import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.transfermarkt.es/laliga/tabelle/wettbewerb/ES1/saison_id/2024"

# Obtener el HTML de la web
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}
response = requests.get(url, headers=headers)
html = response.text

# Parsear con BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Seleccionar la tabla
table = soup.find("table", class_="items")

# Lista para almacenar los datos
data = []

for row in table.tbody.find_all("tr"):
    cols = row.find_all("td")
    
    posicion = cols[0].text.strip().split()[0]
    club = cols[2].text.strip()
    partidos = cols[3].text.strip()
    ganados = cols[4].text.strip()
    empatados = cols[5].text.strip()
    perdidos = cols[6].text.strip()
    goles = cols[7].text.strip()
    diferencia = cols[8].text.strip()
    puntos = cols[9].text.strip()
    
    data.append([posicion, club, partidos, ganados, empatados, perdidos, goles, diferencia, puntos])

# Crear DataFrame
df = pd.DataFrame(data, columns=["Posición", "Club", "PJ", "G", "E", "P", "Goles", "+/-", "Puntos"])

# Guardar CSV
df.to_csv("laliga_clasificacion.csv", index=False, encoding="utf-8-sig")

print("CSV creado con éxito!")
