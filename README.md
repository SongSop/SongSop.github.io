# My Weblog

Astro 驱动的极简个人博客，Simon Willison 风格，托管在 GitHub Pages。

## 本地开发

```bash
npm install
npm run dev
```

浏览器打开 `http://localhost:4321`。编辑 `src/content/posts/*.md` → 热更新自动刷新。

## 写文章

1. 在 `src/content/posts/` 目录下创建 `YYYY-MM-DD-slug.md`
2. 添加 frontmatter：
   ```yaml
   ---
   type: article  # article | note | link
   title: 文章标题
   date: 2026-01-01
   ---
   ```
3. 写 Markdown，支持：
   - **代码高亮**：标记语言后自动着色
   - **数学公式（KaTeX）**：`$E=mc^2$` 行内，`$$...$$` 块级
   - **图片**：放 `public/images/` 目录，`![alt](/images/file.png)`
   - **表格**：标准 Markdown 表格语法

## 构建

```bash
npm run build
```

输出到 `dist/` 目录。

## 部署到 GitHub Pages

本项目已配置 GitHub Actions 自动部署。
Push 到 `main` 分支后自动构建并部署。

## 文件结构

```
SongSop.github.io/
├── src/
│   ├── content/
│   │   └── posts/          ← ✏️ 写 Markdown 文章
│   │       └── YYYY-MM-DD-slug.md
│   ├── layouts/
│   │   └── Base.astro      ← 页面布局
│   ├── pages/
│   │   ├── index.astro     ← 首页
│   │   ├── posts/[slug].astro ← 文章页
│   │   └── search.json.ts  ← 搜索接口
│   └── styles/
│       └── global.css      ← 样式
├── public/
│   ├── images/             ← ✏️ 放图片
│   └── search.js           ← 搜索前端
├── astro.config.mjs        ← Astro 配置
└── package.json
```
