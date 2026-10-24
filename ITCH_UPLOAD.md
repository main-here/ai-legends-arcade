# Subir AI LEGENDS ARCADE a itch.io — checklist

Archivos listos en `dist/`:
- `ai-legends-arcade-itch.zip` — juego HTML5 (`index.html` en la raíz del zip, rutas relativas, ~2.3 MB, 233 archivos)
- `cover_630x500.png` — imagen de portada

(Si `dist/` no existe o cambiaste algo: `sh tools/package.sh` y `uv run --with pillow --with numpy --with scipy python tools/make_cover.py`.)

## 1. Crear el proyecto (Dashboard → Create new project)
- **Title:** AI LEGENDS ARCADE
- **Project URL:** `ai-legends-arcade` (queda `https://<usuario>.itch.io/ai-legends-arcade`)
- **Short description / tagline:** Pick a legend of science, philosophy or AI and win a 16-bit debate. FACT, LOGIC or QUOTE?
- **Classification:** Games · **Kind of project:** HTML
- **Release status:** Released · **Pricing:** No payments (free)

## 2. Uploads
- Subir `dist/ai-legends-arcade-itch.zip` y marcar **This file will be played in the browser**.

## 3. Embed options
- **Viewport dimensions:** 540 × 960 (vertical 9:16)
- ✅ **Mobile friendly** → Orientation: **Portrait**
- ✅ **Fullscreen button**
- ⬜ Automatically start on page load (dejar desmarcado: el juego ya tiene pantalla de título)
- ⬜ Enable scrollbars (desmarcado)

## 4. Details
- **Description (sugerida):**
  > INSERT COIN. Pick one of 76 fighters — science & philosophy LEGENDS, today's AI figures as pixel caricatures and mascots, and
  > invented ARCHETYPES — and out-argue the CPU in a 16-bit arcade debate. Pick FACT, LOGIC or QUOTE: FACT beats
  > QUOTE, QUOTE beats LOGIC, LOGIC beats FACT. Win exchanges to fill your SUPER bar, then MIC DROP your fighter's
  > most famous line. Real figures argue with real quotes and facts, sources included. Chiptune soundtrack (toggle it with ♪). 60 seconds, one thumb.
  > Follow @ai.legends.arcade on Instagram for new fights.
- **Genre:** Fighting
- **Tags:** `pixel-art`, `fighting`, `arcade`, `retro`, `16-bit`, `artificial-intelligence`, `philosophy`, `science`, `parody`, `mobile` (itch admite hasta 10)
- **Cover image:** `dist/cover_630x500.png`
- **Screenshots (opcional):** capturas del juego en el móvil (título, selección, pelea con frase, K.O.)
- **Links:** Instagram `https://www.instagram.com/ai.legends.arcade/`
- **Visibility:** primero *Draft* para probarlo; luego *Public*.

## 5. Después de publicar
1. Abrir la página desde el navegador in-app de Instagram (móvil) y jugar una ronda.
2. Poner la URL de itch en `const GAME_URL = ''` de `index.html` (sección "Public page to share"), volver a
   ejecutar `sh tools/package.sh` y subir el zip nuevo (sustituyendo el anterior). Así el botón SHARE comparte
   siempre la página de itch. Sin esto, el juego intenta usar la página de itch que lo contiene y, si no puede,
   comparte la URL interna del iframe.
3. Poner el link en la bio de @ai.legends.arcade.
