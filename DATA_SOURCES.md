# Data sources, attribution and challenge mapping

## Challenge
Official challenge: https://www.spaceappschallenge.org/2026/challenges/lunar-landing-site-navigator/?tab=resources

The indexed official description asks for an intuitive tool for comparing lunar south-pole sites and dates and visualizing Sun and Earth relative to the horizon for solar-access and direct-to-Earth visibility assessment.

**Verification note (2026-11-14):** direct retrieval of the official resources tab returned HTTP 503/502. We do not claim to have verified its entire current resource list. An indexed mirror lists QuickMap, Moon Trek, Horizons System, and CSA Moon Exploration. Each numerical dataset actually used below was checked against its primary provider; the mirrored list was not used as scientific data.

## Numerical data actually used
| Purpose | Primary source | Bundled files / use |
|---|---|---|
| Date-specific lunar Sun/Earth geometry | NASA/JPL Horizons API https://ssd-api.jpl.nasa.gov/doc/horizons.html | Backend requests + real saved example |
| Full-Moon shape | NASA LRO LOLA PDS archive https://imbrium.mit.edu/DATA/LOLA_GDR/CYLINDRICAL/IMG/ | Raw LDEM_4.IMG and its authoritative LBL; prepared globe-dem.json |
| Local south-pole elevation | NASA Goddard PGDA https://pgda.gsfc.nasa.gov/products/78 | Site01_final_adj_5mpp_surf.tif resampled into mission-terrain.json |
| Regional context | NASA Goddard PGDA https://pgda.gsfc.nasa.gov/products/90 | LDEM_80S_80MPP_ADJ.TIF subset into regional-terrain.json |

## Why this fits the resource tools
- **Horizons** is the computation source, not a decorative reference.
- **Moon Trek** (https://trek.nasa.gov/moon/) and **LROC QuickMap** (https://quickmap.lroc.asu.edu/) provide exploration/access context for LRO terrain products. We use the actual underlying LOLA numerical products directly; neither external website is embedded or required at runtime.
- CSA Moon Exploration is context only and is not claimed as a numerical feed.

## Global LOLA details
The PDS label identifies the dataset as `LRO-L-LOLA-4-GDR-V1.0`, product `LDEM_4`, MEAN EARTH/POLAR AXIS OF DE421 frame, positive east longitude, 1440 columns × 720 rows, 0..360° E, +90..−90° latitude. Values are little-endian signed 16-bit integers; elevation = DN × 0.5 m. Reference radius is 1,737,400 m. Source observation span and creation dates are retained in `data/LDEM_4.LBL`.

Preparation rotates columns by 180° to use −180..180° and averages 4×4 blocks into 1° globe samples. Actual global geometry uses radius plus elevation, with **no vertical exaggeration**. The locally generated relief JPEG comes only from gradients and heights in the original LOLA grid. It is an illustrative topographic shading, **not** optical albedo, AI imagery, or an independent dataset. The global mesh is for context, not local horizon decisions.

## Polar grids
Local: 16 km tile, 5 m source pixel spacing, bilinear resampling to 320×320 / 50 m. Regional: 320 km subset, 80 m source spacing, bilinear resampling to 320×320 / 1 km. Both are south-polar stereographic, lunar sphere 1,737,400 m and MOON_ME / DE421. Sampling spacing must not be confused with vertical or horizontal measurement accuracy.

## Horizons example and live requests
Bundled example is an actual JPL response fetched 2026-11-14. Central point: −89.46316°, −137.48955° E; altitude is DEM ground + 2 m. Window: 2026-11-14 00:00 to 2026-11-21 00:00 UTC, hourly. JSON includes query URLs, fetch timestamp, service signature and every returned target sample. No simulated ephemeris is substituted for failed API requests.

New requests use Sun 10, Earth 399, center coord@301, geodetic coordinates, quantities 4/13/20, airless apparent coordinates and UTC. Target angular diameters and ranges are preserved for provenance; current classification tests centers, not disk edges.

## Third-party software
Three.js 0.160.0 is vendored in `frontend/assets/three.module.js`, MIT license in `docs/THREE-LICENSE.txt`. No runtime CDN calls. Python runtime uses only its standard library. Optional data preparation scripts use NumPy/rasterio/Pillow. Code and design were developed with ChatGPT assistance, disclosed for competition references.

NASA/JPL and LRO provider attribution is retained. NASA names identify data sources; there is no claim of NASA sponsorship or endorsement. Application MIT licensing does not relicense NASA data or third-party software.
