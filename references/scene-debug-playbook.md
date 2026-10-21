# Scene Debug Playbook

How to find out why a render is wrong, fix one thing at a time, and keep every version. Written for headless Blender 3.6 EEVEE; notes for 4.2+ are at the end.

## 1. Evidence order

Do not guess from the script. Gather in this order:

1. **Scene facts** — engine, resolution, samples, exposure, view transform, camera, light list, world, packed textures.
2. **Raw render** — turn off the compositor and render again. If the raw image is good, the problem is in post; if it is bad, the problem is in lighting/scene/camera.
3. **Layer isolation** — hide fog, then bloom, then rims/fill, then the set, rendering small previews. The layer that changes the symptom is the culprit.
4. **Frustum/bounds** — check where objects actually are in camera space; do not trust the viewport or your mental model.
5. **Reference comparison** — if a reference exists, crop both to the same framing and compare value, color, and contrast, not details.

A useful first move is always:

```bash
"D:/BLENDER/blender.exe" -b --python scripts/inspect_blend.py -- --blend "path/to/scene.blend"
```

Then render a diagnostic preview:

```bash
"D:/BLENDER/blender.exe" -b --python scripts/render_preview.py -- \
  --blend "path/to/scene.blend" --out "path/to/debug_raw.png" \
  --width 768 --height 960 --samples 32 --raw
```

## 2. Diagnostic passes

Use cheap 32–64 sample previews at 60–75% resolution. Render one pass per question.

| Pass | How | What it tells you |
|---|---|---|
| Raw | `scene.use_nodes = False` (`--raw`) | Lighting only. Removes glare, color grade, lens, vignette. |
| No fog | hide mesh objects with `fog`/`volume` in the name (`--no-fog`) | Fog walls, gray blacks, lost contrast, blocked moonbeam. |
| No bloom/glare | disable `scene.eevee.use_bloom` and bypass Glare node | Halos, glow blobs, clipped highlights. |
| Key only | mute/hide fill, rims, practicals | Key shaping, shadow direction, exposure headroom. |
| Key + fill | add fill back | Fill ratio, flatness, face readability. |
| Add rim | add rims | Silhouette separation, color spill on skin. |
| Set only | hide character collection | Set exposure, hotspots, composition without the subject. |
| Character only | hide set | Is the character itself lit correctly? |
| No compositor color grade | raw + Glare only | Whether the grade is crushing or tinting. |

Keep diagnostic renders outside `versions/` so they do not pollute the version sheet.

## 3. Scene facts checklist

- **Engine** is EEVEE, not Workbench/Cycles; Cycles will not match an EEVEE look.
- **Resolution percentage is 100%** for finals. A blend saved at 50% silently halves output.
- **Camera** is `scene.camera`; lens, sensor fit, f-stop, focus object.
- **Exposure/view transform** are Filmic + exposure −0.2 to −0.5; Standard makes everything clip.
- **World strength** is low for dark sets; an HDR can light the whole room invisibly.
- **Fog object** is visible, its box encloses the subject, and its edges are outside the frustum.
- **Images**: every FILE image is packed, none missing, none pointing to a dead drive.
- **Light units**: area/point in watts, spot cone, contact shadows, `specular_factor`.
- **Object visibility**: `hide_render` vs `hide_viewport`; objects can be visible in the viewport and hidden in render, or vice versa.
- **Collections** may have render visibility off even when objects are on.

## 4. Symptom → cause → fix

### Exposure and tone

| Symptom | Likely cause | Fix |
|---|---|---|
| Skin/white cloth clipped to pure white | Exposure too high, key too strong, Specular too high, bloom | Drop exposure 0.2–0.3, cut key 20–30%, lower cloth Specular/Sheen, raise glare threshold |
| Overall gray, washed out | World too strong, fog too dense, Standard view transform, compositor lift | World down, fog density down, Filmic, remove lift, add a dark value in frame |
| Background not black on a black set | World strength, fog, bloom, ambient/SSR, floor bounce | World 0.001–0.003 / strength 0.25, hide fog, bloom intensity ≤0.03, darken floor |
| Character too dark while set is bright | Key aimed at set, fill lighting the walls, background wash too strong | Aim key at face, cut wall wash, add small face fill, darken set behind subject |
| Highlights roll off ugly / gray | Filmic + too much light; low contrast look | Reduce light, Medium High Contrast, keep highlights below clipping |
| Color cast on skin | Strongly tinted rim/fill or HDR | Warm neutral key, cool fill only from behind/side, reduce rim spill, neutralize world |
| One side of face muddy | Fill too weak or too close to key angle | Fill opposite key, 1/4–1/8 key, large and soft; add tiny glint if needed |

