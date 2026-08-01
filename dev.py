"""实时预览开发服务器 — 保存即刷新 + Markdown 自动构建"""
import http.server
import os
import sys
import time
import threading
import subprocess
import webbrowser

PORT = 8080
ROOT = os.path.dirname(os.path.abspath(__file__))

# 版本号：只有文件变化时才递增，作为是否刷新的依据
_version = 0


def bump_version():
    global _version
    _version += 1
    return _version


# 自动刷新脚本 — 版本号变了才刷新
RELOAD_SCRIPT = b"""
<script>
(function() {
  var v = 0;
  setInterval(function() {
    fetch('/__ping').then(function(r) { return r.text(); }).then(function(t) {
      var nv = parseInt(t) || 0;
      if (v === 0) { v = nv; return; }
      if (nv !== v) { location.reload(); }
    });
  }, 800);
})();
</script>
"""


class DevHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def do_GET(self):
        if self.path == "/__ping":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
            self.end_headers()
            self.wfile.write(str(_version).encode())
            return

        # HTML 文件注入自动刷新脚本
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            path = os.path.join(path, "index.html")
        if path.endswith(".html") and os.path.exists(path):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            with open(path, "rb") as f:
                content = f.read()
            content = content.replace(b"</body>", RELOAD_SCRIPT + b"</body>")
            self.wfile.write(content)
            return

        return super().do_GET()

    def log_message(self, format, *args):
        if "/__ping" not in str(args):
            sys.stdout.write("[%s] %s\n" % (time.strftime("%H:%M:%S"), args[0]))


def watch_files():
    """监听文件变化 → rebuild → bump 版本号"""
    posts_dir = os.path.join(ROOT, "posts")
    templates_dir = os.path.join(ROOT, "templates")
    style_css = os.path.join(ROOT, "style.css")
    mtimes = {}

    # 初始构建
    subprocess.run([sys.executable, os.path.join(ROOT, "build.py")])
    bump_version()

    while True:
        changed = False

        # 监听 posts/ 和 templates/
        for watch_dir in [posts_dir, templates_dir]:
            if not os.path.isdir(watch_dir):
                continue
            for root, _, files in os.walk(watch_dir):
                for f in files:
                    fp = os.path.join(root, f)
                    try:
                        mt = os.stat(fp).st_mtime
                    except OSError:
                        continue
                    if fp not in mtimes:
                        mtimes[fp] = mt
                    elif mt != mtimes[fp]:
                        mtimes[fp] = mt
                        rel = os.path.relpath(fp, ROOT)
                        sys.stdout.write("\n→ %s changed, rebuilding...\n\n" % rel)
                        changed = True

        # 监听 style.css
        for fpath in [style_css]:
            if os.path.exists(fpath):
                try:
                    mt = os.stat(fpath).st_mtime
                except OSError:
                    continue
                if fpath not in mtimes:
                    mtimes[fpath] = mt
                elif mt != mtimes[fpath]:
                    mtimes[fpath] = mt
                    rel = os.path.relpath(fpath, ROOT)
                    sys.stdout.write("\n→ %s changed, bumping version...\n\n" % rel)
                    bump_version()

        if changed:
            subprocess.run([sys.executable, os.path.join(ROOT, "build.py")])
            bump_version()

        time.sleep(1)


if __name__ == "__main__":
    os.chdir(ROOT)

    # 文件监听线程
    watcher = threading.Thread(target=watch_files, daemon=True)
    watcher.start()

    # 等首次构建完成
    time.sleep(2)

    server = http.server.HTTPServer(("", PORT), DevHandler)

    print(f"\n  博客预览: http://localhost:{PORT}/\n")
    print("  编辑 posts/*.md   → rebuild → 刷新")
    print("  编辑 style.css     → 刷新")
    print("  编辑 templates/*   → rebuild → 刷新")
    print("  按 Ctrl+C 退出\n")

    webbrowser.open(f"http://localhost:{PORT}/")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  已退出")
        server.shutdown()
