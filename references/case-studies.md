# Worked Cases

Two real scene builds, with the parameters that survived and the mistakes that produced the next version. All values are for Blender 3.6 EEVEE; rescale light power with distance and re-calibrate exposure in other versions.

Character shader authoring is deliberately **not** covered here. In Case 2, only set, light, camera, atmosphere, and delivery decisions are recorded.

---

## Case 1 — Gothic moonlit Victorian interior (v01–v12)

**Brief:** a static MMD character, high-quality render, lighting/camera/background done, simple indoor scene, headless, save every version, screenshot and iterate.

**Result:** v11 full-body 1920×1080, plus a 58 mm close-up derived from the same scene. Twelve versions, ~40 minutes of iteration.

### 1.1 Set

- 8 × 8 m room, 3.35 m ceiling; deep teal walls `(0.020, 0.044, 0.048)`, dark wood floor, wainscoting, gold trim.
- Left arched window 1.6 × 1.8 m, heavy curtains, separate night-sky plane, moon, 18 stars, no glass.
- Burgundy rug and armchair, console, gold-framed painting, chandelier, brass candlesticks, oil lamp, potted plant.
- Contact-shadow plane under the feet, 0.8 × 0.56 m.
- World: moonrise HDR, strength 0.15.

### 1.2 Final light rig (v11)

| Light | Type | Power | Color | Purpose |
|---|---|---:|---|---|
| Moon sky | Area 3.0 m | 25 W | (0.55, 0.70, 1.00) | Cool fill outside window |
| Moon shaft | Spot 28°, blend 0.80 | 320 W | (0.58, 0.72, 1.00) | Moonbeam and floor pool |
| Warm key | Area 2.2 m | 150 W | (1.0, 0.73, 0.50) | Warm key from front-right |
| Cool fill | Area 2.6 m | 28 W | (0.60, 0.75, 1.00) | Cool front-left fill |
| Rim | Area 1.0 m | 85 W | (0.58, 0.48, 1.00) | Violet back rim |
| Wall wash | Area 1.2 m | 13 W | (1.0, 0.70, 0.48) | Wall panels |
| Top soft | Area 2.6 m | 24 W | (1.0, 0.80, 0.60) | Chandelier bounce |
| Painting light | Area 0.6 m | 7 W | (1.0, 0.72, 0.45) | Painting, specular factor 0 |
| Candles ×3 | Point | 2.2 W | (1.0, 0.48, 0.16) | Practicals |
| Oil lamp | Point | 1.6 W | (1.0, 0.55, 0.22) | Practical |
| Chandelier | Point | 9 W | (1.0, 0.52, 0.22) | Practical |

Fog: color `(0.58, 0.68, 0.90)`, density 0.011, anisotropy 0.45, box 7.1 × 6.3 × 3.6 at `(0, −1.65, 1.5)`.

Camera: `(0.55, −4.15, 1.30)` → `(0.05, 0.30, 0.95)`, 44 mm, f/2.5, focus `(0.05, 0.10, 1.47)`, 1920×1080.

Render: 128 TAA, 64 volumetric, GTAO, SSR, bloom 1.0/4.5/0.02, Filmic, exposure −0.2, Medium High Contrast. Compositor: Fog Glow 1.2/8/−0.9 → ColorBalance → HueSat 1.06 → Lens Distortion −0.004/0.008 → ellipse vignette 0.95/0.18/0.30.

### 1.3 Version history (scene-relevant)

| Version | Change | Result |
|---|---|---|
| v01 | First full set: room, window night, furniture, fog, DOF, post | Composition worked; badly overexposed/pink; floating candle; blank mirror |
| v02 | Exposure +0.35→0.0, 1600×900/64, teal walls, light energies cut ~50–80%, fog 0.012→0.004 | Much better; feet cropped; chair too bright; mirror black |
| v03 | Camera back to `(0.55, −4.15, 1.30)`, 44 mm, aim `(0.05, 0.30, 0.95)`; moon shaft 1000 W; fog 0.006 | Feet, night, candle flames fixed; mirror/overexposure remained |
| v04 | Chair tinted burgundy; stars smaller/closer to window; shaft 1200 W; fog 0.008 | Stable; mirror still blown |
| v05 | Replaced mirror with arched night painting; 18 stars; shaft 1500 W/28°; stronger contact shadow | Composition better; painting became a silver mirror under SSR |
| v06 | Painting roughness 0.80/specular 0.15; spot moved outside; fog box narrowed | Mirror fixed; fog boundary appeared; vertical window streak |
| v07 | Real CC0 painting texture; **removed window glass**; fog box expanded to 7.1×6.3×3.6 | Moon gap, streak, fog boundary all fixed |
| v08 | Painting light 10→7 W, specular factor 0; fill/wash/top reduced; hands raised to hips | Painting hotspot gone; pose more natural |
| v09 | Exposure −0.2; shaft 1200 W; fog 0.011/anisotropy 0.45; vignette 0.30 | More cinematic; floor moon pool still hot |
| v10 | Moon shaft 1200→700 W | Pool softened |
| **v11** | Moon shaft 320 W, blend 0.80; 1920×1080/128/64 | Final full-body |
| v12 | Wrist targets moved forward to expose hands | Hands floated; rejected, restored v11 pose |

