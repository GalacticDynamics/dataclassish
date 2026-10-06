# /// script
# requires-python = ">=3.11"
# dependencies = ["resvg-py"]
# ///
"""Copyright (c) 2024 Nathaniel Starkman. All rights reserved.

Draw the dataclassish logo: structured data, approximately.

A brace opening a record of fields, each a key dot and a wavy tilde for its
value, beside a plain box: fields for any object, not only a dataclass, and the
tildes for the "-ish". The shapes are vector, so the logo is written as an SVG,
sharp at any size; for a bitmap, name a .png and give its size::

    uv run docs/_static/make_logo.py                     # favicon.svg
    uv run docs/_static/make_logo.py --size 2048 big.png
"""

import argparse
from pathlib import Path

NAVY, TEAL, PURPLE = "#030a23", "#66a19a", "#7738eb"  # GalacticDynamics' colours

# In a 64-unit square. The brace: its ends' x, its top and bottom, and its depth.
BRACE = (13, 13, 51, 3.2)
# The fields: the key dots' x, the first row's y, the rows' spacing, and each
# row's tilde length.
FIELDS = (19, 22.5, 9.5, (18, 16, 14))
BOX = (47, 13, 12, 38)  # x, y, width, height

SVG = """\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="512" height="512">
  <g fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="{brace}" stroke="{purple}" stroke-width="4"/>
{tildes}
    <rect x="{bx:g}" y="{by:g}" width="{bw:g}" height="{bh:g}" rx="4"
      stroke="{navy}" stroke-width="3"/>
  </g>
{dots}
</svg>
"""


def brace() -> str:
    """Return the brace as an SVG path: ends at the right, its point at left."""
    x, top, bottom, w = BRACE
    h, mid = bottom - top, (top + bottom) / 2
    # The brace's back, its point, and where its curves pull in to the point.
    back, tip, neck = x - w, x - 2.2 * w, x - 1.8 * w
    return (
        f"M{x:g} {top:g}"
        f"C{back:g} {top:g} {back:g} {top + 0.08 * h:g} {back:g} {top + 0.2 * h:g}"
        f"V{mid - 0.12 * h:g}"
        f"C{back:g} {mid - 0.03 * h:g} {neck:g} {mid:g} {tip:g} {mid:g}"
        f"C{neck:g} {mid:g} {back:g} {mid + 0.03 * h:g} {back:g} {mid + 0.12 * h:g}"
        f"V{bottom - 0.2 * h:g}"
        f"C{back:g} {bottom - 0.08 * h:g} {back:g} {bottom:g} {x:g} {bottom:g}"
    )


def tilde(x: float, y: float, length: float) -> str:
    """Return a tilde of ``length`` starting at ``x``, ``y``: a hump, a dip."""
    quarter, rise = length / 4, 0.32 * length
    return f"M{x:g} {y:g}q{quarter:g} {-rise:g} {2 * quarter:g} 0t{2 * quarter:g} 0"


def svg() -> str:
    """Return the logo as SVG text."""
    x, y0, spacing, lengths = FIELDS
    rows = [(y0 + i * spacing, length) for i, length in enumerate(lengths)]
    tildes = "\n".join(
        f'    <path d="{tilde(x + 5.5, y, length)}" stroke="{TEAL}"'
        ' stroke-width="3.6"/>'
        for y, length in rows
    )
    dots = "\n".join(
        f'  <circle cx="{x:g}" cy="{y:g}" r="2.7" fill="{PURPLE}"/>' for y, _ in rows
    )
    bx, by, bw, bh = BOX
    return SVG.format(
        brace=brace(),
        tildes=tildes,
        dots=dots,
        purple=PURPLE,
        navy=NAVY,
        bx=bx,
        by=by,
        bw=bw,
        bh=bh,
    )


def main() -> None:
    """Parse the command line and save the logo."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument(
        "out",
        nargs="?",
        type=Path,
        default=Path(__file__).with_name("favicon.svg"),
        help="output file, SVG or PNG by its extension (default: favicon.svg)",
    )
    parser.add_argument(
        "--size", type=int, default=512, help="pixels per side, for a PNG"
    )
    args = parser.parse_args()

    if args.out.suffix == ".svg":
        args.out.write_text(svg())
    else:
        import resvg_py  # noqa: PLC0415  # only a PNG needs a renderer

        png = resvg_py.svg_to_bytes(svg_string=svg(), width=args.size)
        args.out.write_bytes(bytes(png))


if __name__ == "__main__":
    main()
