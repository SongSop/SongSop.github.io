---
title: Hello, World
date: 2026-07-30
---

这是我的第一篇博客文章。

## 关于这个博客

纯手工搭建的极简博客，托管在 [GitHub Pages](https://pages.github.com/)。设计灵感来自 Simon Willison。

## Markdown 功能测试

### 代码高亮

Python 代码块自动高亮：

```python
def fibonacci(n: int) -> int:
    """返回第 n 个斐波那契数"""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b

# 测试
print(fibonacci(10))  # → 55
```

JavaScript 也支持：

```javascript
const greet = (name) => {
  console.log(`Hello, ${name}!`);
};
```

### 数学公式

行内公式：$E = mc^2$

块级公式：

$$
\int_{-\infty}^{\infty} e^{-x^2} \, dx = \sqrt{\pi}
$$

另一个例子：$\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$

### 表格

| 方案 | 复杂度 | 适用 |
|------|--------|------|
| 纯 HTML | 极简 | 少量页面 |
| Jekyll | 中等 | GitHub Pages 原生 |
| Hugo | 中等 | 速度最快 |

### 引用

> 简单是终极的复杂。
> — 达·芬奇

### 图片

![示例图片](images/example.png)

---

以上就是这个博客的 Markdown 功能展示。
