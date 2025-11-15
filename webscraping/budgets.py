#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scrape_presupuestos.py
Scrapea la página indicada y genera presupuestos_2024_25.csv con columnas:
club,budget,expenses
Budget/expenses -> número (millones €). Si en la fuente aparece un rango (p.ej. 450-460 M€),
se usa el promedio.
"""

import requests
from bs4 import BeautifulSoup
import re
import csv
import statistics
import sys

URL = "https://cronicaglobal.elespanol.com/culemania/palco/20250213/todos-los-presupuestos-de-liga-primera-division/923657741_0.html"
OUT_CSV = "presupuestos_2024_25.csv"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; budget-scraper/1.0)"}

number_pattern = re.compile(r'([0-9\.\,]+(?:-[0-9\.\,]+)?)\s*M\s*€', re.IGNORECASE)

def parse_number_token(token: str) -> float:
    """
    Convierte un token como '1.128', '58,7', '450-460' en un float.
    - Si hay '-', se calcula el promedio de los extremos.
    - Interpreta '.' como separador de miles y ',' como decimal (estilo español).
    """
    token = token.strip().replace(' ', '')
    if '-' in token:
        parts = token.split('-')
        vals = [parse_number_token_single(p) for p in parts if p.strip()]
        if not vals:
            raise ValueError(f"No se pudo parsear rango: {token}")
        return float(sum(vals) / len(vals))
    else:
        return float(parse_number_token_single(token))

def parse_number_token_single(s: str) -> float:
    # eliminar puntos usados como miles y cambiar coma decimal a punto
    s = s.strip()
    s = s.replace('.', '')     # 1.128 -> 1128
    s = s.replace(',', '.')    # 58,7 -> 58.7
    try:
        return float(s)
    except Exception as e:
        raise ValueError(f"Error parseando número '{s}': {e}")

def parse_from_table(soup):
    """
    Si existe una <table> con filas de club/budget/expenses, parsea esa tabla.
    Devuelve lista de tuplas (club, budget_float, expenses_float).
    """
    results = []
    table = soup.find('table')
    if not table:
        return results
    # intentar leer filas
    for tr in table.find_all('tr'):
        cols = [c.get_text(" ", strip=True) for c in tr.find_all(['td','th'])]
        if len(cols) < 3:
            continue
        # buscar dos tokens numéricos en la fila (presupuesto ingresos, gastos)
        row_text = " ".join(cols)
        matches = number_pattern.findall(row_text)
        if len(matches) >= 2:
            # club: todo hasta la primera aparición del primer número
            first_match = number_pattern.search(row_text)
            club = row_text[:first_match.start()].strip()
            budget_token = matches[0]
            expenses_token = matches[1]
            try:
                budget_val = parse_number_token(budget_token)
                expenses_val = parse_number_token(expenses_token)
            except Exception:
                continue
            results.append((club, budget_val, expenses_val))
    return results

def parse_from_text(soup):
    """
    Extrae el texto del artículo y busca el bloque que contiene la tabla textual,
    luego parsea cada línea buscando dos tokens numéricos con 'M€'
    """
    text = soup.get_text("\n")
    # localizar el comienzo de la lista/tabulación
    candidates = [
        "CLUB PRESUPUESTO DE INGRESOS PRESUPUESTO DE GASTOS",
        "CLUB PRESUPUESTO DE INGRESOS",
        "CLUB PRESUPUESTO",
        "PRESUPUESTO DE INGRESOS PRESUPUESTO DE GASTOS",
        "PRESUPUESTO DE INGRESOS"
    ]
    start = None
    for c in candidates:
        idx = text.find(c)
        if idx != -1:
            start = idx
            break
    if start is None:
        # si no encuentra, empezar desde el final del texto (fallback)
        start = 0

    # intentar cortar hasta la sección que sigue (p.ej. 'Más en Palco' o hasta 6000 chars)
    end_marker = "Más en Palco"
    end = text.find(end_marker, start)
    if end == -1:
        end = start + 6000 if start + 6000 < len(text) else len(text)

    block = text[start:end]
    lines = [l.strip() for l in block.splitlines() if l.strip()]
    results = []
    for line in lines:
        # solo tratamos líneas que contengan 'M€' o 'M €'
        if 'M€' not in line and 'M €' not in line and 'M' not in line:
            continue
        matches = list(number_pattern.finditer(line))
        if len(matches) >= 2:
            first = matches[0]
            second = matches[1]
            club = line[: first.start() ].strip()
            budget_token = first.group(1)
            expenses_token = second.group(1)
            # si club está vacío, quizá la línea es algo raro; intentar extraer de tokens previos:
            if not club:
                # fallback: intentar columnas por espacios
                parts = re.split(r'\s{2,}', line)
                club = parts[0].strip() if parts else line
            try:
                budget_val = parse_number_token(budget_token)
                expenses_val = parse_number_token(expenses_token)
                results.append((club, budget_val, expenses_val))
            except Exception:
                # ignorar fila si no se puede parsear
                continue
    return results

def main():
    try:
        r = requests.get(URL, headers=HEADERS, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print("Error descargando la página:", e, file=sys.stderr)
        return

    soup = BeautifulSoup(r.content, "html.parser")

    # 1) intentar parsear tabla HTML si existe
    results = parse_from_table(soup)

    # 2) si no salió nada, parsear desde texto
    if not results:
        results = parse_from_text(soup)

    # Si aún nada, abortar con mensaje
    if not results:
        print("No se han encontrado filas válidas para club/budget/expenses en la página.", file=sys.stderr)
        return

    # Guardar CSV
    with open(OUT_CSV, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["club", "budget", "expenses"])
        for club, budget, expenses in results:
            # Escribir números con punto decimal (millones €)
            writer.writerow([club, f"{budget:.3f}".rstrip('0').rstrip('.'), f"{expenses:.3f}".rstrip('0').rstrip('.')])

    print(f"He escrito {len(results)} filas en '{OUT_CSV}'")

if __name__ == "__main__":
    main()
