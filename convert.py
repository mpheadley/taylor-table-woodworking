#!/usr/bin/env python3
"""
convert.py — Image optimizer for J.T.'s Table Collection website

Converts source images to WebP, resizes to web display dimensions,
and organizes them into the images/ subfolder structure.

Usage:
    python3 convert.py           # skip already-converted files
    python3 convert.py --force   # re-process all files

To add a new gallery photo, append an entry to IMAGES below.
Run the script again to process it.
"""

from PIL import Image, ImageCms
from pathlib import Path
import io, sys

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────

SRC_DIR = Path(__file__).parent       # source images live alongside this script
OUT_DIR = SRC_DIR / "images"          # all output goes under images/
QUALITY      = 85    # Default WebP quality for gallery images (0–100).
QUALITY_HERO = 88    # Override quality for hero/spotlight images. Set per-image in IMAGES.

# ─────────────────────────────────────────────────────────────────────────────
# IMAGE CATALOG
#
# Each entry: (source_filename, output_subfolder, output_filename, max_width, alt_text)
#         or: (source_filename, output_subfolder, output_filename, max_width, alt_text, quality)
#
# max_width: image is scaled down so width <= max_width, aspect ratio preserved.
#            Never upscaled. Height is calculated automatically.
#            Gallery standard: 1500   Hero/spotlight: 2000
#
# quality:   optional per-image override. Omit to use QUALITY (85).
#            Use QUALITY_HERO (88) for hero/spotlight images: add it as the 6th element.
#
# alt_text:  used in the HTML reference printed at the end of the run.
# ─────────────────────────────────────────────────────────────────────────────

