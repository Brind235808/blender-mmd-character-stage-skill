"""Verify packed textures, relative output path, camera, and resolution.

Usage:
  blender.exe -b --python verify_pack.py -- --blend "a.blend" [--blend "b.blend"] \
      [--expect-width 1440 --expect-height 1800]

Exit code is 0 only when every file passes. Each file prints one VERIFY line.
"""

import argparse
import os
import sys

import bpy


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser(description="Verify a portable staged .blend.")
    parser.add_argument("--blend", action="append", required=True, help="Repeat for multiple files")
    parser.add_argument("--expect-width", type=int, default=None)
    parser.add_argument("--expect-height", type=int, default=None)
    return parser.parse_args(argv)


def main():
    args = parse_args()
    failures = 0

    for name in args.blend:
        path = os.path.abspath(name)
        if not os.path.isfile(path):
            print("VERIFY|{}|FAIL|missing_file".format(path))
            failures += 1
            continue

        bpy.ops.wm.open_mainfile(filepath=path, load_ui=False)
        scene = bpy.context.scene
        render = scene.render
        camera = scene.camera

        file_images = [image for image in bpy.data.images if image.source == "FILE"]
        missing = [image for image in file_images if not image.packed_file]
        packed = sum(1 for image in file_images if image.packed_file)
        relative = render.filepath.startswith("//")
        percent = render.resolution_percentage
        has_resolution = render.resolution_x > 0 and render.resolution_y > 0
        output_dir = ""
        if relative:
            output_dir = os.path.dirname(os.path.join(os.path.dirname(path), render.filepath[2:]))
        dir_exists = bool(output_dir) and os.path.isdir(output_dir)

        problems = []
        if missing:
            problems.append("missing_images={}".format(len(missing)))
        if camera is None:
            problems.append("no_camera")
        if not relative:
            problems.append("absolute_output_path")
        if not has_resolution:
            problems.append("no_resolution")
        if percent != 100:
            problems.append("resolution_percent={}".format(percent))
        if args.expect_width is not None and render.resolution_x != args.expect_width:
            problems.append("width={}".format(render.resolution_x))
        if args.expect_height is not None and render.resolution_y != args.expect_height:
            problems.append("height={}".format(render.resolution_y))

        status = "PASS" if not problems else "FAIL"
        if problems:
            failures += 1
        print("VERIFY|{}|{}|missing={}|packed={}|camera={}|res={}x{}@{}%|output={}|dir_exists={}|size={:.1f}MB|problems={}".format(
            path, status, len(missing), packed,
            camera.name if camera else "NONE",
            render.resolution_x, render.resolution_y, percent,
            render.filepath, dir_exists, os.path.getsize(path) / 1048576.0,
            ",".join(problems) if problems else "-"))
        for image in missing[:20]:
            print("MISSING|{}|{}".format(image.name, image.filepath))
        if len(missing) > 20:
            print("MISSING_MORE|{}".format(len(missing) - 20))

    if failures:
        print("VERIFY_FAIL|{}".format(failures))
        sys.stdout.flush()
        sys.exit(1)
    print("VERIFY_OK|{}".format(len(args.blend)))


if __name__ == "__main__":
    main()
