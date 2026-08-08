"""Generate hover-colored copies of the map and arrow images.

Each source color is swapped for its hover counterpart; the resulting
`*_hover.png` files are used as overlays by the site's hover effect.
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image

COLOR_SWAPS = {
    (0xFF, 0xF4, 0xD9): (0xFD, 0xFF, 0x69),
    (0xC2, 0xB9, 0xAA): (0xDD, 0xDF, 0x5B),
    (0xD2, 0xC9, 0xB3): (0xD0, 0xD2, 0x56),
}

TOLERANCE = 12

SOURCES = [
    "interactivemaping/alarrRegion.png",
    "interactivemaping/AlarrCoast.png",
    "interactivemaping/AlrrianWilderness.png",
    "interactivemaping/BriarProvince.png",
    "interactivemaping/down_arrow_1.png",
    "interactivemaping/right_arrow_1.png",
]


def recolor(path: Path) -> Path:
    image = Image.open(path).convert("RGBA")
    pixels = np.array(image)
    rgb = pixels[:, :, :3].astype(int)

    for source, target in COLOR_SWAPS.items():
        distance = np.abs(rgb - np.array(source)).sum(axis=2)
        pixels[:, :, :3][distance <= TOLERANCE] = target

    out_path = path.with_name(f"{path.stem}_hover.png")
    Image.fromarray(pixels).save(out_path)
    return out_path


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    for relative in SOURCES:
        print(recolor(root / relative).relative_to(root))
    return 0


if __name__ == "__main__":
    sys.exit(main())
