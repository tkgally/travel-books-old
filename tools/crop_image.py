#!/usr/bin/env python3
"""Crop an illustration from a full-size leaf image into the book's images directory.

  crop_image.py FULL_LEAF.jpg OUT.jpg x0,y0,x1,y1 [--max N] [--gray] [--rotate 90|180|270]
  crop_image.py --shrink IMAGE.jpg ...      re-encode existing pictures in place within the limits below
The box is in fractions of the leaf (0-1), as the leaf is scanned: work it out on the small page image, then LOOK
at the result. A plate printed sideways is turned upright after cropping: --rotate N turns it N degrees
counter-clockwise (caption reading bottom to top along the right edge: 270; top to bottom along the left: 90).
Longest side at most MAX pixels, JPEG quality QUALITY (Tom, 2026-11-23: the site and the repository must stay small;
the test ImageLimits refuses larger files in books/ and wip/). Naming: images/pNNNN-k.jpg = k-th [[image:]] on leaf pNNNN;
images/cover.jpg = the front cover if the title is clearly readable on it, otherwise the title page (notes/workflow.md §5).
"""
import argparse
from PIL import Image, ImageOps

MAX, QUALITY = 1000, 75
ROTATE = {0: None, 90: Image.Transpose.ROTATE_90, 180: Image.Transpose.ROTATE_180, 270: Image.Transpose.ROTATE_270}


def crop(im, box, gray=False, rotate=0, longest=MAX):
    """Crop box (fractions of the leaf), optionally greyscale, turn upright, reduce: returns a new image."""
    x0, y0, x1, y1 = box
    im = im.crop((int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height)))
    im = ImageOps.autocontrast(im.convert("L"), cutoff=1) if gray else im.convert("RGB")
    if ROTATE[rotate] is not None:
        im = im.transpose(ROTATE[rotate])
    im.thumbnail((longest, longest), Image.LANCZOS)
    return im


def save(im, path):
    """Write a picture as the books keep them: JPEG at QUALITY, optimized, colour profile kept."""
    icc = im.info.get("icc_profile")
    im.save(path, "JPEG", quality=QUALITY, optimize=True, **({"icc_profile": icc} if icc else {}))


def shrink(path):
    """Reduce an existing picture in place to the limits (longest side MAX, quality QUALITY); returns (before, after) bytes."""
    import os
    before = os.path.getsize(path)
    im = Image.open(path)
    im.load()
    if im.mode not in ("L", "RGB"):
        im = im.convert("RGB")
    im.thumbnail((MAX, MAX), Image.LANCZOS)
    save(im, path)
    return before, os.path.getsize(path)


def within_limits(path):
    """None if the picture is within the limits, else what is wrong."""
    im = Image.open(path)
    if max(im.size) > MAX:
        return f"{max(im.size)} px on its longest side (at most {MAX})"
    q = getattr(im, "quantization", None)
    if im.format != "JPEG" or not q:
        return "not a JPEG"
    if sum(q[0]) < sum(_reference_table()):
        return f"JPEG quality above {QUALITY}"
    return None


_REF = []


def _reference_table():
    """The luminance quantization table that Pillow writes at QUALITY (a smaller sum means a higher quality)."""
    if not _REF:
        import io
        b = io.BytesIO()
        Image.new("L", (8, 8)).save(b, "JPEG", quality=QUALITY)
        _REF.append(Image.open(io.BytesIO(b.getvalue())).quantization[0])
    return _REF[0]


def main():
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--shrink":
        tb = ta = 0
        for p in sys.argv[2:]:
            b, a = shrink(p)
            tb += b; ta += a
        print(f"{len(sys.argv) - 2} pictures: {tb / 1e6:.1f} MB -> {ta / 1e6:.1f} MB")
        return
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out"); ap.add_argument("box")
    ap.add_argument("--max", type=int, default=MAX, help=f"longest side in pixels (ornaments: 600); never more than {MAX}")
    ap.add_argument("--gray", action="store_true", help="engravings and line drawings: greyscale with contrast stretched")
    ap.add_argument("--rotate", type=int, default=0, choices=sorted(ROTATE),
                    help="degrees counter-clockwise, to turn a plate printed sideways upright")
    a = ap.parse_args()
    box = tuple(float(v) for v in a.box.split(","))
    im = crop(Image.open(a.src), box, gray=a.gray, rotate=a.rotate, longest=min(a.max, MAX))
    save(im, a.out)
    print(a.out, im.size)


if __name__ == "__main__":
    main()
