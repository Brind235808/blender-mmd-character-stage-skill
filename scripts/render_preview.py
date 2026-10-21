"""Headless preview render with optional diagnostics.

Usage:
  blender.exe -b --python render_preview.py -- --blend "scene.blend" --out "preview.png" \
      --width 960 --height 1200 --samples 64

Flags:
  --raw       disable the compositor (lighting-only diagnostic)
  --no-fog    hide render for mesh objects named fog/volume/atmos
  --no-bloom  disable EEVEE bloom for this render
  --percent   resolution percentage, default 100

The .blend is never saved. Output is written to --out; relative paths are
resolved against the .blend directory.
"""

import argparse
import os
import sys
import time

import bpy


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser(description="Render a preview from a staged .blend.")
    parser.add_argument("--blend", required=True)
    parser.add_argument("--out", default=None, help="Output PNG path; default <blend_dir>/preview.png")
    parser.add_argument("--width", type=int, default=None)
    parser.add_argument("--height", type=int, default=None)
    parser.add_argument("--samples", type=int, default=None)
    parser.add_argument("--percent", type=int, default=100)
    parser.add_argument("--raw", action="store_true", help="Disable the compositor")
    parser.add_argument("--no-fog", action="store_true", help="Hide fog/volume objects")
    parser.add_argument("--no-bloom", action="store_true", help="Disable EEVEE bloom")
    return parser.parse_args(argv)


def main():
    args = parse_args()
    blend = os.path.abspath(args.blend)
    if not os.path.isfile(blend):
        print("PREVIEW_FAIL|missing_blend|" + blend)
        sys.exit(2)

    bpy.ops.wm.open_mainfile(filepath=blend, load_ui=False)
    scene = bpy.context.scene
    render = scene.render

    if args.width:
        render.resolution_x = args.width
    if args.height:
        render.resolution_y = args.height
    render.resolution_percentage = args.percent

    eevee = getattr(scene, "eevee", None)
    if args.samples and eevee and hasattr(eevee, "taa_render_samples"):
        eevee.taa_render_samples = args.samples
    if args.no_bloom and eevee and hasattr(eevee, "use_bloom"):
        eevee.use_bloom = False

    if args.raw:
        scene.use_nodes = False

    hidden = []
    if args.no_fog:
        for obj in scene.objects:
            if obj.type != "MESH":
                continue
            lowered = obj.name.lower()
            if "fog" in lowered or "volume" in lowered or "atmos" in lowered:
                obj.hide_render = True
                hidden.append(obj.name)

    if args.out:
        output = args.out
        if not os.path.isabs(output):
            output = os.path.join(os.path.dirname(blend), output)
    else:
        output = os.path.join(os.path.dirname(blend), "preview.png")
    output = os.path.abspath(output)
    os.makedirs(os.path.dirname(output), exist_ok=True)

    render.filepath = output
    render.image_settings.file_format = "PNG"
    render.image_settings.color_mode = "RGB"
    render.image_settings.color_depth = "8"

    samples = getattr(eevee, "taa_render_samples", "?") if eevee else "?"
    print("PREVIEW_START|blend={}|out={}|res={}x{}@{}%|samples={}|raw={}|no_fog={}|no_bloom={}|fog_hidden={}".format(
        blend, output, render.resolution_x, render.resolution_y, render.resolution_percentage,
        samples, args.raw, args.no_fog, args.no_bloom, len(hidden)))

    started = time.time()
    bpy.ops.render.render(write_still=True)
    elapsed = time.time() - started
    print("PREVIEW_OK|{}|{}x{}|{:.1f}s|{:.1f}MB".format(
        output, render.resolution_x, render.resolution_y, elapsed,
        os.path.getsize(output) / 1048576.0 if os.path.isfile(output) else 0.0))


if __name__ == "__main__":
    main()
