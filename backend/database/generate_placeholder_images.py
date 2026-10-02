"""
Script sekali jalan: membuat gambar placeholder untuk slider seed.

Jalankan dari folder backend/:
    .\\.venv\\Scripts\\python.exe database/generate_placeholder_images.py
"""

from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:  # pragma: no cover
    raise SystemExit(
        "Pillow belum terinstall. Jalankan: pip install pillow"
    )

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "uploads" / "sliders"

SLIDERS = [
    ("konsultasi-online.jpg", (37, 99, 235), (59, 130, 246)),   # biru
    ("cek-kesehatan.jpg", (5, 150, 105), (16, 185, 129)),        # hijau
    ("promo-mental.jpg", (124, 58, 237), (168, 85, 247)),        # ungu
]


def gradient(width: int, height: int, start: tuple, end: tuple):
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)
    for x in range(width):
        t = x / max(1, width - 1)
        r = int(start[0] + (end[0] - start[0]) * t)
        g = int(start[1] + (end[1] - start[1]) * t)
        b = int(start[2] + (end[2] - start[2]) * t)
        draw.line([(x, 0), (x, height)], fill=(r, g, b))
    return img


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for filename, start, end in SLIDERS:
        img = gradient(1200, 400, start, end)
        draw = ImageDraw.Draw(img)
        # Hiasan lingkaran translusen sederhana
        for cx, cy, rad in [(980, 120, 90), (1080, 300, 130), (820, 330, 60)]:
            overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            ov_draw = ImageDraw.Draw(overlay)
            ov_draw.ellipse(
                (cx - rad, cy - rad, cx + rad, cy + rad),
                fill=(255, 255, 255, 40),
            )
            img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
        draw = ImageDraw.Draw(img)
        draw.text((60, 175), filename.replace(".jpg", "").replace("-", " ").upper(), fill=(255, 255, 255))

        path = OUTPUT_DIR / filename
        img.save(path, "JPEG", quality=85)
        print(f"OK {path}")


if __name__ == "__main__":
    main()
