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
   - **相册网格**：用 `<div class="gallery">` 包裹若干 `<figure>`，自动响应式排列

## 相册网格

在文章里写 HTML，每个 `<figure>` 是一张卡片：

```html
<div class="gallery">
  <figure>
    <img src="/images/portfolio/01.jpg" alt="项目一">
    <figcaption>项目一 — 一句话说明</figcaption>
  </figure>
</div>
```

图片按原始比例完整显示（不裁剪），高度上限 420px，网格随屏宽自动换行。

> 新增图片建议先压缩，否则手机加载很慢。项目根目录有 `compress.py`，
> 把图放进 `public/images/portfolio/` 后运行 `python compress.py`，
> 会压到 1200px 宽 / 质量 80%（原图需自行备份）。

## 样式（重要）

样式的**唯一源文件是 `public/styles/global.css`**，由 `Base.astro` 通过 `<link>` 引入。

> 注意：不要新建 `src/styles/` 并用 `import` 引入——本环境下 Astro 的 CSS import
> 不会把样式打进产物（已验证，清缓存后依然如此），页面会变成无样式状态。
> 改样式请直接编辑 `public/styles/global.css`。

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
├── public/
│   ├── styles/
│   │   └── global.css      ← ✏️ 样式（唯一源）
│   ├── images/             ← ✏️ 放图片
│   │   └── portfolio/      ← 简历作品集照片
│   ├── search.js           ← 搜索前端
├── astro.config.mjs        ← Astro 配置
└── package.json
```
