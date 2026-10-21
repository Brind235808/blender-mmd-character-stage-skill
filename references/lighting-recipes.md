# Lighting Recipes

Starting points for a character ~1.6–1.75 m tall, camera 2.5–4.5 m away, EEVEE Legacy in Blender 3.6. Wattages are not physical; treat them as relative values and rescale with distance.

## Calibration first

1. Set **Filmic** and exposure **−0.2 to −0.5**. Do not judge lighting in Standard.
2. Put the key at 35–50° front-side, slightly above eye level, large enough to wrap the face.
3. Fill opposite the key at 1/4–1/8 key power; cooler than the key.
4. Add rims behind at 3/4 and 5/4; one cool, one warm/complementary.
5. Add practicals and background light last.
6. Check: skin highlights retain detail; the background is darker than the face; the silhouette separates from the background.

Rules of thumb:

- Area light power roughly follows inverse square: doubling distance needs ~4× power.
- Soft key size 2–3 m at 3–4 m; rim size 0.8–1.3 m; face fill 0.4–0.6 m.
- Key:fill ≈ 4:1–8:1 for low-key, 2:1–3:1 for high-key.
- Rim may be 1.5–3× key power because it hits at a grazing angle.
- Spot lights: 28–35°, blend 0.55–0.80.
- Contact shadows: distance 0.2, bias 0.03, thickness 0.2; enable on key/fill/rim/moon.
- For black sets, keep world strength 0.15–0.30 and hide the fog; for foggy rooms, 0.3–0.6 world and density 0.006–0.012.

## Recipe A — Gothic moonlit interior (v11)

**Set:** 8 × 8 m room, 3.35 m ceiling; deep teal walls `(0.020, 0.044, 0.048)`, dark wood floor and wainscoting, gold trim, burgundy rug and chair. Arched window at the left with a separate night-sky plane, moon, 18 stars; no glass. Curtains, console, framed painting, chandelier, candles, plant.

**Lights**

| Light | Type | Power | Color | Position | Purpose |
|---|---|---:|---|---|---|
| Moon sky | Area 3.0 m | 25 W | (0.55, 0.70, 1.00) | (−1.55, 4.6, 2.4) | Cool sky fill outside the window |
| Moon shaft | Spot 28°, blend 0.8 | 320 W | (0.58, 0.72, 1.00) | (−1.55, 3.25, 2.4) → (−0.90, −0.10, 0.55) | Moonbeam and floor pool |
| Warm key | Area 2.2 m | 150 W | (1.0, 0.73, 0.50) | (2.3, −2.45, 2.1) | Warm front-right key |
| Cool fill | Area 2.6 m | 28 W | (0.60, 0.75, 1.00) | (−2.0, −2.6, 1.6) | Cool front-left fill |
| Rim | Area 1.0 m | 85 W | (0.58, 0.48, 1.00) | (1.5, 1.85, 2.15) | Violet back-right rim |
| Wall wash | Area 1.2 m | 13 W | (1.0, 0.70, 0.48) | (0.7, −0.9, 2.25) | Panel texture |
| Top soft | Area 2.6 m | 24 W | (1.0, 0.80, 0.60) | (0.2, 0.0, 3.1) | Chandelier bounce |
| Painting light | Area 0.6 m | 7 W | (1.0, 0.72, 0.45) | (1.55, 1.95, 2.52) | Framed painting, specular factor 0 |
| Candle ×3 | Point | 2.2 W | (1.0, 0.48, 0.16) | At flames | Warm practicals |
| Oil lamp | Point | 1.6 W | (1.0, 0.55, 0.22) | (0.92, 2.15, 1.62) | Warm practical |
| Chandelier | Point | 9 W | (1.0, 0.52, 0.22) | (1.1, 1.5, 2.52) | Warm practical |

**World:** `qwantani_moonrise_puresky_2k.hdr`, strength 0.15.

**Atmosphere:** fog color `(0.58, 0.68, 0.90)`, density 0.011, anisotropy 0.45, volume box 7.1 × 6.3 × 3.6 centered at (0, −1.65, 1.5); keep the box edges out of frame.

**Camera:** (0.55, −4.15, 1.30) → (0.05, 0.30, 0.95), 44 mm, f/2.5, 7 blades, focus empty at (0.05, 0.10, 1.47). Full body with feet visible.

**Render:** 1920 × 1080, 128 TAA, 64 volumetric, GTAO 0.3/1.0, SSR, bloom threshold 1.0 / radius 4.5 / intensity 0.02, Filmic, exposure −0.2, Medium High Contrast.

**Compositor:** Fog Glow (threshold 1.2, size 8, mix −0.9) → ColorBalance (lift 0.985/0.98/1.0, gain 1.03/1.0/0.97) → HueSat 1.06 → Lens Distortion (−0.004, 0.008) → blurred ellipse vignette (0.95 × 0.18 × 0.30).

## Recipe B — Black studio stage (v23 scene only)

This is a **scene/lighting** recipe. The character shader work from that phase is out of scope and is not described here.

**Set:** black circular floor radius 3.4 m (roughness 0.16, specular 0.65), black back/side walls, two visible white emissive arcs (radius 1.75 and 2.05; a third at 2.35 is hidden), 3 vertical white tubes (emission 5.0), a gold-framed black panel at the left, 6 clusters of white five-petal flowers at different depths, contact shadow under the feet.

**Lights**