### Shadows and grounding

| Symptom | Likely cause | Fix |
|---|---|---|
| Character floats | No contact shadow, lights not casting shadows, shadow disabled on object | Add gradient contact-shadow plane, enable shadows, check light `use_shadow` |
| Harsh black shadows | Small source, no fill, high contrast | Increase key size 1.5–2×, add fill, enable soft shadows, raise contact-shadow thickness |
| No shadow at all | Contact shadow off, light size huge, object `visible_shadow` off | Enable contact shadows (distance 0.2, bias 0.03, thickness 0.2), check object visibility |
| Shadow acne / stripes | Bias too low, coplanar floor | Raise bias slightly, move contact plane 1–2 mm above floor, avoid coplanar surfaces |
| Prop looks pasted on | No shadow/contact, wrong scale, wrong color temperature | Add contact shadow, match light direction, grade the prop into the set |

### Atmosphere and glow

| Symptom | Likely cause | Fix |
|---|---|---|
| Visible fog wall/band | Volume box edge inside frustum | Enlarge box so all edges are out of frame and behind the set; lower density |
| Gray veil over everything | Fog density too high, world volume, bloom mix | Density 0.004–0.012, hide fog for black sets, reduce glare mix |
| Moonbeam invisible | No volume, spot outside volume, density too low, spot angle wrong | Ensure spot cone intersects the volume, density ≥0.006, anisotropy 0.3–0.5, widen cone |
| Beam too hard / solid | Density high, spot blend low, tiny source | Lower density, raise blend 0.55–0.8, enlarge spot size |
| Halo/concentric rings | Overlapping emissive arcs + bloom, low glare threshold | Hide extra arcs, lower emission 0.4–0.5, raise glare threshold, reduce bloom size/mix |
| Glow blobs on metal | Specular kicker too strong, bloom threshold too low | Reduce kicker, raise threshold, increase roughness slightly |
| White streak from window | Glass plane refraction/reflection or muntin in front of moon | Remove window glass; hide muntins for close-ups; place sky/moon outside |
| Moon has a gap | Muntin or curtain edge cuts it | Move moon, hide muntin, open curtain, or accept as composition |
| Practicals do not read as light sources | No emission, no bloom, tiny flame | Add emissive flame/tube, small point light at source, subtle bloom |
| Practicals blow out | Emission too high, point light too strong | Emission down, point 1.5–3 W at small scale, distance falloff |

### Set and materials

| Symptom | Likely cause | Fix |
|---|---|---|
| Mirror/painting looks like a silver mirror | Low roughness + SSR + white world/lights | Roughness 0.7–0.85, Specular 0.1–0.2, remove white reflections, matte canvas |
| Wall hotspot | Light too close, small source, high power | Move light back, enlarge source, lower power, use wall wash at grazing angle |
| Set looks like a plain box | No trim, no depth layers, flat wall | Baseboards, wainscot, panels, foreground occlusion, 2–3 depth planes |
| Everything is the same value | No value plan | Dark background, midtone set, bright face/accent; add a practical or rim |
| Prop steals focus | Bright color/emission behind or beside head | Darken/desaturate, move out of key, lower emission, blur with DOF |
| Character blends into background | Similar value/color behind silhouette | Rim light, darken set behind subject, change background value |
| White flowers look like balloons | Spheres, high specular, no thickness | Thin ellipsoid petals (10% thickness), 5 petals, varied rotation, roughness up |
| Flowers pop in/out of frame | Placed in world space without frustum check | Use `world_to_camera_view`, keep 0.03–0.05 margin, place relative to camera |
| Floating candle/prop | Asset origin/bounds wrong | Snap to surface, check world bounding box, add contact shadow |
| Set edge visible | Room too small for camera | Extend walls/floor, move camera in, or add a dark falloff at the edge |

