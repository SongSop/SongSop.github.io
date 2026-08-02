---
type: article
title: 换电脑、迁移 Astro、修 bug
date: 2026-08-02
---

第一篇文章发出去不到 24 小时，开发的设备因为一些原因用不了了。好在代码已经推到 GitHub 上，在新电脑上 clone 下来就能继续。

但事情没有想象中那么顺利。

## 环境

新电脑上什么都没有。没有 Python，没有 Node.js，没有字体，没有编辑器。从头来。

博客已经在前一台设备上迁到了 Astro，所以这次只需要装 Node.js 就够了。但 Windows 上装 Node.js 也出了一点状况——winget 不可用，直接下载安装包需要管理员权限兜兜转转最后用了一个之前解压到一半的 v22.12.0。把路径写到系统环境变量里，重启终端，终于认了。

```bash
node --version  # v22.12.0
npm --version   # 10.9.0
```

`npm install` 一把过。

## 架构

第一篇文章里提到过，最初的博客是纯 Python 方案——每个 Markdown 文件手动转成一段 HTML，然后用字符串模板拼进 `base.html` 里。简单高效，但谈不上什么设计感，MacOS 风格的模糊导航栏加上麦当劳配色（红色导航栏配白色背景），能用就行。

这次迁移到 Astro，不只是换了个构建工具。借着重新拆解组件的机会，也重新设计了整个视觉。

### 配色

键盘圈有一个经典的复古配色叫 [GMK 9009](https://matrixzj.github.io/docs/gmk-keycaps/GMK-9009/)，cream + cement + orange，暖灰调里带一点橙色点缀，像是从八十年代的工业设计手册里撕下来的。我之前折腾机械键盘的时候就对这个配色印象很深。

把它搬到了博客上：

```css
:root {
  --cream:   #F5F3EE;  /* 页面底色，乳白偏灰 */
  --cement:  #C4C9C9;  /* 边框、分割线、侧边栏标题 */
  --orange:  #F46822;  /* 链接、高亮、hover */
  /* ... */
}
```

不是纯白背景戳眼睛，不是纯黑看久了压抑。比第一版的麦当劳配色安静很多，也更耐看。

字体选了 JetBrains Mono——程序员最喜欢的等宽字体之一，以前用 Monaco，这次换过来。字型大了一圈，行宽也放宽了，每行大概 80 个字符左右。

### 组件化

原来的 `base.html` 是一整坨 200 行的大模板，Header、侧边栏、搜索框、Footer 全部揉在一起，改任何东西都得扫一遍全文。

拆成 Astro 组件之后：

- `Base.astro`：页面骨架，包含 Header、侧边栏、Footer，通过 `<slot />` 插入页面内容
- `index.astro`：首页，遍历文章列表生成摘要
- `[slug].astro`：文章详情页，Markdown 渲染 + KaTeX 数学公式

侧边栏是整站变化最大的地方。之前只有一个链接列表，现在加上了 About 简介、全部文章归档、以及 Elsewhere 外部链接。每次都手动从文章列表里更新最近文章，虽然麻烦，但相比之前的那种"孤零零的页面"，已经有了点"博客"的样子。

## 三个 bug

跑 `npm run build`，报错。

### 图片路径

第一篇文章里有一张天空的照片。在旧的 Python 方案里，图片放在项目根目录的 `images/` 下，文章里用 `images\xxx.jpg` 引用。Markdown 解析器不关心斜杠方向，直接拼路径就行。

Astro 不一样。它用 Vite 处理资源，图片需要用正斜杠，而且路径是相对于页面根的。更关键的是——图片得放在 `public/` 目录下。这是 Astro 的约定：`public/` 下的文件原样输出，不经过 Vite 的处理管线。

修改：

```diff
- ![sky](images\img_v3_02146_xxx.jpg)
+ ![sky](/images/img_v3_02146_xxx.jpg)
```

顺便把图片挪到 `public/images/`。

### 搜索链接

搜索功能是纯前端方案：构建时生成 `search.json`，一段 JS 做即时检索。旧的代码里搜索结果链接写死了 `.html` 后缀：

```javascript
'<a href="' + p.slug + '.html" class="search-result-item">'
```

但 Astro 默认生成的是 Clean URL（`/posts/slug/` 不带 `.html`），所以搜索结果点进去全是 404。

改成：

```javascript
'<a href="/posts/' + p.slug + '/" class="search-result-item">'
```

### CSS 丢了

`astro build` 不报错，但打开页面是一个毛坯房——所有的样式都没了。检查一下生成的 HTML，`<head>` 里只有一个 Google Fonts 的 `<link>`，没有任何 CSS。

原因在 `Base.astro` 里：

```javascript
import '../styles/global.css';
```

这段代码看起来没问题——在 Astro 的文档里这也是推荐写法。但不知为什么，Vite 在处理的时候没有把它打包进去。`dist/_astro/` 下只有 KaTeX 的字体文件，没有任何 CSS 文件。

排查了一圈，最简单的解决方案是把 CSS 放到 `public/` 下让它原样输出，然后在 `<head>` 里用传统方式 link：

```diff
- import '../styles/global.css';
+ <!-- 移到 public/styles/ -->

  <link rel="stylesheet" href="/styles/global.css">
```

CSS 文件本身不用改，一个字都不动。

## 清理

旧的 Python 时代遗留下一些文件——`posts/` 目录（文章已经移到 `src/content/posts/` 里了）、多余的 `images/` 目录。这些都删干净了。README 也更新成 Astro 的说明。

## 迁移前后对比

| | Python 方案 | Astro |
|---|---|---|
| 本地预览 | `python dev.py` | `npm run dev` |
| 构建 | `python build.py` | `npm run build` |
| 热更新 | 文件变化触发完整 rebuild | HMR，只刷新变化的部分 |
| 文章存放 | `posts/*.md` | `src/content/posts/*.md` |
| 图片 | `images/` | `public/images/` |
| 布局 | Python 模板字符串 | Astro 组件 |
| 数学公式 | MathJax（按需加载） | KaTeX（构建时渲染） |
| 搜索 | 纯前端 JSON + JS | 同上，基本没变 |
| 配色 | 麦当劳红白 | GMK 9009 Cream + Cement + Orange |
| 排版 | Monaco，窄行宽 | JetBrains Mono，放宽行宽 |

Astro 带来的最大改进是**组件化**。侧边栏、文章列表、页面头尾——每个都是独立的组件，改一个地方全站生效。之前改一下 CSS 要手动 rebuild 所有页面，现在保存就立即看到结果。

## 之后

这次迁移暴露了一个问题：`import` CSS 在 Astro 里时灵时不灵。可能跟具体版本有关，也可能是路径解析的问题。目前用 `<link>` 的 workaround 能用，但之后想搞清楚为什么——也许能变成一篇 debug 笔记。