IMAGES = [

    # ── Brand ────────────────────────────────────────────────────────────────

    (
        "IMG_2050.PNG", "brand", "jts-table-collection-logo.webp", 200,
        "J.T.'s Table Collection logo — eagle emblem, handbuilt since 2017",
    ),
    (
        "IMG_2078.PNG", "brand", "wood-grain-hero.webp", 1200,
        "Close-up of rich wood grain on a handbuilt J.T.'s Table Collection tabletop",
    ),
    (
        "images/brand/justin-taylor-j.t.-bio.jpg", "brand", "justin-taylor-bio.webp", 900,
        "Justin Taylor, founder and builder of J.T.'s Table Collection, handbuilt furniture Alabama",
    ),

    # ── Customization options ─────────────────────────────────────────────────

    (
        "IMG_1917.PNG", "options", "stain-paint-color-chart.webp", 400,
        "J.T.'s Table Collection stain and paint color options — 12 wood stains "
        "including Golden Oak, Walnut, and Mahogany, plus 8 paint colors",
    ),
    (
        "IMG_1943.PNG", "options", "tabletop-styles-rectangle.webp", 400,
        "Diagram of four rectangle tabletop plank patterns: "
        "vertical, horizontal, wide vertical, and diagonal",
    ),
    (
        "IMG_1944.PNG", "options", "tabletop-styles-square.webp", 400,
        "Diagram of five square tabletop plank patterns including "
        "horizontal, vertical, and diagonal plank layouts",
    ),
    (
        "IMG_1947.PNG", "options", "leg-styles-diagram.webp", 400,
        "Diagram of four handbuilt leg styles: "
        "Simple X, Box Style, Fancy X, and Truss Style",
    ),
    (
        "IMG_1994.PNG", "options", "leg-style-chunky-farmhouse.webp", 400,
        "Chunky farmhouse turned table legs — available for kitchen tables, "
        "coffee tables, desks, and benches",
    ),
    (
        "IMG_1995.PNG", "options", "leg-style-industrial-pipes.webp", 400,
        "Industrial pipe table legs compatible with kitchen tables, "
        "coffee tables, and desks",
    ),
    (
        "IMG_1996.PNG", "options", "leg-style-hairpin.webp", 400,
        "Hairpin table legs — modern minimalist style compatible "
        "with all tabletop sizes",
    ),

    # ── Gallery: custom builds ────────────────────────────────────────────────

    (
        "IMG_1845.jpg", "gallery/custom",
        "custom-barn-door-headboard-bedroom-dark-walnut.webp", 1500,
        "Custom barn-door style headboard in dark walnut with X-brace panels "
        "and built-in sconce lighting, installed in customer bedroom",
    ),
    (
        "IMG_1847.jpg", "gallery/custom",
        "custom-barn-door-headboard-portrait-dark-walnut.webp", 2000,
        "Close-up portrait view of custom barn-door headboard with X-brace "
        "woodwork and warm Edison sconce lights",
        QUALITY_HERO,
    ),
    (
        "IMG_3049.jpg", "gallery/custom",
        "custom-porch-swing-bed-white-rope.webp", 2000,
        "Custom hanging porch swing bed with white painted frame and rope "
        "suspension, styled with navy cushions on a Southern front porch",
        QUALITY_HERO,
    ),
    (
        "IMG_4110.jpeg", "gallery/custom",
        "custom-kids-loft-bunk-bed-construction.webp", 1500,
        "Custom kids loft and bunk bed system under construction, "
        "showing X-brace framing and structural detail",
    ),
    (
        "IMG_4584.jpeg", "gallery/custom",
        "custom-kids-loft-bunk-bed-white-finished.webp", 2000,
        "Finished custom white bunk loft system with X-brace railing, "
        "curtained sleeping nooks, fairy lights, and built-in shelving",
        QUALITY_HERO,
    ),
    (
        "IMG_4586.JPG", "gallery/custom",
        "custom-kids-loft-bunk-bed-night-led.webp", 1500,
        "Custom kids loft bunk bed at night with blue LED accent lights "
        "and cozy curtained sleeping nooks",
    ),

    # ── Gallery: coffee tables ────────────────────────────────────────────────

    (
        "IMG_9648.jpeg", "gallery/coffee-tables",
        "farmhouse-coffee-table-golden-oak-white-truss-legs.webp", 2000,
        "Handbuilt farmhouse coffee table in golden oak stain with white truss "
        "legs, styled with fall decor in a living room with green couch and jute rug",
        QUALITY_HERO,
    ),
    (
        "IMG_9660.jpeg", "gallery/coffee-tables",
        "farmhouse-coffee-table-golden-oak-angled-view.webp", 1500,
        "Angled view of farmhouse coffee table showing plank top detail, "
        "golden oak stain, and white painted truss-style legs",
    ),

    # ── Gallery: benches ─────────────────────────────────────────────────────

    (
        "IMG_3288.jpeg", "gallery/benches",
        "farmhouse-bench-dark-walnut-x-legs-mudroom.webp", 2000,
        "Custom farmhouse bench in dark walnut stain with X-style legs, "
        "installed in a customer mudroom entryway with board and batten wall",
        QUALITY_HERO,
    ),

    # ── Add new gallery photos here ───────────────────────────────────────────
    # Standard gallery (1500px, quality 85):
    # (
    #     "IMG_XXXX.jpg", "gallery/tables",
    #     "farmhouse-dining-table-dark-walnut-truss-legs.webp", 1500,
    #     "Handbuilt farmhouse dining table in dark walnut stain with truss legs",
    # ),
    #
    # Hero/spotlight (2000px, quality 88) — add QUALITY_HERO as 6th element:
    # (
    #     "IMG_XXXX.jpg", "gallery/tables",
    #     "farmhouse-dining-table-dark-walnut-truss-legs.webp", 2000,
    #     "Handbuilt farmhouse dining table in dark walnut stain with truss legs",
    #     QUALITY_HERO,
    # ),

]

# ─────────────────────────────────────────────────────────────────────────────


def human_size(n):
    return f"{n / 1024:.0f} KB" if n < 1_000_000 else f"{n / 1_000_000:.1f} MB"