### Camera and composition

| Symptom | Likely cause | Fix |
|---|---|---|
| Feet cropped | Coverage too small or aim too high | Pull back, widen lens, lower aim; compute vertical coverage (Section 5) |
| Too much empty space | Lens too wide / subject too far | Longer lens or move in; keep 5–10% margin |
| Face distorted | Wide lens too close | 85–105 mm for close-ups, ≥65 mm for three-quarter |
| Eyes soft, ear sharp | Focus on face center/head bone | Focus empty at frontmost eye surface, f/2.0–f/2.8 |
| Whole image soft | f-stop too wide, focus distance wrong | f/2.8–f/4 for full body, verify focus object |
| Horizon tilted | Track-to up axis wrong | Camera Track To: To `-Z`, Up `Y`; check verticals |
| Subject dead center | No composition plan | Offset subject, use negative space, leading lines, foreground blur |
| Prop tangent to head | Prop directly behind silhouette | Move prop laterally/behind, darken it, use DOF |
| Crop cuts hands awkwardly | Framing chosen after pose | Choose crop between joints, not through wrists/ankles |

### Render artifacts and performance

| Symptom | Likely cause | Fix |
|---|---|---|
| Pink/missing textures | Unpacked images, dead paths | `bpy.ops.file.pack_all()`, verify with `verify_pack.py` |
| Hair/eyelash sorting errors | Alpha blend mode, backface culling | Check material blend method, `show_transparent_back`, shadow method; avoid changing the character shader beyond render settings |
| Aliased thin arcs/tubes | Low TAA, thin geometry | 128 TAA for finals, slightly thicker geometry, bloom softens |
| Noisy volumetrics | Low volumetric samples, large volume | 64 samples for finals, 32 preview, reduce volume size, raise tile size |
| Long render times | 4K + 128 TAA + volumetrics + SSR | Preview 60–75% at 64 samples; final only after look is locked |
| EEVEE bloom missing in 4.2+ | Bloom removed in EEVEE Next | Use compositor Glare (Fog Glow/Bloom); verify volume/shadow settings |
| Colors/light units differ in 4.2+ | EEVEE Next changes | Re-check exposure/light power; do not assume a 3.6 file matches |

## 5. Camera and frustum math

Blender's `sensor_fit = AUTO` uses `sensor_width` on the **longer image dimension**. For a portrait render, 36 mm is the vertical sensor; for landscape, it is horizontal. This is why a 72 mm portrait lens frames much tighter than expected.

Exact pinhole coverage at a plane perpendicular to the camera axis:

```
coverage = distance * sensor_dimension / focal_length
```

```python
from mathutils import Vector

def sensor_dims(cam, rx, ry):
    d = cam.data
    if d.sensor_fit == 'AUTO':
        if rx >= ry:
            return d.sensor_width, d.sensor_width * ry / rx
        return d.sensor_width * rx / ry, d.sensor_width
    if d.sensor_fit == 'HORIZONTAL':
        return d.sensor_width, d.sensor_width * ry / rx
    return d.sensor_height * rx / ry, d.sensor_height

def coverage(cam, scene, point):
    rx, ry = scene.render.resolution_x, scene.render.resolution_y
    sw, sh = sensor_dims(cam, rx, ry)
    view = cam.matrix_world.to_quaternion() @ Vector((0, 0, -1))
    dist = (Vector(point) - cam.location).dot(view)
    return dist * sw / cam.data.lens, dist * sh / cam.data.lens, dist

# v23 example: portrait 1440x1800, 72 mm, subject plane ~3.48 m away
# vertical sensor 36 mm -> vertical coverage = 3.48 * 36 / 72 = 1.74 m
# aim height 1.12 m -> frame spans 0.25 m to 1.99 m, so feet are cropped by design
```

For a full body of height `H` with 8% top margin and 5% bottom margin, require:

```
vertical_coverage >= H * 1.13
```

