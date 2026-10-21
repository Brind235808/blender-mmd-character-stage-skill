"""Headless scene inspection for staged Blender files.

Usage:
  blender.exe -b --python inspect_blend.py -- --blend "path/to/scene.blend"

Prints one record per line, prefixed with a tag, and ends with INSPECT_OK.
No scene changes are saved.
"""

import argparse
import os
import re
import sys

import bpy
from mathutils import Vector


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser(description="Dump scene, camera, lights, textures, and pack status.")
    parser.add_argument("--blend", required=True, help="Path to a .blend file")
    return parser.parse_args(argv)


def vec(value, digits=3):
    return tuple(round(float(v), digits) for v in value)


def sensor_dims(cam, res_x, res_y):
    data = cam.data
    if data.sensor_fit == "AUTO":
        if res_x >= res_y:
            return data.sensor_width, data.sensor_width * res_y / res_x
        return data.sensor_width * res_x / res_y, data.sensor_width
    if data.sensor_fit == "HORIZONTAL":
        return data.sensor_width, data.sensor_width * res_y / res_x
    return data.sensor_height * res_x / res_y, data.sensor_height


def find_background(world):
    if not world or not world.use_nodes or not world.node_tree:
        return None
    return next((node for node in world.node_tree.nodes if node.type == "BACKGROUND"), None)


def image_source(node):
    for link in node.inputs["Color"].links:
        source = link.from_node
        if source.type == "TEX_ENVIRONMENT" and source.image:
            return source.image.filepath or source.image.name
        for nested in source.inputs:
            for nested_link in nested.links:
                inner = nested_link.from_node
                if inner.type == "TEX_ENVIRONMENT" and inner.image:
                    return inner.image.filepath or inner.image.name
    return None


