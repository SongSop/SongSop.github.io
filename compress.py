from PIL import Image
import os, glob

SRC = r"d:\blog\SongSop.github.io\public\images\portfolio"
MAX_W = 1200
QUALITY = 80

total_before = 0
total_after = 0

for f in sorted(glob.glob(os.path.join(SRC, "*.jpg"))):
    name = os.path.basename(f)
    before = os.path.getsize(f)
    with Image.open(f) as im:
        if im.mode in ("RGBA", "P", "LA"):
            im = im.convert("RGB")
        w, h = im.size
        if w > MAX_W:
            nh = int(h * MAX_W / w)
            im = im.resize((MAX_W, nh), Image.LANCZOS)
        im.save(f, "JPEG", quality=QUALITY, optimize=True, progressive=True)
        after = os.path.getsize(f)
    total_before += before
    total_after += after
    print(f"{name}: {before/1024:.0f}KB -> {after/1024:.0f}KB  ({w}x{h} -> {im.size[0]}x{im.size[1]})")

print(f"\nTOTAL: {total_before/1024/1024:.1f}MB -> {total_after/1024/1024:.1f}MB")
