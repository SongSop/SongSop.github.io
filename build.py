"""
build.py — 将 Markdown 文章构建为静态 HTML

支持三种内容类型:
  article — 长文章（默认），有标题
  note    — 随手笔记/每日小结，以日期为主导
  link    — 资源分享/书签，外部链接 + 简短注释

用法:
    python build.py          # 构建全部
    python new.py            # 快速新建一篇笔记
    python new.py -t link    # 新建链接分享
"""

import os
import sys
import re
import json
from pathlib import Path
from datetime import datetime

import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension
import frontmatter

ROOT = Path(__file__).parent
POSTS_DIR = ROOT / "posts"
IMAGES_DIR = ROOT / "images"
TEMPLATES_DIR = ROOT / "templates"

MD = markdown.Markdown(extensions=[
    CodeHiliteExtension(guess_lang=True, css_class='codehilite'),
    FencedCodeExtension(),
    TableExtension(),
    'footnotes',
])

MATH_SCRIPT = """
<script>
window.MathJax = {
  tex: { inlineMath: [['$','$'], ['\\\\(','\\\\)']] },
  options: { ignoreHtmlClass: 'no-math' }
};
</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
"""


def load_template() -> str:
    path = TEMPLATES_DIR / "base.html"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — My Weblog</title>
  <link rel="stylesheet" href="style.css">
  {extra_head}
</head>
<body>
  <header class="site-header">
    <div class="container">
      <div class="header-row">
        <a href="/" class="site-title">My Weblog</a>
      </div>
    </div>
  </header>
  <div class="container">
    <div class="content-shell">
      <div class="page-layout">
        <div class="main-column">{content}</div>
        <aside class="sidebar">
          <div class="sidebar-section"><h3>About</h3><p class="sidebar-description">Developer. Notes and links.</p></div>
        </aside>
      </div>
    </div>
  </div>
  <footer class="site-footer"><div class="container"><p>Hosted on <a href="https://pages.github.com">GitHub Pages</a></p></div></footer>
