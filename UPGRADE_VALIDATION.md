# Upgrade validation

12 JavaScript tests and 8 Python tests passed. The 12 include a 60-ray accelerated-versus-exhaustive intersection test and the existing science test module.

Browser check: default saved dataset loaded; planner found 44 eligible candidate starts of 163; the first is 2026-11-18 23:00 to 2026-11-19 05:00 UTC at the central site and 2 m height. The selected six-hour window passed the five-minute recheck (73 epochs). At hourly sampling, 1 m failed the 30-minute Earth-gap requirement (360 modeled blocked minutes); 2 m and 5 m passed. Changing the requested duration cleared the prior candidate and checks.

This result is sensitive to modeled height. Bilinear observer elevation and triangulated terrain, downsampling, and missing small obstacles limit its physical interpretation. No independent high-resolution illumination benchmark, global terrain validation, radio-link analysis or power analysis has been completed.

Reproduce stored scenarios: `node tools/check_decisions.mjs`. Read docs/METHODOLOGY.md and docs/DATA_SOURCES.md before making scientific claims.

Implementation: Python standard library HTTP backend and NASA query proxy, JavaScript modules, Web Workers, Three.js with Canvas fallback, NASA LOLA-derived grids and JPL Horizons. AI-assisted implementation and debugging; no trained ML prediction model is included.