def process_image(src, subfolder, out_name, max_width, alt, quality=None, force=False):
    quality = quality if quality is not None else QUALITY
    src_path = SRC_DIR / src
    out_path = OUT_DIR / subfolder / out_name
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if out_path.exists() and not force:
        img = Image.open(out_path)
        print(f"  SKIP  {out_name}")
        return out_path, img.width, img.height

    if not src_path.exists():
        print(f"  MISS  {src}  ← source file not found, skipping")
        return None, None, None

    src_bytes = src_path.stat().st_size
    img = Image.open(src_path)

    # Convert from embedded color profile (e.g. iPhone Display P3) to sRGB.
    # Without this, P3 wide-gamut colors look washed out after conversion.
    icc = img.info.get('icc_profile')
    if icc and img.mode == 'RGB':
        try:
            img = ImageCms.profileToProfile(
                img,
                ImageCms.ImageCmsProfile(io.BytesIO(icc)),
                ImageCms.createProfile('sRGB'),
                renderingIntent=ImageCms.Intent.PERCEPTUAL,
                outputMode='RGB',
            )
        except Exception:
            img = img.convert('RGB')
    else:
        # Preserve alpha channel (e.g. logos with transparency), else use RGB
        mode = "RGBA" if img.mode in ("RGBA", "LA", "P") else "RGB"
        img = img.convert(mode)

    # Scale down to max_width, never upscale, preserve aspect ratio
    if img.width > max_width:
        new_h = round(img.height * (max_width / img.width))
        img = img.resize((max_width, new_h), Image.Resampling.LANCZOS)

    img.save(out_path, "WEBP", quality=quality, method=6)
    out_bytes = out_path.stat().st_size
    savings = 100 * (1 - out_bytes / src_bytes)

    print(
        f"  OK    {out_name:<58}  {img.width}×{img.height}  "
        f"{human_size(src_bytes)} → {human_size(out_bytes)}  "
        f"({savings:.0f}% smaller)"
    )
    return out_path, img.width, img.height


def main():
    force = "--force" in sys.argv

    if force:
        print("Force mode: re-processing all files\n")

    print(f"Source:  {SRC_DIR}")
    print(f"Output:  {OUT_DIR}")
    print(f"Quality: {QUALITY}\n")
    print(f"{'':6}{'Output filename':<58}  {'Size':>12}  Dimensions")
    print("─" * 100)

    results = []
    for entry in IMAGES:
        src, subfolder, out_name, max_width, alt = entry[:5]
        quality = entry[5] if len(entry) > 5 else None
        out_path, w, h = process_image(src, subfolder, out_name, max_width, alt, quality=quality, force=force)
        if w:
            results.append((subfolder, out_name, w, h, alt))

    # ── Print HTML <img> reference ────────────────────────────────────────────
    print("\n" + "─" * 100)
    print("HTML <img> reference  (copy these attributes into your HTML)\n")

    current_folder = None
    for subfolder, out_name, w, h, alt in results:
        if subfolder != current_folder:
            print(f"  <!-- images/{subfolder}/ -->")
            current_folder = subfolder

        rel = f"images/{subfolder}/{out_name}"
        # First image in brand folder gets eager loading; everything else is lazy
        loading = "eager" if (subfolder == "brand" and out_name == "wood-grain-hero.webp") else "lazy"
        print(
            f'  <img src="{rel}"\n'
            f'       alt="{alt}"\n'
            f'       width="{w}" height="{h}"\n'
            f'       loading="{loading}">\n'
        )

    total_src  = sum(
        (SRC_DIR / e[0]).stat().st_size
        for e in IMAGES
        if (SRC_DIR / e[0]).exists()
    )
    total_out  = sum(
        (OUT_DIR / e[1] / e[2]).stat().st_size
        for e in IMAGES
        if (OUT_DIR / e[1] / e[2]).exists()
    )
    if total_src:
        print(
            f"Total: {human_size(total_src)} → {human_size(total_out)}  "
            f"({100 * (1 - total_out / total_src):.0f}% smaller overall)\n"
        )


if __name__ == "__main__":
    main()