def main():
    args = parse_args()
    path = os.path.abspath(args.blend)
    if not os.path.isfile(path):
        print("INSPECT_FAIL|missing_file|" + path)
        sys.exit(2)

    bpy.ops.wm.open_mainfile(filepath=path, load_ui=False)
    scene = bpy.context.scene
    size_mb = os.path.getsize(path) / 1048576.0
    print("INSPECT_BEGIN|{}|{:.1f}MB|Blender {}".format(path, size_mb, bpy.app.version_string))

    render = scene.render
    eevee = getattr(scene, "eevee", None)
    print("SCENE|engine={}|frame={}|res={}x{}|percent={}|filepath={}|format={}|compositor={}".format(
        render.engine, scene.frame_current, render.resolution_x, render.resolution_y,
        render.resolution_percentage, render.filepath,
        render.image_settings.file_format, scene.use_nodes))
    print("COLOR|view={}|look={}|exposure={}|gamma={}|display={}".format(
        scene.view_settings.view_transform, scene.view_settings.look,
        round(scene.view_settings.exposure, 3), round(scene.view_settings.gamma, 3),
        scene.display_settings.display_device))
    if eevee:
        print("EEVEE|taa={}|vol_samples={}|vol_start={}|vol_end={}|gtao={}|ssr={}|soft_shadows={}|bloom={}".format(
            getattr(eevee, "taa_render_samples", "?"),
            getattr(eevee, "volumetric_samples", "?"),
            getattr(eevee, "volumetric_start", "?"),
            getattr(eevee, "volumetric_end", "?"),
            getattr(eevee, "use_gtao", "?"),
            getattr(eevee, "use_ssr", "?"),
            getattr(eevee, "use_soft_shadows", "?"),
            getattr(eevee, "use_bloom", "?")))
        if getattr(eevee, "use_bloom", False):
            print("BLOOM|threshold={}|radius={}|intensity={}".format(
                round(eevee.bloom_threshold, 3), round(eevee.bloom_radius, 3),
                round(eevee.bloom_intensity, 4)))

    cam = scene.camera
    if cam is None:
        print("CAMERA|NONE")
    else:
        focus = cam.data.dof.focus_object if cam.data.dof.use_dof else None
        forward = cam.matrix_world.to_quaternion() @ Vector((0.0, 0.0, -1.0))
        target = cam.location + forward * 3.0
        print("CAMERA|name={}|loc={}|forward={}|target3m={}|sensor={}x{}|fit={}|lens={}|fstop={}|dof={}".format(
            cam.name, vec(cam.location), vec(forward), vec(target),
            round(cam.data.sensor_width, 2), round(cam.data.sensor_height, 2),
            cam.data.sensor_fit, round(cam.data.lens, 2),
            round(cam.data.dof.aperture_fstop, 2), cam.data.dof.use_dof))
        if focus:
            print("FOCUS|{}|{}".format(focus.name, vec(focus.matrix_world.translation)))
            point = focus.matrix_world.translation
        else:
            print("FOCUS|NONE|focus_distance={}".format(round(cam.data.dof.focus_distance, 3)))
            point = target
        sensor_w, sensor_h = sensor_dims(cam, render.resolution_x, render.resolution_y)
        distance = (Vector(point) - cam.location).dot(forward)
        if distance > 0:
            print("COVERAGE|distance={:.2f}m|horizontal={:.2f}m|vertical={:.2f}m|sensor_h={:.2f}mm".format(
                distance, distance * sensor_w / cam.data.lens,
                distance * sensor_h / cam.data.lens, sensor_h))

    world = scene.world
    background = find_background(world)
    if background is None:
        print("WORLD|nodes={}|background=NONE".format(bool(world and world.use_nodes)))
    else:
        print("WORLD|color={}|strength={}|hdr={}".format(
            vec(background.inputs["Color"].default_value, 4),
            round(background.inputs["Strength"].default_value, 4),
            image_source(background) or "-"))

    lights = sorted((obj for obj in scene.objects if obj.type == "LIGHT"), key=lambda obj: obj.name.lower())
    print("LIGHTS|count={}".format(len(lights)))
    for obj in lights:
        light = obj.data
        extra = ""
        if light.type == "AREA":
            extra = "size={:.3f},shape={}".format(light.size, light.shape)
        elif light.type == "SPOT":
            extra = "spot={:.1f},blend={:.2f},size={:.3f}".format(
                light.spot_size, light.spot_blend, light.shadow_soft_size)
        elif light.type == "POINT":
            extra = "radius={:.3f}".format(light.shadow_soft_size)
        print("LIGHT|{}|{}|{:.2f}W|{}|{}|{}|shadow={},contact={},spec={:.2f}".format(
            obj.name, light.type, light.energy, vec(light.color), vec(obj.location), extra,
            light.use_shadow, getattr(light, "use_contact_shadow", "?"),
            getattr(light, "specular_factor", -1.0)))
        if obj.hide_render:
            print("LIGHT_HIDDEN|{}".format(obj.name))

    meshes = [obj for obj in scene.objects if obj.type == "MESH"]
    hidden_meshes = sorted((obj.name for obj in meshes if obj.hide_render), key=str.lower)
    print("MESHES|count={}|hidden_render={}|vertices={}".format(
        len(meshes), len(hidden_meshes),
        sum(len(obj.data.vertices) for obj in meshes if obj.data)))
    groups = {}
    singles = []
    for name in hidden_meshes:
        prefix = re.sub(r"[ ._-]*\d+$", "", name)
        if prefix != name:
            groups[prefix] = groups.get(prefix, 0) + 1
        else:
            singles.append(name)
    for prefix, count in sorted(groups.items(), key=lambda item: item[0].lower()):
        print("HIDDEN_GROUP|{}|{}".format(prefix, count))
    for name in singles[:40]:
        print("HIDDEN|{}".format(name))
    if len(singles) > 40:
        print("HIDDEN_MORE|{}".format(len(singles) - 40))
    for obj in sorted(meshes, key=lambda item: item.name.lower()):
        lowered = obj.name.lower()
        if "fog" in lowered or "volume" in lowered or "atmos" in lowered:
            print("FOG|{}|hide_render={}".format(obj.name, obj.hide_render))

    file_images = [image for image in bpy.data.images if image.source == "FILE"]
    missing = [image for image in file_images if not image.packed_file]
    packed = sum(1 for image in file_images if image.packed_file)
    print("IMAGES|file={}|packed={}|missing={}|generated={}".format(
        len(file_images), packed, len(missing),
        sum(1 for image in bpy.data.images if image.source == "GENERATED")))
    for image in missing[:20]:
        print("MISSING|{}|{}".format(image.name, image.filepath))
    if len(missing) > 20:
        print("MISSING_MORE|{}".format(len(missing) - 20))

    print("MATERIALS|count={}".format(len(bpy.data.materials)))
    print("COLLECTIONS|count={}".format(len(scene.collection.children_recursive) + 1))
    print("INSPECT_OK")


if __name__ == "__main__":
    main()