| Light | Type | Power | Color | Position | Purpose |
|---|---|---:|---|---|---|
| Key softbox | Area 1.4 m | 82 W | (1.00, 0.95, 0.92) | (2.1, −2.7, 2.15) | Warm front-right key |
| Cool fill | Area 2.4 m | 6 W | (0.55, 0.70, 1.00) | (−2.3, −2.2, 1.55) | Cool front-left fill |
| Face fill | Area 0.4 m disk | 3 W | (1.00, 0.90, 0.86) | (0.85, −1.45, 1.72) | Face softening |
| Skin glint | Area 0.12 m disk | 24 W | (1.00, 0.97, 0.94) | (0.45, −2.2, 2.1) | Small skin highlight |
| Specular kicker | Area 0.22 m disk | 55 W | (1.00, 0.96, 0.92) | (1.55, −1.55, 2.0) | Nose/lip/shoulder specular |
| Cyan rim | Area 0.9 m | 320 W | (0.62, 0.84, 1.00) | (1.65, 2.25, 2.05) | Right back rim |
| Violet rim | Area 1.0 m | 195 W | (0.80, 0.76, 1.00) | (−1.65, 1.95, 1.95) | Left back rim |
| Hair backlight | Area 0.6 m disk | 125 W | (0.68, 0.85, 1.00) | (0.4, 1.4, 2.05) | Hair edge |
| Top hair light | Area 1.7 m | 68 W | (0.86, 0.94, 1.00) | (0.45, −0.25, 3.15) | Top hair sheen |
| Floor bounce | Area 1.0 m | 3 W | (0.55, 0.72, 1.00) | (0, −0.65, 0.16) | Cool floor bounce |
| Tube light L | Area 0.3 m | 2 W | (0.60, 0.80, 1.00) | (−1.75, 2.3, 1.45) | Practical tube light |
| Tube light R | Area 0.3 m | 3 W | (0.60, 0.80, 1.00) | (1.85, 2.5, 1.5) | Practical tube light |

**World:** near-black `(0.0012, 0.0016, 0.0032)`, strength 0.25. Hide the volume fog for the cleanest black.

**Camera:** three-quarter portrait at (0.75, −3.05, 1.32) → (0.05, 0.28, 1.12), 72 mm, f/2.2, focus at the eye surface (0.045, 0.285, 1.492). Close-up at (0.45, −1.55, 1.50), 85 mm, f/2.0, same focus.

**Render:** 1440 × 1800, 128 TAA, 32 volumetric, bloom threshold 0.85 / radius 6.0 / intensity 0.028, Filmic, exposure −0.44, Medium High Contrast.

**Compositor:** Fog Glow (0.9, size 8, mix −0.88) → ColorBalance (lift 0.985/0.99/1.01, gain 1.02/1.0/0.985) → HueSat 1.10 → Lens Distortion (−0.003, 0.006) → blurred ellipse vignette (1.2, blur 0.22, Fac 0.25).

## Recipe C — Warm candlelit boudoir

A generic warm interior for burgundy/gold characters.

- Key: area 2.0 m, 120 W, 2700 K, at (2.0, −2.5, 2.0) → face.
- Fill: area 2.5 m, 20 W, cool 6500 K, at (−2.0, −2.0, 1.6).
- Rim: area 1.0 m, 60 W, amber/violet, at (−1.5, 1.8, 2.0).
- Practicals: 3–5 candle points at 3 W each; one oil lamp at 12–18 W.
- Fog: density 0.005–0.008, warm gray-blue; keep the box edges out of frame.
- Set: 6 × 6 m room, bed/vanity, heavy curtains, rug, gold frame, dark wood.
- Camera: 50 mm full-body at 4 m, or 85 mm half-body at 2.2 m.
- Exposure: −0.25 to −0.4.

## Recipe D — High-key atelier

For pastel, spring, soft characters.

- Key: area 3.0 m, 300 W, neutral white, at (2.0, −3.0, 2.5).
- Fill: area 3.0 m, 100 W, at (−2.5, −2.5, 2.0).
- Background: area 2.0 m, 80 W, at (0, 2.5, 2.2), aimed at the wall.
- Top: area 2.0 m, 40 W, overhead.
- World: light gray, strength 0.4–0.6.
- Bloom: threshold 1.2, intensity 0.015; avoid clipping white fabric.
- Camera: 50–85 mm, f/2.5–4.0.
- Exposure: −0.05 to −0.2.

## Recipe E — Neon studio / cyber

For neon hair, techwear, chrome.

- Key: area 1.5 m, 60 W, cool white, front-left.
- Rim A: area 1.0 m, 200 W, magenta `(1.0, 0.2, 0.7)`, back-left.
- Rim B: area 1.0 m, 220 W, cyan `(0.1, 0.7, 1.0)`, back-right.
- Floor: glossy black/wet; add a large area bounce at 10–20 W.
- Haze: density 0.006–0.010; bloom 0.04–0.06, threshold 0.8.
- Camera: 35–50 mm full-body, low angle optional.
- Exposure: −0.4 to −0.6.

## Quick symptom guide

| Symptom | First thing to try |
|---|---|
| Skin/white cloth clipped | Lower exposure 0.2–0.3, cut key 20–30%, lower Specular on cloth |
| Flat, no separation | Increase rim 30–50%, darken fill and background |
| Harsh shadows | Increase key size, add fill, enable soft shadows |
| Gray/veiled black background | Lower world strength, hide fog, reduce bloom |
| Visible fog wall | Enlarge the volume box, move edges out of frame, reduce density |
| Halo around arches | Lower emissive strength; hide secondary arcs |
| Character blends into set | Add a rim or darken the set directly behind the silhouette |
| Prop steals focus | Darken/desaturate the prop, move it out of the key, reduce its material emission |
| Face too dark in a full-body | Add a small face fill/glint, do not raise the whole key |
| Feet cropped | Widen lens or pull camera back; check the vertical coverage formula in the debug playbook |

For artifact-specific fixes, see `scene-debug-playbook.md`.
