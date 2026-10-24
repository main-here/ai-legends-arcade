# AI LEGENDS ARCADE — juego para el link de la bio

Juego web de una sola página (sin build): `index.html` + `assets/` (≈2.5 MB en total, pero el móvil solo descarga
~150 KB al abrir: retratos con lazy-load y los 2 sprites de cada pelea).

Flujo: título (INSERT COIN) → SELECT YOUR LEGEND (LEGENDS / NOW / ARCHETYPES, 76 personajes) → VS →
DEBATE contra la CPU: FACT / LOGIC / QUOTE a piedra-papel-tijera (FACT gana a QUOTE, QUOTE a LOGIC, LOGIC a FACT;
empate = daño leve a los dos), barra SUPER → MIC DROP con la frase más famosa, 99 de tiempo, rachas
→ K.O. / DOUBLE K.O. "Who won the debate?" → Compartir + Follow @ai.legends.arcade.

Las líneas de debate (FACT, LOGIC, QUOTE, MIC DROP con su fuente) están en `tools/debate.json`. Personas reales:
solo frases reales ya usadas en los episodios o datos verificables en tercera persona; arquetipos y Rocket
Billionaire, texto inventado. Tras editarlo: `uv run --with pillow --with numpy --with scipy python tools/build_assets.py --data-only`.

## Probar en local

```bash
python3 -m http.server 8765
```

Abrir http://127.0.0.1:8765 (con las herramientas de desarrollador en modo móvil).

## Regenerar los sprites (si cambian las hojas de personajes)

```bash
uv run --with pillow --with numpy --with scipy python tools/build_assets.py
```

Lee `Legends/_produccion/personajes/personajes.json`, las hojas `pixel/<key>.png` y los retratos `port/<key>.png`,
y las frases de `Legends/_produccion/S1|S2/episodes_*.json`. Escribe `assets/sp/*.webp` y `assets/data.js`.
Se puede pasar una lista de keys para regenerar solo esos personajes.

Notas de contenido:
- `musk` no tiene hoja (bloqueado) → no aparece. "The Rocket Billionaire" es la parodia con mosaico; no tiene frases
  reales, así que usa dos líneas inventadas de parodia (en `tools/build_assets.py`).
- Algunas frases de las hojas vienen partidas (p. ej. Lovelace empieza en minúscula); el juego les pone "…" delante.

## Publicación: itch.io

Decisión: se publica en itch.io como juego HTML5 (embed vertical 540×960 + botón de pantalla completa).

```bash
sh tools/package.sh
```

Genera `dist/ai-legends-arcade-itch.zip` (`index.html` + `assets/`, sin `tools/` ni docs).
`tools/make_cover.py` genera `dist/cover_630x500.png`. Pasos de subida: [ITCH_UPLOAD.md](ITCH_UPLOAD.md).

Dentro del iframe de itch: no navega la ventana principal (Instagram abre en pestaña nueva), SHARE usa el menú
de compartir del móvil y, si no, copia el link. Para que comparta la página de itch, rellenar `GAME_URL` en
`index.html` tras crear la página.

## Estructura

```
index.html            juego (HTML/CSS/JS en un solo archivo)
assets/data.js        roster (nombre, grupo, movimientos, frases) generado
assets/sp/*.webp      retrato (_p), idle (_i) y especial (_s) de cada personaje
assets/PixelifySans.ttf
tools/                scripts de assets, portada y empaquetado (requieren uv)
dist/                 salida para itch.io (ignorada por git)
```