Close-up derived from v11: camera `(0.60, −2.15, 1.42)` → `(0.05, 0.08, 1.35)`, 58 mm, f/2.0, focus `(0.05, 0.10, 1.50)`, extra warm portrait fill 12 W at `(0.95, −1.25, 1.75)`. The first close-up cut the moon with window muntins; hiding three muntins fixed it.

### 1.4 Lessons

- **Exposure first, then every light.** v01 had a full set but +0.35 exposure and 750 W moonlight; nothing else could be judged until that was fixed.
- **A mirror is a trap.** A low-roughness asset plus SSR plus a bright world reads as a silver sheet. Matte painting + rough surface solved it; do not “fix” it by adding more light.
- **Window glass is optional.** Removing the glass plane fixed both the moon gap and the vertical white streak. Build the sky/moon outside, but skip the glass.
- **Fog box edges must be out of frame.** v06 showed a hard boundary at the bottom; expanding the box fixed it. Do not confuse a fog wall with a lighting problem.
- **Moon pool power has a narrow range.** 1500 W was a hard pool, 700 W still hot, 320 W with blend 0.80 was soft and natural. Change spot power and blend together.
- **Composition before details.** The feet crop was solved by camera distance/lens, not by moving the character or the set.
- **Static pose limits.** v12 tried to expose the hands by moving the wrist target; the hands detached visually. Restore the best version rather than fix-forward.
- **Roughness is a lighting control.** Painting light at 7 W with `specular_factor=0` removed the hotspot without changing exposure.
- **Save and log every iteration.** The final light table came from reading the version log, not memory.

---

## Case 2 — Black studio stage (scene/lighting only; v13–v23)

**Brief:** the user supplied dark-stage reference photos of the same character and asked to replicate the look. Only the **stage, lighting, camera, atmosphere, and delivery** are summarized; the character shader rebuild is out of scope.

**Result:** black stage with white arcs, tube practicals, gold-framed panel, white flower clusters; 72 mm three-quarter portrait 1440×1800 and 85 mm close-up 1200×1500.

### 2.1 Set

- Black circular floor radius 3.4 m, roughness 0.16, specular 0.65; black back/side walls for a seamless void.
- White emissive arcs at radius 1.75 and 2.05; a third at 2.35 was built but hidden.
- Three vertical white tubes, emission strength 5.0.
- Gold-framed black panel 1.55 × 2.30 m on the left.
- Six clusters of white five-petal flowers at different depths: right foreground, right midground, left background.
- Contact-shadow plane under the feet at `(0.05, 0.38, 0.024)`.
- World near-black `(0.0012, 0.0016, 0.0032)`, strength 0.25; volume fog object present but hidden.
- Adult add-on materials hidden with alpha 0; clothed, frontal presentation retained.

### 2.2 Final light rig (v23 scene)

| Light | Type | Power | Color | Purpose |
|---|---|---:|---|---|
| Key softbox | Area 1.4 m | 82 W | (1.00, 0.95, 0.92) | Warm front-right key |
| Cool fill | Area 2.4 m | 6 W | (0.55, 0.70, 1.00) | Cool front-left fill |
| Face fill | Area 0.4 m disk | 3 W | (1.00, 0.90, 0.86) | Face softening |
| Skin glint | Area 0.12 m disk | 24 W | (1.00, 0.97, 0.94) | Small skin highlight |
| Specular kicker | Area 0.22 m disk | 55 W | (1.00, 0.96, 0.92) | Nose/lip/shoulder specular |
| Cyan rim | Area 0.9 m | 320 W | (0.62, 0.84, 1.00) | Right back rim |
| Violet rim | Area 1.0 m | 195 W | (0.80, 0.76, 1.00) | Left back rim |
| Hair backlight | Area 0.6 m disk | 125 W | (0.68, 0.85, 1.00) | Hair edge |
| Top hair light | Area 1.7 m | 68 W | (0.86, 0.94, 1.00) | Top sheen |
| Floor bounce | Area 1.0 m | 3 W | (0.55, 0.72, 1.00) | Cool floor bounce |
| Tube light L | Area 0.3 m | 2 W | (0.60, 0.80, 1.00) | Practical |
| Tube light R | Area 0.3 m | 3 W | (0.60, 0.80, 1.00) | Practical |

