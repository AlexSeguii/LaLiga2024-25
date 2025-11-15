from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time

driver = webdriver.Chrome()  # o Firefox, Edge según tengas
driver.get("https://www.torneodefutbol.es/porra-la-liga/2024-2025/estadisticas")

time.sleep(5)  # esperar que cargue JS y las tablas

# Goleadores
goals_table = driver.find_element(By.XPATH, '//h3[contains(text(),"Máximos goleadores")]/following-sibling::table')
rows = goals_table.find_elements(By.TAG_NAME, "tr")
goals_list = []
for row in rows[1:]:  # saltar encabezado
    cells = row.find_elements(By.TAG_NAME, "td")
    if len(cells) >= 3:
        name = cells[1].text
        goals = int(cells[2].text or 0)
        goals_list.append((name, goals))

# Asistencias
assists_table = driver.find_element(By.XPATH, '//h3[contains(text(),"Asistencias")]/following-sibling::table')
rows = assists_table.find_elements(By.TAG_NAME, "tr")
assists_list = []
for row in rows[1:]:
    cells = row.find_elements(By.TAG_NAME, "td")
    if len(cells) >= 3:
        name = cells[1].text
        assists = int(cells[2].text or 0)
        assists_list.append((name, assists))

# Merge
players = {}
for name, goals in goals_list:
    players[name] = {"name": name, "goals": goals, "assists": 0}
for name, assists in assists_list:
    if name in players:
        players[name]["assists"] = assists
    else:
        players[name] = {"name": name, "goals": 0, "assists": assists}

# Guardar CSV sin columna 'id'
with open("players_stats.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "goals", "assists"])
    writer.writeheader()
    for p in players.values():
        writer.writerow({"name": p["name"], "goals": p["goals"], "assists": p["assists"]})

driver.quit()
print("CSV generado correctamente sin la columna 'id'.")
