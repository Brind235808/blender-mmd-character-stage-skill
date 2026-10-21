---
name: build-character-stage
description: Build a Blender/MMD character scene and lighting rig from a supplied character or reference. Use when the user provides a character model (PMX/FBX/GLB) or character images and asks for an environment, lighting, camera, atmosphere, background, render look, or a fully staged render — e.g. gothic moonlit interior, candlelit room, dark studio stage, high-key atelier. Covers style analysis, set dressing, light rigs, camera/DOF, fog, EEVEE/compositor settings, headless preview iteration, version saving, texture packing, and portable delivery. Use 角色场景、布景、灯光、镜头、氛围 关键词触发. Do not use for character shader authoring or re-texturing the character.
---

# Build Character Stage / 角色场景搭建

## Scope

This skill covers **environment, set dressing, lighting, camera, atmosphere, and final render/delivery** for a character. It does not cover rebuilding the character's shader, replacing MMD materials, or re-texturing the character. If the user asks for those, treat them as a separate task and do not mix them into the stage build.

## Operating contract

Derived from the user's original brief; details and exact quotes are in `references/user-brief.md`.

- **Headless only:** run `blender.exe -b --python <script>`; never leave a foreground Blender window.
- **Persist until done:** do not stop at a plan, a script, or a code-only check. Render, inspect the actual image, and iterate.
- **Save before every improvement:** create a new `versions/vNN_scene.blend` before each render. Never overwrite or delete an older version.
- **Screenshot-driven:** render a preview and inspect the PNG visually; judge the image, not the logs. Crop the face/hair/eyes when needed.
- **Document everything:** record each version's changes, the best version, and the final light/camera tables.
- **Pack for portability:** pack all textures, use `//renders/...` relative output paths, verify, and create a backup.
- **Do not touch earlier deliverables:** add new files with new names; keep the previous best version intact.
- **Respect model licenses:** if the readme forbids redistribution, keep the `.blend` containing model data local.
- **Language:** give concise updates in the user's language (Chinese when the user writes Chinese).

## Default workflow

### 0. Intake — infer, don't interrogate

Accept any of: a character model path, a PMX/FBX/GLB file, character images, a mood board, or a one-line style brief.

Infer from the character itself: hair/eye/outfit palette, material story, silhouette, genre, and the story beat. If a detail is missing, choose a sensible default and proceed. Only ask when a decision is expensive to undo (e.g. a completely different scene direction, or a licensed asset purchase).

If the user says "先策划一下 / plan first / don't touch anything", produce a plan and wait. Otherwise, proceed end-to-end.

Default unless the brief says otherwise: a **simple interior**, one hero set, 2–3 supporting props, one camera, and a dark-to-mid value plan that makes the character read first.

### 1. Read the character's style

Write a five-line style card before building:

1. **Palette** — dominant hair/eye/outfit colors, metal accents, temperature, saturation.
2. **Material story** — porcelain skin, silk, lace, leather, armor, chrome, fur.
3. **Silhouette** — flowing skirt, cape, armor, twin-tails, veil; what will catch light.
4. **Genre/era** — gothic, fantasy, modern, sci-fi, idol, historical.
5. **Narrative beat** — arrival, vigil, portrait, performance, aftermath.

Map the card to a scene direction:

| Character cues | Scene direction | Key | Fill / rim | Atmosphere |
|---|---|---|---|---|
| Pale skin, lavender/cyan hair, white lace, elegant | Black studio or moonlit gallery | Soft cool key, large source | Cool fill + cyan/violet rims | Near-black, glossy floor, sparse white accents |
| Burgundy/gold, corset, Victorian | Candlelit Victorian interior | Warm key from front-right | Cool moon fill + violet rim | Volumetric moon shaft, light fog |
| Warm gold/red, ornate, desert | Sunset palace / tent | Low warm key | Amber bounce + cool sky rim | Dust, warm haze |
| Neon hair, techwear, chrome | Neon studio / alley | Cool white key | Magenta/cyan rims | Haze, wet reflective floor |
| Pastel, spring, soft | High-key atelier / garden room | Very large soft key | White bounce + faint cool rim | Bright, low contrast, airy |
| Steel, armor, knight | Stone hall / forge | Hard cool key | Cold fill + warm forge rim | Smoke, strong contact shadow |
| Idol, energetic, colorful | Stage with practicals | Bright frontal key | Colored rims | Bloom, practicals, light beams |

If the character has a strong single color, build the set around its **complement or value contrast**, not more of the same color. Example: cyan/lavender hair → warm skin key + cool environment, or black set + white arcs.

## Character prep (after the style card, before composition)

Import and stage the character first; the set is built around its real proportions, not a guessed height.

