# Numerical method and limitations

1. Convert longitude/latitude to the south-polar map projection. Obtain observer ground elevation by bilinear interpolation of the local grid when available, otherwise the regional grid. Add the user-specified height above ground.
2. Query JPL Horizons for Sun and Earth apparent topocentric azimuth/elevation at that lunar location, including the total elevation in kilometers relative to the 1737.4 km sphere. Time labels are UTC. All geographic longitudes are east-positive, with negative values representing western longitudes.
3. For every DEM vertex, invert the south-polar projection, then compute the body-fixed Cartesian point with radius R + h. Project it into a common local east/north/up basis solely to improve numerical conditioning and renderability. This preserves lunar curvature.
4. Convert each target direction from the observer's ENU basis into the same Cartesian frame. Cast a ray from the observer and perform two-sided Möller–Trumbore intersections with the triangulated grids. A hierarchy of bounding boxes accelerates the search. The nearest positive intersection above 0.05 m is returned as a terrain obstruction.
5. The local tile provides detail; regional cells deep inside that tile are excluded from regional intersection to limit duplicated coarse terrain, with an overlap margin near the boundary. The local and regional grids may have interpolation differences. These are research approximations rather than certified terrain products.
6. Repeat for each epoch in a Web Worker. Green means no intersection found within modeled terrain with a positive reference-horizon elevation and complete grid validity; red means the center ray intersects terrain. Amber means unresolved (invalid coverage or a non-positive elevation with no hit). Clear sample percentages count samples, not continuously integrated durations. A joint clear run extends between its first and last adjacent clear samples; transitions between samples remain unresolved.

## Scope
- Finite regional footprint. Terrain outside it is not tested. No-hit is not a global proof of unobstructed geometry.
- Downsampled terrain. Local 50 m and regional 1 km spacing can hide smaller obstacles. Native pixel spacing is not height accuracy.
- Centers, not finite disks. Partial Sun/Earth visibility, penumbras and eclipses are not modeled.
- Direct-to-Earth geometry, not a link budget. Ground stations, Earth rotation relative to stations, antenna patterns, frequency, relay paths and atmospheric/weather effects are excluded.
- Solar access proxy, not electrical power. Panel orientation, conversion efficiency, temperature, storage and physical energy yield are excluded.
- Surface lighting and ray lengths are illustrative. Display ray lengths do not represent astronomical distances. Raw Horizons ranges are preserved in exported provenance.
- The global Moon is true-coordinate context; analysis uses the separate polar meshes. Globe relief colors are derived from elevation rather than optical reflectance.
- Display meshes are simplified further for rendering speed; the calculation uses the full prepared analysis grids.

## Validation performed
Coordinate projection round trips; analytical ray/triangle hit and miss; outward zenith versus downward rays; a real Sun center clear case and Earth blocked-to-clear change from the saved Horizons example; API parameter validation and real column order; anonymous HTTP access, module MIME types and data dimensions. These checks demonstrate implementation consistency, not validation for flight operations.

## Operation-window planner
Candidates start only at available sample timestamps. An interval receives a known state only if its endpoints agree; transitions and unknown states are unresolved. Durations are weighted by elapsed time and clipped to the requested operation, with no extra interval at the last endpoint. Every candidate containing unresolved time is rejected. Known blocked Earth intervals are checked against the maximum allowed uninterrupted gap; Sun clear time is compared with the minimum fraction. Ranking is lexicographic: shortest maximum Earth gap, longest joint clear duration, earliest start. No arbitrary safety score is used. Overlapping candidates are alternatives.

The verification button recomputes the selected duration with fresh Horizons geometry at five-minute spacing (or the finer overview spacing). It reports changes, not a guarantee that events shorter than the spacing cannot occur. The three height scenarios use the original overview spacing and re-query each observer altitude. They do not measure confidence or terrain error. Observer ground is bilinearly interpolated while the ray surface is triangulated; this mismatch and DEM resampling can affect near-ground results, especially comparisons of 1–5 m heights. No claim of actual metre-scale terrain accuracy is made.

Decision JSON contains inputs, candidate assessments, rows for verification and height tests when completed, and source metadata. A failed or incomplete verification is explicitly unavailable. Changing inputs invalidates previous decision results.

## Additional reproducible checks
Run `python -m unittest discover -s tests` and `node --test tests/*.mjs` (Node 22+). Tests include irregular timestamps, clipped duration, unresolved transitions, exact blackout limits, finer sampling revealing a missed event, and a deterministic 60-ray BVH versus exhaustive triangle comparison on synthetic curved terrain. This is implementation validation, not independent flight-grade validation of lunar illumination. `node tools/check_decisions.mjs` reproduces the bundled-data baseline.