Camera: three-quarter `(0.75, −3.05, 1.32)` → `(0.05, 0.28, 1.12)`, 72 mm, f/2.2, focus at eye `(0.045, 0.285, 1.492)`. Close-up `(0.45, −1.55, 1.50)`, 85 mm, f/2.0, same focus.

Render: 1440 × 1800, 128 TAA, 32 volumetric, bloom 0.85/6.0/0.028, Filmic, exposure −0.44, Medium High Contrast. Compositor: Fog Glow 0.9/8/−0.88 → ColorBalance → HueSat 1.10 → Lens Distortion −0.003/0.006 → vignette 1.2/0.22/0.25.

### 2.3 Version history (scene/camera-related only)

| Version | Scene/camera change | Result |
|---|---|---|
| v13 | Replaced the gothic set with black stage, two arcs, three tubes, gold panel, flower spheres; camera 52 mm at 1.35 m; exposure −0.10 | Stage language read, but overall heavily overexposed; flowers looked like balloons |
| v14 | Camera moved to 72 mm vertical composition; exposure −0.42; added kicker 38 W and hair backlight 95 W | Framing much closer to reference; exposure still high |
| v15 | Final camera `(0.75, −3.05, 1.32)`, 72 mm, f/2.2; hid volume fog | Cleaner black; stage composition locked |
| v16 | Exposure −0.55; key 82→55 W, cyan rim 230 W, violet 150 W, hair backlight 75 W; hid third arc; flowers changed to flat discs | Exposure recovered; petals looked like paper |
| v17 | Petals rebuilt as thin ellipsoids (10% thickness), five per flower, six clusters placed relative to camera; exposure −0.50; focus `(0.06, 0.14, 1.47)` | Flowers gained volume; all clusters stayed in frame; skin slightly dark |
| v18 | Focus moved to measured eye point `(0.045, 0.285, 1.492)` | Eyes sharp; camera locked |
| v20 | Added two extra concentric accent arcs | Strong concentric halo overwhelmed the character |
| v21 | Hid both accent arcs; main arc emission 0.48 | Background clean; subject regained focus |
| v22 | Added skin glint 24 W at 0.12 m; main arc emission 0.42; exposure −0.44 | Skin highlights and lips read; final exposure |
| **v23** | Scene/camera unchanged from v22; final 1440×1800/128 render + close-up | Final |

### 2.4 Lessons

- **Black is a lighting decision, not a world color.** World 0.0012/0.0016/0.0032 at 0.25 strength, no visible fog, and low bloom were all required; changing only the world color still produced gray.
- **Rim lights can be much stronger than the key.** Cyan rim 320 W and violet 195 W at grazing angles separated the silhouette without blowing out the face; the key stayed at 82 W.
- **Small specular sources do a lot.** A 0.12 m skin glint and 0.22 m kicker produced the reference's porcelain highlights without raising the key.
- **One arc is enough.** Adding accent arcs created a bullseye; hiding them was the fix, not reducing every light.
- **Flowers are set dressing, not spheres.** Thin ellipsoid petals with varied rotation and camera-relative placement read as flowers; spheres read as balloons.
- **Focus at the eye surface.** Moving the focus from a guessed point to the measured frontmost eye point made the portrait credible; f/2.2 keeps the ear soft.
- **Framing is intentional.** 72 mm portrait at 3.48 m gives ~1.74 m vertical coverage, so the feet are out of frame by design; the close-up uses 85 mm and a separate file.
- **Do not mix shader and scene iteration.** The shader rebuild changed apparent exposure and color; scene versions were judged on light/camera/set only, and the final scene is reproducible without the shader work.

---

## Transferable defaults

| Decision | Start here | Adjust when |
|---|---|---|
| Scene type | One simple interior or one stage | Brief explicitly asks for exterior/epic |
| Room size | 8 × 8 m, 3.35 m ceiling | Full-body needs more depth; close-up can use 5 × 5 m |
| Key | 2–3 m area at 3–4 m, 35–50° front-side | Smaller source for hard light; larger for beauty |
| Fill | 1/4–1/8 key, cooler, opposite side | High-key: 1/2–1 key |
| Rims | 1.5–3× key at grazing angles | Black stage: 2–4× key |
| Exposure | −0.2 to −0.5, Filmic | High-key: −0.05 to −0.2 |
| Fog | 0.004–0.012 density, box edges out of frame | Black stage: hide fog |
| Bloom | 0.02–0.055, threshold 0.85–1.2 | Thin white emissives: lower intensity, higher threshold |
| Full-body lens | 44–50 mm at 4.0–4.5 m | Tight room: 35 mm and accept perspective |
| Three-quarter | 65–85 mm at 2.5–3.5 m | Reference portrait: 72 mm |
| Close-up | 85–105 mm at 1.2–1.8 m | Keep f/2.0–f/2.8 for eye focus |
| Preview | 1152×1440 or 1280×720, 64 samples | Final 128 samples, full resolution |