- PMX: `bpy.ops.mmd_tools.import_model(filepath=..., scale=0.08, types={"MESH", "ARMATURE", "MORPHS"})`. FBX/GLB: use the built-in importer and check up/forward axes.
- Measure the world bounding box of all character meshes; normalize height to 1.60–1.75 m, ground the lowest point at `z ≈ 0.02`, and face the camera.
- Preserve the imported materials, object/bone names, and shape keys. This skill does not rebuild the character shader.
- Hide adult add-ons with alpha 0 or `hide_render`; keep the data for license compliance.
- Put the eye focus empty on the measured frontmost eye surface, not the head-bone origin.
- If the palette is unclear, render one neutral gray lookdev pass before choosing the scene; do not count it as a scene version.

Full snippets and quick checks: `references/character-prep.md`.

### 2. Compose camera-first

Place the subject and camera before building the room. Build only what the frame can see.

- Choose framing: full-body, three-quarter, or close-up.
- Choose one **hero prop** that explains the character (throne, mirror, window, arch, piano, flowers).
- Add 2–3 supporting props at different depths; keep the rest empty.
- Plan three values: dark background, midtone set, bright subject/accent.
- Use foreground occlusion (blurred flowers, curtain edge) and leading lines (arches, window frames, corridor).
- Keep the character silhouette clear; do not put a bright prop directly behind the head.

### 3. Build the set

Scale reference: character 1.6–1.75 m; room 8 × 8 m, ceiling 3.35 m; door 2.1 m; window 1.6 × 1.8 m.

- Build a closed set: floor, back wall, two side walls (or a cyclorama). Avoid gaps at the frame edge.
- Use physically plausible materials: roughness, specular, subtle bump; avoid pure white/black except as intentional accents.
- Add trim/baseboards/panels to give scale; keep geometry simple and rely on lighting.
- Place practicals (candles, oil lamp, chandelier, tubes) as visible sources; add small lights at the flame/tube.
- Add a **contact shadow** plane under the feet (gradient alpha, ~0.8 × 0.56 m) so the character sits on the floor.
- For windows: build a separate night sky/moon/stars layer outside; **remove window glass** if it creates a moon gap or a vertical white streak.
- Hide adult/inappropriate add-ons if the model has them; keep the presentation tasteful.
- Name objects and collections clearly (`Set_`, `Prop_`, `Light_`, `FX_`).

### 4. Light in layers

Build in this order; do not start with rim lights.

1. **Key** — large area softbox, 35–50° front-side, slightly above eye level; warm or neutral.
2. **Fill** — opposite side, 1/4–1/8 of key, cooler; large and soft.
3. **Rim(s)** — two area lights behind at 3/4 and 5/4; one cool, one warm/complementary; rim can exceed key power for separation.
4. **Background / wall wash** — low power, shapes the set without stealing focus.
5. **Practicals** — visible flames/tubes plus small point/area lights; keep them subtle.
6. **Atmosphere** — fog/volume after the light rig is readable.

Rules:

- Use **contact shadows** on key/fill/rim/moon; enable soft shadows.
- Calibrate exposure so skin highlights keep detail and the background stays dark. Start at exposure −0.2 to −0.5 with Filmic + Medium High Contrast.
- Keep skin tones protected: avoid equal-RGB white light on skin; use a warm key and cool fill/rim.
- If the image is flat, increase rim/key ratio before adding more fill.
- If the background is gray, lower world strength or hide the fog; do not just crush exposure.

Concrete wattages at a ~3 m subject distance are in `references/lighting-recipes.md`. Treat them as starting points and rescale with inverse-square distance.

### 5. Camera and depth of field

| Framing | Lens | Distance | Aperture | Notes |
|---|---:|---:|---:|---|
| Full-body | 44–50 mm | 4.0–4.5 m | f/2.5–4.0 | Feet fully in frame with margin; check the bottom edge |
| Three-quarter | 65–85 mm | 2.5–3.5 m | f/2.0–2.8 | Crop mid-thigh or below intentionally |
| Close-up | 85–105 mm | 1.2–1.8 m | f/2.0 | Focus on the eye surface, not the face center |

- Use a **Focus empty** at the frontmost eye point. Compute it from the eye mesh, not from the head bone.
- Leave headroom; avoid tangent lines at the frame edges.
- Check that foreground flowers/props are inside the camera frustum before placing them.
- Build depth layers: foreground (blurred), subject (sharp), background (soft arcs/window).
- For full-body, verify the feet are not cut by rendering once before detailing the set.

### 6. Atmosphere and compositor

Start subtle; atmosphere should support the character, not fog the image.

- **Fog:** volume cube, density 0.004–0.012, anisotropy 0.3–0.5. Keep the box edges outside the camera or hide the fog for a black stage.
- **Bloom/glare:** Fog Glow, threshold 0.9–1.2, size 8, mix −0.88; bloom intensity 0.02–0.055.
- **Color balance:** cool lift, slightly warm gain; HueSat 1.06–1.10.
- **Lens:** distortion −0.003 to −0.004, dispersion 0.006–0.008.
- **Vignette:** blurred ellipse, multiply 0.15–0.30; avoid a hard ring.
- **EEVEE:** 128 TAA samples, 64 volumetric samples, GTAO, SSR/refraction, soft shadows, Filmic + Medium High Contrast.
- Blender 4.2+ EEVEE Next changes bloom/SSR/volume behavior; verify the look in the target version.