At `H = 1.70 m`, need ≥1.92 m. For 44 mm landscape (vertical sensor 20.25 mm), distance must be ≥ 1.92 * 44 / 20.25 = 4.17 m. That is why the gothic full-body used 44 mm at 4.15–4.5 m.

Frustum check for any prop or flower:

```python
from bpy_extras.object_utils import world_to_camera_view

def in_frame(scene, cam, obj, margin=0.03):
    co = world_to_camera_view(scene, cam, obj.matrix_world.translation)
    return margin <= co.x <= 1 - margin and margin <= co.y <= 1 - margin and co.z > 0
```

Check the object's bounding-box corners, not just its origin. For clusters, check every flower head.

## 6. Focus on the eye

1. Find the eye mesh/material (names often contain `目`, `eye`, `iris`, `瞳`).
2. Evaluate the mesh with modifiers applied (`object.evaluated_get(depsgraph)`).
3. Transform vertices to world space; choose the vertex closest to the camera among vertices in the eye region, or the frontmost point along the camera axis.
4. Put the Focus empty at that world point minus a tiny offset toward the camera (1–3 mm).
5. Set `camera.data.dof.focus_object = focus_empty`, f-stop per framing.
6. Render a close crop of the face to confirm the iris is sharp and the ear is soft.

Do not use the head bone origin; it sits inside the skull and often focuses behind the eyes. In v23 the focus point was `(0.045, 0.285, 1.492)`, measured from the eye mesh, not a guessed height.

## 7. Iteration protocol

1. **Save before render.** `versions/vNN_scene.blend` with the next number; never overwrite.
2. **State the goal** in one line (e.g. “reduce skin clipping without losing rim”).
3. **Change one variable group**: exposure+key power; fill+rim ratio; fog density+bounds; camera+focus; one prop's material. Do not change composition and grading in the same version.
4. **Render preview** at 1152×1440 / 64 (portrait) or 1280×720 / 64 (wide), 100% resolution.
5. **Inspect** the full image, then a 1:1 face crop, then the feet/hands crop.
6. **Write the version row**: number, time, resolution/samples, change, result, decision.
7. **Keep even rejected versions.** Mark them “rejected/experiment”, never delete. A rejected version is evidence of what not to do.
8. **Revert by opening the best saved blend**, not by undoing edits in memory.
9. **Stop** when: silhouette reads, skin highlights retain detail, eyes are sharp, framing is intentional, no artifact draws the eye, and the set supports rather than competes. Then do the final-quality render.

Version log row template:

```
| v07 | 13:02 | 1600x900 / 64 | fog box 5.6→7.1 m, glass removed, painting matte | moon/window artifacts gone; floor shadow soft | keep |
```

## 8. Comparison and contact sheets

- Render all versions from the same camera and crop; otherwise the contact sheet lies.
- Use the same output size for previews; label each cell with the version.
- Put the best version first or mark it; keep rejected versions visible.
- Compare at thumbnail size for composition/value, then at 100% for skin/eyes/artifacts.
- For reference matching, crop the reference to the same head size and compare: background value, skin value, hair gradient, rim color, contrast, highlight shape.

## 9. Delivery checks

- Pack all textures; zero missing; relative render path (`//renders/...`).
- Confirm camera, resolution, resolution percentage 100%, samples, exposure, engine.
- Render the final image from the packed blend once, to prove the packed file works.
- Keep the matching `.blend` next to the final image; name them with the same version.
- Back up the packed blend + renders + version log + scripts; record the archive size/hash if useful.
- Respect the model license: local-only if redistribution is forbidden.

## 10. Blender 4.2+ notes

- **Bloom removed** from EEVEE Next; use compositor Glare (Fog Glow or Bloom). Re-tune threshold/size/mix.
- **Light units and shadows** changed; a 3.6 wattage table is only a starting point.
- **Volumetrics** are configured differently and are more expensive; verify density/samples.
- **SSR/refraction** behavior differs; glossy floors and mirrors may need roughness changes.
- **MMD Tools/PMX import** compatibility varies; test import and material alpha before building.
- If a 3.6 look must be reproduced exactly, use Blender 3.6.14 rather than chasing EEVEE Next.
