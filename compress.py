from PIL import Image
import os, glob

SRC = r"d:\blog\SongSop.github.io\public\images\portfolio"
MAX_W = 1200
QUALITY = 80

# 已被压缩过（宽度 <= MAX_W）的图片会跳过，避免重复编码导致画质损失
for f in sorted(glob.glob(os.path.join(SRC, "*.jpg"))):
    name = os.path.basename(f)
    with Image.open(f) as im:
        w, h = im.size
        if w <= MAX_W:
            print(f"{name}: skip (already {w}px wide)")
            continue
        if im.mode in ("RGBA", "P", "LA"):
            im = im.convert("RGB")
        before = os.path.getsize(f)
        nh = int(h * MAX_W / w)
        im = im.resize((MAX_W, nh), Image.LANCZOS)
        im.save(f, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    after = os.path.getsize(f)
    print(f"{name}: {before/1024:.0f}KB -> {after/1024:.0f}KB  ({w}x{h} -> {MAX_W}x{nh})")