### 7. Preview/debug loop

1. Save `versions/vNN_scene.blend` **before** rendering.
2. Render a preview at 1152 × 1440 / 64 samples (or 1280 × 720 for wide scenes).
3. Inspect the PNG. Name the top three issues in priority order.
4. Change **one variable group** per version (e.g. exposure + key power; or fog density + volume bounds; or camera + focus).
5. Save `vNN+1`, render, compare side by side.
6. Record the change and result in the version log.
7. If the new version is worse, return to the best saved version; do not fix forward blindly.

Use `scripts/render_preview.py` for headless previews, `scripts/contact_sheet.py` for a version sheet, and `scripts/inspect_blend.py` for scene diagnostics. Detailed symptom → cause → fix tables are in `references/scene-debug-playbook.md`.

### 8. Final render and delivery

- Save the final `.blend`; render the final image at the agreed resolution/samples.
- Pack all textures with `bpy.ops.file.pack_all()`; set `scene.render.filepath = "//renders/<name>.png"`.
- Verify with `scripts/verify_pack.py`; require 100% packed, zero missing, relative path, camera, and resolution.
- Make a contact sheet of all versions; keep every version.
- Append a version log: reference analysis, version table, final light/camera table, file list, usage, license.
- Choose the best image and its matching `.blend`; keep previous deliverables untouched.
- Back up the packed `.blend`, renders, scripts, and log.
- Report the final paths and the main changes in the user's language.

## User prompt details

Read `references/user-brief.md` when starting a new project or when the user references their earlier requirements. The non-negotiables:

- Background-only Blender, no foreground window.
- Save a version before improving; never lose an old version.
- Render and inspect screenshots; iterate until the result is good.
- Save the `.blend`, document each version, pick the best, pack for moving computers.
- Use a simple indoor scene unless the character/reference demands otherwise.
- Keep model files local when the license forbids redistribution.

## Worked cases

`references/case-studies.md` contains two complete case studies:

1. **Gothic Victorian interior** (v01–v12): moonlight through an arched window, candlelit set, 44 mm full-body, 12 iterations.
2. **Black studio stage** (v13 scene): white arcs, tube lights, gold frame, white flowers, 72 mm three-quarter and 85 mm close-up. The character shader work from that phase is deliberately excluded.

Use them for parameter starting points and for the debugging history, not as templates to copy blindly.

## Resources

- `references/user-brief.md` — exact user prompts, preferences, delivery checklist, folder layout.
- `references/character-prep.md` — PMX/FBX import, height/ground/pose, eye focus, add-on hiding, neutral lookdev.
- `references/lighting-recipes.md` — light rigs, wattage tables, color/exposure calibration, symptom fixes.
- `references/scene-debug-playbook.md` — diagnostics, artifact fixes, camera/frustum checks, iteration protocol.
- `references/case-studies.md` — gothic interior and black studio case studies with final parameters.
- `scripts/inspect_blend.py` — dump scene, lights, camera, images, pack status (run with Blender `-b`).
- `scripts/render_preview.py` — headless preview render with resolution/samples overrides.
- `scripts/verify_pack.py` — verify packed textures, relative output path, camera, resolution.
- `scripts/contact_sheet.py` — build a labeled version contact sheet with PIL (system Python).

## Script quick start

Set `SKILL` to this skill folder and `BLENDER` to the Blender executable (on this machine `D:/BLENDER/blender.exe`). None of these scripts saves the `.blend`.

```bash
"$BLENDER" -b --python "$SKILL/scripts/inspect_blend.py" -- --blend "path/to/scene.blend"

"$BLENDER" -b --python "$SKILL/scripts/render_preview.py" -- \
  --blend "path/to/scene.blend" --out "renders/vNN_preview.png" \
  --width 1152 --height 1440 --samples 64

# lighting-only diagnostic: no compositor, no fog
"$BLENDER" -b --python "$SKILL/scripts/render_preview.py" -- \
  --blend "path/to/scene.blend" --out "renders/debug_raw.png" \
  --width 768 --height 960 --samples 32 --raw --no-fog

"$BLENDER" -b --python "$SKILL/scripts/verify_pack.py" -- \
  --blend "deliverables/final.blend" --blend "deliverables/closeup.blend"

python "$SKILL/scripts/contact_sheet.py" "renders/v*_preview.png" \
  --out "renders/version_contact_sheet.jpg" --cols 4 --title "Scene versions" --best v11
```

`verify_pack.py` exits nonzero on failure and prints `VERIFY_OK` or `VERIFY_FAIL`. `--expect-width/--expect-height` apply to every file in that call, so group files with the same resolution.
