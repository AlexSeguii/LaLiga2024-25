# 📊 LaLiga 2024-25 — Análisis de jugadores y clubes


**Resumen:** Proyecto personal de análisis de la temporada **LaLiga 2024-25**. Contiene el pipeline de limpieza y modelado (Jupyter + PySpark), integración de estadísticas de jugadores/partidos, tablas limpias exportadas para visualización y dashboards interactivos en **Power BI**. Incluye exploración en **Databricks** para ver el flujo cloud/Spark.

---

## 📚 Índice
- [Descripción del proyecto](#descripción-del-proyecto)  
- [Estructura del repositorio](#estructura-del-repositorio)  
- [Tecnologías y librerías](#tecnologías-y-librerías)  
- [Requisitos e instalación rápida](#requisitos-e-instalación-rápida)  
- [Notebooks y scripts (orden de ejecución)](#notebooks-y-scripts-orden-de-ejecución)  
- [Fragmentos clave (ejemplos de código)](#fragmentos-clave-ejemplos-de-código)  
- [Power BI — Visuales y medidas DAX recomendadas](#power-bi---visuales-y-medidas-dax-recomendadas)  
- [Comprobaciones de calidad de datos (sanity checks)](#comprobaciones-de-calidad-de-datos-sanity-checks)  
- [Hallazgos principales / insights](#hallazgos-principales--insights)  
- [Mejoras futuras](#mejoras-futuras)  
- [Databricks (nota)](#databricks-nota)  
- [Contacto / Créditos](#contacto--créditos)

---

## Descripción del proyecto
Este proyecto procesa y analiza datos de la temporada **LaLiga 2024-25**: jugadores, estadísticas por partido y clasificación.  
Objetivos principales:

- Normalizar y limpiar datos heterogéneos (CSV con inconsistencias comunes).  
- Integrar y enriquecer estadísticas (sobrescribir goles/asistencias con fuente fiable).  
- Generar datasets limpios listos para visualización en Power BI.  
- Construir dashboards interactivos (Jugadores y Clubs) con KPIs y visuales útiles para análisis táctico y económico.

Se exploró Databricks para entender el flujo cloud/Spark; la limpieza se ejecutó en Jupyter + PySpark en la VM y los CSV limpios se importaron a Power BI para diseño del dashboard.

---

## Estructura del repositorio
