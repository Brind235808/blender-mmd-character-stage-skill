# Character Prep

Import, measure, ground, and pose the character before building the set. This is staging, **not** shader authoring: keep the model's materials as imported. If the character's shading looks wrong, note it as a separate task; do not rebuild its shader inside a scene build.

## 1. Import

- **PMX (MMD):** enable MMD Tools, then import at the scale that puts the character in meters. In this pipeline the working call is:

```python
bpy.ops.mmd_tools.import_model(
    filepath=PMX_PATH,
    scale=0.08,
    types={"MESH", "ARMATURE", "MORPHS"},
)
```

- **FBX/GLB:** use Blender's importer. Check up-axis and forward axis (a GLB may arrive Y-up and face the wrong way); rotate the root, not the mesh data.
- Import into an empty scene or a dedicated `Character` collection.
- Keep the original object, bone, material, and shape-key names. They are often referenced by MMD tools and by the model's morphs.
- Do not run `Unpack Resources` or delete textures. If materials are pink, fix the image paths, not the shader.

## 2. Measure, scale, ground

Measure the **world bounding box of all character meshes**, not the armature origin. Imported PMX models are often 0.08 scale and can be a few centimeters off the floor.

```python
from mathutils import Vector

def bounds(objects):
    points = []
    for obj in objects:
        if obj.type != "MESH":
            continue
        points.extend(obj.matrix_world @ Vector(corner) for corner in obj.bound_box)
    xs = [p.x for p in points]
    ys = [p.y for p in points]
    zs = [p.z for p in points]
    return (min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))

meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
low, high = bounds(meshes)
height = high[2] - low[2]
print("CHAR_HEIGHT", height, "FEET_Z", low[2])
```

Target height **1.60–1.75 m**. Scale the armature/root object uniformly by `1.65 / height`, then re-measure. Do not apply scale to a skinned mesh unless the armature is handled too; add a tiny floor offset so the lowest point sits at `z ≈ 0.02`, and put the contact-shadow plane at `z ≈ 0.024`.

Check facing: the camera usually sits on `-Y`; the character should face `-Y` (toward the camera). If the back is to the camera, rotate the root 180° around Z.

## 3. Pose and expression

- Use the imported rest pose or a simple static pose. This skill is for stills, not animation.
- Small arm/wrist/head changes are fine, but verify hands against the skirt/body. A wrist target that pulls the hand away from the sleeve creates a floating hand; revert instead of forcing it.
- Use existing shape keys for a subtle expression if available; keep it tasteful.
- If the model has adult/BDSM add-ons, hide them: `Alpha = 0` on those materials and/or `hide_render` on their objects. Do not delete the data; it stays local for license compliance.
- Do not copy explicit poses from reference images. Replicate lighting, framing, and stage language only.

## 4. Eye focus point

The camera focus must sit on the **frontmost eye surface**, not the head-bone origin.

1. Find eye meshes/materials by name (`目`, `eye`, `iris`, `瞳`, `pupil`) or by inspecting the face.
2. Evaluate the mesh with modifiers applied:

```python
depsgraph = bpy.context.evaluated_depsgraph_get()
evaluated = eye_object.evaluated_get(depsgraph)
mesh = evaluated.to_mesh()
points = [evaluated.matrix_world @ vertex.co for vertex in mesh.vertices]
evaluated.to_mesh_clear()
```

3. Choose the point closest to the camera along the view axis, or the frontmost vertex in the eye region. In the v23 stage the measured point was `(0.045, 0.285, 1.492)` for a 1.65 m character, with the camera on `-Y`.
4. Create an empty at that point and assign `camera.data.dof.focus_object = empty`.
5. Verify with a face crop at f/2.0–f/2.8: iris sharp, ear soft. If the eyes are soft, the focus point is behind the face.

## 5. Neutral lookdev pass (optional)

If the character's palette is unclear from the files, render one neutral pass before choosing a scene:

- Gray world (0.05–0.1), two large area lights (key front-left, fill front-right at 1/4), no fog, no compositor grade.
- 512 × 640, 32–64 samples, 65–85 mm, f/2.8.
- Read hair/eye/outfit colors, material types, silhouette, and which parts catch light.
- Do not number this as a scene version; it is a style reference. Remove the temporary lights before building.

## 6. Character collection and license

- Keep all character objects in one `Character` collection; the set goes in `Set`, props in `Props`, lights in `Lights`, atmosphere in `FX`.
- Do not rename internal character objects or bones; scene scripts and morphs may depend on them.
- If the model readme forbids redistribution, the final `.blend` (which contains mesh and textures) is local-only. State this in the delivery note and never upload it publicly.
- Pack textures only at delivery, after the scene is final; packing early makes iteration files unnecessarily large.

## 7. Quick checks

| Check | Expected | If not |
|---|---|---|
| Character height | 1.60–1.75 m | Scale the armature/root, re-measure |
| Lowest point | `z ≈ 0.02` | Move the root up/down; add contact shadow at 0.024 |
| Facing | Toward camera (`-Y` by default) | Rotate root 180° |
| Materials | As imported, textures found | Fix image paths; do not re-author shader |
| Adult add-ons | Hidden, data intact | Alpha 0 / hide_render |
| Eye focus | On eye surface | Move focus empty; verify with a face crop |
| Hands | Connected and natural | Revert the pose change; keep the best saved version |
| Imported animation | None or intentional | Clear actions/NLA if the rest pose is wrong |
