"""快速新建一篇内容

用法:
    python new.py                     # 新建今日笔记 (note)
    python new.py -t link             # 新建链接分享
    python new.py -t article "标题"   # 新建长文章

生成的文件自动命名: YYYY-MM-DD-slug.md
"""

import sys
import os
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
POSTS_DIR = ROOT / "posts"
POSTS_DIR.mkdir(exist_ok=True)

today = datetime.now()
date_str = today.strftime("%Y-%m-%d")

# 解析参数
args = sys.argv[1:]
post_type = "note"
title = ""

i = 0
while i < len(args):
    if args[i] == "-t" and i + 1 < len(args):
        post_type = args[i + 1]
        i += 2
    else:
        title = args[i]
        i += 1

if post_type not in ("note", "article", "link"):
    print(f"Unknown type: {post_type}. Use: note, article, link")
    sys.exit(1)

# 生成文件名
if title:
    slug = title.lower().replace(" ", "-").replace("/", "-")[:40]
else:
    slug_map = {"note": "today", "article": "post", "link": "link"}
    slug = slug_map.get(post_type, "post")

filename = f"{date_str}-{slug}.md"
filepath = POSTS_DIR / filename

if filepath.exists():
    print(f"Already exists: posts/{filename}")
    print("Edit it directly, or choose a different title.")
    sys.exit(0)

# 根据类型生成模板
templates = {
    "note": f"""---
type: note
date: {date_str}
---

今天的事情：

-

-

-
""",

    "link": f"""---
type: link
title: 资源标题
date: {date_str}
link: https://
---

简短说明为什么值得收藏。
""",

    "article": f"""---
type: article
title: {title or "文章标题"}
date: {date_str}
---

开始写吧。
""",
}

content = templates[post_type]
filepath.write_text(content, encoding="utf-8")
print(f"Created: posts/{filename}")
print(f"Type:   {post_type}")
print(f"Edit and save → browser auto-refreshes.")
