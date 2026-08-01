# My Weblog

纯手工 Markdown → HTML 的极简个人博客，Simon Willison 风格，托管在 GitHub Pages。

## 本地预览

```bash
python dev.py
```

浏览器自动打开。编辑 `posts/*.md` → 自动重建 → 浏览器自动刷新。

## 写文章

1. 在 `posts/` 目录下创建 `YYYY-MM-DD-slug.md`
2. 写 Markdown，支持：
   - **代码高亮**：标记语言后自动着色
   - **数学公式**：`$E=mc^2$` 行内，`$$...$$` 块级
   - **图片**：放 `images/` 目录，`![alt](images/file.png)`
   - **表格**：标准 Markdown 表格语法
3. 保存 → 自动 rebuild → 浏览器刷新

## 构建

```bash
python build.py
```

生成 `index.html` 和每篇文章的 `.html` 文件。

## 部署到 GitHub Pages

```bash
git init
git add .
git commit -m "init blog"
git remote add origin https://github.com/你的用户名/仓库名.git
git push -u origin main
```

然后在 GitHub 仓库 → Settings → Pages → Source 选 `main` → Save。

## 文件结构

```
websiteblog/
├── posts/            ← ✏️ 写 Markdown 文章
│   └── YYYY-MM-DD-slug.md
├── images/           ← ✏️ 放图片
├── templates/        ← HTML 模板
│   └── base.html
├── build.py          ← MD → HTML 构建
├── dev.py            ← 本地预览服务器
├── style.css          ← 样式
├── index.html        ← 🤖 构建生成
└── *.html            ← 🤖 构建生成
```