</body>
</html>"""


def parse_post(md_path: Path) -> dict:
    post = frontmatter.load(str(md_path))

    filename = md_path.stem
    parts = filename.split("-", 3)

    if len(parts) >= 3 and parts[0].isdigit():
        raw_date = f"{parts[0]}-{parts[1]}-{parts[2]}"
        desc = parts[3] if len(parts) > 3 else "post"
        slug = f"{raw_date}-{desc}"
    else:
        raw_date = datetime.now().strftime("%Y-%m-%d")
        slug = f"{raw_date}-{filename}"

    date_val = post.get("date", raw_date)
    title = post.get("title", "")
    custom_slug = post.get("slug", slug)
    post_type = post.get("type", "article")
    external_link = post.get("link", "")

    if isinstance(date_val, str):
        date_str = date_val
    else:
        date_str = date_val.strftime("%Y-%m-%d")
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        date_str = raw_date

    if post_type == "note" and not title:
        title = date_str

    html_body = MD.convert(post.content)
    MD.reset()

    has_math = "$" in post.content

    return {
        "slug": custom_slug,
        "title": title,
        "date": date_str,
        "type": post_type,
        "link": external_link,
        "html": html_body,
        "has_math": has_math,
    }


def render_post_page(post: dict, template: str, archive: str = "") -> str:
    extra = MATH_SCRIPT if post["has_math"] else ""

    if post["type"] == "link" and post["link"]:
        header_html = f"""
          <header class="article-header">
            <span class="entry-type-badge">Link</span>
            <h1><a href="{post['link']}" class="external-link-heading">{post['title']}</a></h1>
            <time datetime="{post['date']}">{post['date']}</time>
          </header>"""
    elif post["type"] == "note":
        header_html = f"""
          <header class="article-header">
            <span class="entry-type-badge">Note</span>
            <h1>{post['title']}</h1>
            <time datetime="{post['date']}">{post['date']}</time>
          </header>"""
    else:
        header_html = f"""
          <header class="article-header">
            <h1>{post['title']}</h1>
            <time datetime="{post['date']}">{post['date']}</time>
          </header>"""

    post_html = f"""
        <article>
          {header_html}
          <div class="content">
            {post['html']}
          </div>
        </article>
        <nav class="back-nav">
          <a href="/">Back</a>
        </nav>"""

    return template.format(
        title=post["title"],
        extra_head=extra,
        archive=archive,
        content=post_html,
    )


def render_index(posts: list, template: str, archive: str = "") -> str:
    """首页 — 展示每篇文章的完整内容"""
    items = []
    for p in posts:
        date = p["date"]
        slug = p["slug"]
        title = p["title"]
        ptype = p["type"]
        html_body = p["html"]

        if ptype == "link":
            link_url = p["link"]
            domain = link_url.split("://")[-1].split("/")[0] if link_url else ""
            entry_head = f"""
          <div class="entry-head">
            <span class="entry-date"><a href="{slug}.html">{date}</a></span>
            <span class="entry-type-tag">Link</span>
            <a href="{slug}.html" class="entry-title">{title}</a>
            <a href="{link_url}" class="entry-domain" rel="nofollow">{domain}</a>
          </div>"""
        elif ptype == "note":
            entry_head = f"""
          <div class="entry-head">
            <span class="entry-date"><a href="{slug}.html">{date}</a></span>
            <span class="entry-type-tag">Note</span>
            <a href="{slug}.html" class="entry-title">{title}</a>
          </div>"""
        else:
            entry_head = f"""
          <div class="entry-head">
            <span class="entry-date"><a href="{slug}.html">{date}</a></span>
            <a href="{slug}.html" class="entry-title">{title}</a>
          </div>"""

        items.append(f"""
        <article class="entry">
          {entry_head}
          <div class="entry-body">
            {html_body}
          </div>
          <a href="{slug}.html" class="entry-permalink">Permalink</a>
        </article>""")

    index_html = "\n".join(items) if items else '<p style="color: var(--muted); padding: 40px 0;">No posts yet.</p>'

    # 首页也需要 MathJax 如果有文章包含公式
    index_extra = ""
    if any(p["has_math"] for p in posts):
        index_extra = MATH_SCRIPT

    return template.format(
        title="Home",
        extra_head=index_extra,
        archive=archive,
        content=f'{index_html}',
    )


def build():
    """构建全部静态文件"""
    print("Building...\n")

    template = load_template()

    # 清空旧 HTML
    for f in ROOT.glob("*.html"):
        if f.name != "404.html":
            f.unlink()

    posts = []
    for md_path in sorted(POSTS_DIR.glob("*.md"), reverse=True):
        try:
            post = parse_post(md_path)
            posts.append(post)
        except Exception as e:
            print(f"  ERR {md_path.name}: {e}")

    # 生成归档列表（所有页面共用）
    archive_items = []
    for p in posts:
        archive_items.append(
            f'<li><a href="{p["slug"]}.html"><span class="archive-date">{p["date"]}</span>{p["title"]}</a></li>'
        )
    archive_html = (
        '<ul class="archive-list">' + "".join(archive_items) + "</ul>"
        if archive_items
        else ""
    )

    # 生成文章页面
    for p in posts:
        out_path = ROOT / f"{p['slug']}.html"
        html = render_post_page(p, template, archive_html)
        out_path.write_text(html, encoding="utf-8")
        tag = {"article": "[A]", "note": "[N]", "link": "[L]"}.get(p["type"], "[?]")
        print(f"  {tag} {p['slug']}.html  <-  {p['title']}")

    # 首页
    index_html = render_index(posts, template, archive_html)
    (ROOT / "index.html").write_text(index_html, encoding="utf-8")
    print(f"\n  OK index.html  ({len(posts)} posts)")

    # 搜索索引
    search_data = []
    for p in posts:
        text = re.sub(r"<[^>]+>", "", p["html"])
        text = re.sub(r"\s+", " ", text).strip()[:300]
        search_data.append({
            "title": p["title"],
            "date": p["date"],
            "slug": p["slug"],
            "type": p["type"],
            "text": text,
        })
    (ROOT / "search.json").write_text(
        json.dumps(search_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("  OK search.json")

    print("\nDone. Preview: python dev.py\n")


if __name__ == "__main__":
    if "--watch" in sys.argv:
        import time
        print("Watching posts/ for changes...\n")
        build()
        mtimes = {}
        while True:
            for md in POSTS_DIR.glob("*.md"):
                mt = md.stat().st_mtime
                if md not in mtimes:
                    mtimes[md] = mt
                elif mt != mtimes[md]:
                    mtimes[md] = mt
                    print(f"\n-> {md.name} changed, rebuilding...\n")
                    build()
                    break
            time.sleep(1)
    else:
        build()
