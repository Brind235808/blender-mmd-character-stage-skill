"""Build a labeled contact sheet from render previews (system Python + Pillow).

Usage:
  python contact_sheet.py renders/v01_preview.png renders/v02_preview.png \
      --out renders/contact_sheet.jpg --cols 4 --title "Scene versions" --best v11

Accepts files, glob patterns, and directories. Images are fitted into cells
without cropping. Ends with CONTACT_SHEET_OK.
"""

import argparse
import glob
import os
import sys
from math import ceil

from PIL import Image, ImageDraw, ImageFont, ImageOps


def parse_args():
    parser = argparse.ArgumentParser(description="Build a labeled version contact sheet.")
    parser.add_argument("inputs", nargs="+", help="Images, glob patterns, or directories")
    parser.add_argument("--out", required=True)
    parser.add_argument("--cols", type=int, default=4)
    parser.add_argument("--cell-width", type=int, default=400)
    parser.add_argument("--cell-height", type=int, default=500)
    parser.add_argument("--title", default="")
    parser.add_argument("--best", default=None, help="Substring of the best version label")
    parser.add_argument("--label-height", type=int, default=30)
    parser.add_argument("--title-height", type=int, default=56)
    return parser.parse_args()


def expand_inputs(inputs):
    files = []
    for item in inputs:
        if os.path.isdir(item):
            for ext in ("png", "jpg", "jpeg", "webp", "bmp"):
                files.extend(glob.glob(os.path.join(item, "*." + ext)))
                files.extend(glob.glob(os.path.join(item, "*." + ext.upper())))
        elif any(char in item for char in "*?["):
            files.extend(glob.glob(item))
        else:
            files.append(item)
    seen = set()
    unique = []
    for path in sorted(files, key=lambda value: os.path.basename(value).lower()):
        key = os.path.abspath(path).lower()
        if os.path.isfile(path) and key not in seen:
            seen.add(key)
            unique.append(path)
    return unique


def load_font(size, bold=False):
    candidates = [
        r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\seguisb.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if os.path.isfile(candidate):
            try:
                return ImageFont.truetype(candidate, size)
            except OSError:
                continue
    return ImageFont.load_default()


def fit_image(image, width, height):
    image = ImageOps.exif_transpose(image).convert("RGB")
    scale = min(width / image.width, height / image.height)
    size = (max(1, int(image.width * scale)), max(1, int(image.height * scale)))
    return image.resize(size, Image.Resampling.LANCZOS)


def label_for(path):
    return os.path.splitext(os.path.basename(path))[0].replace("_preview", "")


def main():
    args = parse_args()
    files = expand_inputs(args.inputs)
    if not files:
        print("CONTACT_SHEET_FAIL|no images")
        sys.exit(2)
    if args.cols < 1:
        print("CONTACT_SHEET_FAIL|cols must be >= 1")
        sys.exit(2)

    cell_w = args.cell_width
    cell_h = args.cell_height
    label_h = args.label_height
    title_h = args.title_height if args.title else 0
    cols = args.cols
    rows = ceil(len(files) / cols)

    width = cols * cell_w
    height = title_h + rows * (cell_h + label_h)
    sheet = Image.new("RGB", (width, height), (14, 14, 18))
    draw = ImageDraw.Draw(sheet)

    title_font = load_font(30, bold=True)
    label_font = load_font(19, bold=False)
    best_font = load_font(17, bold=True)

    if args.title:
        draw.text((22, 14), args.title, font=title_font, fill=(232, 232, 238))

    for index, path in enumerate(files):
        row, col = divmod(index, cols)
        left = col * cell_w
        top = title_h + row * (cell_h + label_h)
        draw.rectangle([left + 3, top + 3, left + cell_w - 4, top + cell_h + label_h - 3],
                       fill=(24, 24, 30), outline=(52, 52, 62), width=1)
        try:
            with Image.open(path) as handle:
                thumb = fit_image(handle, cell_w - 16, cell_h - 16)
        except Exception as error:
            draw.text((left + 12, top + 12), "LOAD FAILED", font=label_font, fill=(240, 90, 90))
            draw.text((left + 12, top + 42), str(error)[:48], font=label_font, fill=(200, 120, 120))
            continue

        x = left + (cell_w - thumb.width) // 2
        y = top + (cell_h - thumb.height) // 2
        sheet.paste(thumb, (x, y))

        label = label_for(path)
        is_best = bool(args.best) and args.best.lower() in label.lower()
        if is_best:
            draw.rectangle([left + 3, top + 3, left + cell_w - 4, top + cell_h + label_h - 3],
                           outline=(224, 180, 92), width=3)
            draw.rectangle([left + cell_w - 66, top + 9, left + cell_w - 9, top + 35],
                           fill=(224, 180, 92))
            draw.text((left + cell_w - 58, top + 12), "BEST", font=best_font, fill=(20, 20, 20))

        bbox = draw.textbbox((0, 0), label, font=label_font)
        text_w = bbox[2] - bbox[0]
        draw.text((left + (cell_w - text_w) // 2, top + cell_h + 4), label,
                  font=label_font, fill=(228, 228, 235) if not is_best else (238, 200, 120))

    output = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(output), exist_ok=True)
    if output.lower().endswith((".jpg", ".jpeg")):
        sheet.save(output, quality=92, subsampling=0)
    else:
        sheet.save(output)
    print("CONTACT_SHEET_OK|{}|{}|{}x{}".format(output, len(files), sheet.width, sheet.height))


if __name__ == "__main__":
    main()
