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
## Tecnologías y librerías
**Lenguajes / Plataformas**
- Python (Jupyter Notebook)  
- PySpark / Apache Spark  
- Power BI Desktop  
- Databricks (exploración / notebooks cloud)

**Librerías Python**
- `pandas`, `numpy`, `pyspark`, `matplotlib`, `python-dateutil`, `BeautifulSoup`, `Selenium`

**Otras**
- SQL (Spark SQL)  
- DAX (Power BI measures)

---

**Hallazgos principales / insights**

### 1) Impacto de los máximos goleadores sobre la posición del equipo
- **Jugadores estrella (p. ej. Mbappé, Lewandowski, Budimir, etc.)** han marcado diferencias claras en la tabla: muchos de los máximos artilleros se encuentran en equipos con aspiraciones altas o que finalmente han quedado arriba en la clasificación. Su capacidad para convertir ocasiones se traduce de forma directa en puntos y en la diferencia de goles del club, lo que explica por qué los equipos con los goleadores top suelen ocupar posiciones de privilegio.
- **Goleadores en equipos de media o baja tabla:** el dashboard muestra también varios goleadores importantes que juegan en clubes de media tabla. En esos casos su aportación (goles y, a veces, asistencias) aparece decisiva para que el equipo *no* acabe entre los últimos tres: estos jugadores han proporcionado goles que han permitido ganar partidos clave o empatar encuentros donde el equipo hubiera perdido. En términos prácticos, su rendimiento individual ha sido clave para la permanencia o para superar expectativas.
- **Dependencia vs reparto:** hay clubes cuya producción de goles depende de uno o dos delanteros (alto % de goles del equipo concentrado en top-2/3), lo que implica riesgo competitivo si esos jugadores se lesionan o bajan el rendimiento. Otros clubes muestran una distribución más equilibrada, con más jugadores aportando goles, lo que les proporciona resiliencia.

---

### 2) Rol de los asistentes y su efecto en los resultados del club
- **Lamine Yamal y Raphinha como creadores destacados:** según los top de asistencias del dashboard, algunos nombres (como Lamine Yamal) asumen una función creativa muy relevante. Cuando un equipo incorpora un asistente de alto volumen, el beneficio no es solo estadístico: aumenta la probabilidad de que varios jugadores anotadores mejoren sus cifras. En equipos jóvenes (ej.: clubes con menor edad media), la presencia de un creador top ayuda a convertir el caudal ofensivo en goles efectivos.
- **Distribución de la creatividad:** a diferencia de los goles, las asistencias aparecen más repartidas en la liga. Esto reduce la dependencia de un single playmaker en la mayoría de clubes, aunque en algunos equipos sí existe un jugador con aportación notable que actúa como eje creativo.

---

### 3) Presupuesto → influencia (correlación y excepciones)
- **Concentración de budget:** los gráficos de presupuesto muestran que una fracción pequeña de clubes acapara una porción relevante del presupuesto total (los “top spenders”). Estos clubes, en general, aparecen en la parte alta de la clasificación, lo cual confirma la relación esperada entre inversión y rendimiento.
- **Efecto presupuesto ≠ garantía:** el dashboard evidencia también casos donde **alto presupuesto no se traduce en rendimiento acorde** (algunos clubes con gasto/budget elevado no terminan tan arriba como su capacidad financiera podría sugerir). Esto apunta a problemas de eficiencia (mala planificación deportiva, fichajes inefectivos, o desequilibrio entre plantilla y estructura).
- **Sorpresas positivas:** asimismo, hay equipos con presupuestos modestos que superan expectativas y terminan en puestos relativamente altos. Estos casos son ejemplos de **alto ROI deportivo** (mejor aprovechamiento de recursos, scouting eficaz, o modelo táctico eficiente).

---

### 4) Casos destacados / outliers (qué observar en detalle)
- **Club grande + buen presupuesto + buen puesto:** confirma el modelo tradicional (inversión → plantilla competitiva → resultados).  
- **Club grande + alto presupuesto + bajo puesto:** es un caso de estudio para analizar decisiones deportivas (fichajes, rotaciones, lesiones, dirección técnica). Identificar estos clubes ayuda a plantear recomendaciones operativas.  
- **Club pequeño + bajo presupuesto + alto puesto:** ejemplo de eficacia en scouting y estructura; son candidatos a replicar prácticas (mejor gestión de recursos, apuesta por cantera o inteligencia analítica).  
- **Goleadores en equipos en descenso o casi descenso:** su actuación suele reflejar que, pese a cifras personales atractivas, el problema del club era estructural (defensa débil, pocos creadores, o resultados malos en casa/visitante), y un goleador por sí solo no basta para evitar el descenso sin apoyo colectivo.

---

### 5) Relación jugador-equipo: ¿ayudaron a lograr los objetivos?
- **Para los clubes en las primeras posiciones:** los máximos goleadores y máximos asistentes han sido piezas esenciales; sus goles/ases contribuyeron a ganar partidos clave frente a rivales directos y a mantener diferencia de goles favorable. El dashboard muestra una alineación clara entre la presencia de top scorers/creators y la plaza final en muchos casos.
- **Para equipos en mitad de tabla:** la contribución de un goleador «local» o un asistente regular ha permitido consolidar la permanencia y, en ocasiones, aspirar a plazas europeas. La combinación goles + asistencias por parte de un pequeño núcleo de jugadores ha sido determinante.
- **Para equipos abajo/descenso:** cuando hay goleadores destacados pero el equipo sigue abajo, los datos sugieren que la carga del éxito recae en un individuo sin suficiente soporte colectivo (defensa débil, pocas asistencias de apoyo, baja profundidad de plantilla). En estos casos la recomendación operativa es equilibrar fichajes defensivos y reforzar la creación de juego.

---

### 6) Implicaciones tácticas y operativas (qué debería hacer cada tipo de club)
- **Clubes con top-scorer dominante:** diversificar la fuente de goles (fichaje de segundo delantero, trabajar finalización de mediapunta) para reducir riesgo por dependencia.  
- **Clubes con buen creador pero pocos rematadores:** potenciar la llegada de rematadores y la definición en el área; preparar jugadas que maximicen las asistencias del creador estrella.  
- **Clubes con alto presupuesto y bajo rendimiento:** auditoría deportiva (evaluar estructura de fichajes, cuerpo técnico, KPI de scouting). Posible reorientación del gasto hacia áreas con mayor impacto (cantera, analytics).  
- **Clubes de bajo presupuesto con buen rendimiento:** documentar y replicar procesos (scouting, entrenamiento, retención de talento), potenciar marketing y sostenibilidad financiera para mantener competitividad.

---

- Campeón: Barcelona (plantilla joven y gran rendimiento ofensivo).
- Máximo goleador: Kylian Mbappé (31 goles), jugador de talla mundial muy decisivo pero no fue suficiente para que su equipo ganara la liga.
- Máximo asistente: Lamine Yamal (13 asistencias) jugador clave ofensivamente.
- Asistencias más repartidas que goles: dependencia de pocos goleadores, creación más distribuida.
- Matriz 1-X-2 y heatmap de rivales revelan matchups críticos y ventajas como local.

---

> **Resumen final:** el dashboard muestra que los grandes goleadores y creadores tienen un papel decisivo en el rendimiento de sus clubes; el presupuesto facilita competir arriba, pero no garantiza el éxito si no existe eficiencia deportiva. Hay casos de alto presupuesto con rendimiento por debajo de lo esperado y casos de bajo presupuesto con rendimiento superior, lo cual ofrece oportunidades claras para recomendaciones tácticas y de gestión deportiva.

-
