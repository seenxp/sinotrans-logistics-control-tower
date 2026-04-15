# 外运物流控制塔 - 设计系统使用指南

## 概述

本项目集成了 [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) 设计系统，为AI代理提供统一的设计规范。

## 什么是 DESIGN.md？

DESIGN.md 是 Google Stitch 引入的新概念，是一个纯文本设计系统文档，AI代理读取它来生成一致的UI。它只是一个markdown文件，不需要Figma导出或特殊工具。

## 文件结构

```
sinotrans-logistics-control-tower/
├── DESIGN.md              # 设计系统文档（AI代理读取）
├── preview.html           # 亮色主题预览
├── preview-dark.html      # 暗色主题预览
└── DESIGN_GUIDE.md        # 本使用指南
```

## 如何使用

### 1. 查看设计系统预览

打开预览文件查看完整的设计系统：

**启动HTTP服务器:**
```bash
# 进入项目目录
cd ~/sinotrans-logistics-control-tower

# 启动Python HTTP服务器
python3 -m http.server 8080
```

**访问预览页面:**
- 亮色主题: http://localhost:8080/preview.html
- 暗色主题: http://localhost:8080/preview-dark.html

**注意:** 必须使用HTTP服务器访问，不能直接打开本地文件，否则会遇到跨域错误。

### 2. 让AI代理使用设计系统

当你让AI代理生成UI组件时，告诉它使用 `DESIGN.md` 文件：

#### 示例提示词：

**生成卡片组件:**
```
请使用 DESIGN.md 设计系统创建一个物流订单卡片组件。
要求：
- 使用Bg Component背景 (#ffffff)
- 添加12px圆角
- 应用base阴影 (0 3px 6px -4px rgba(0, 0, 0, 0.12))
- 内部间距24px
- 标题使用H4样式
- 状态标签使用功能色
```

**生成按钮组件:**
```
请使用 DESIGN.md 设计系统创建一组按钮组件。
包括：
- 主要按钮 (Primary Blue #1890ff)
- 次要按钮 (白色背景，灰色边框)
- 幽灵按钮 (透明背景，蓝色边框)
- 成功按钮 (Success #52c41a)
- 警告按钮 (Warning #faad14)
- 错误按钮 (Error #f5222d)
```

**生成数据表格:**
```
请使用 DESIGN.md 设计系统创建一个订单数据表格。
要求：
- 表头背景: #f0f2f5
- 行高: 54px
- 边框: 1px solid #f0f0f0
- 悬停行: #e6f7ff
- 状态列使用标签组件
```

### 3. 快速颜色参考

在代码中使用以下颜色：

```css
/* 主色调 */
--primary-color: #1890ff;
--primary-hover: #40a9ff;
--primary-active: #096dd9;
--primary-light: #e6f7ff;

/* 功能色 */
--success-color: #52c41a;
--warning-color: #faad14;
--error-color: #f5222d;
--info-color: #1890ff;

/* 中性色 */
--text-primary: rgba(0, 0, 0, 0.85);
--text-secondary: rgba(0, 0, 0, 0.65);
--text-disabled: rgba(0, 0, 0, 0.25);
--border-color: #d9d9d9;
--bg-base: #ffffff;
--bg-layout: #f0f2f5;

/* 物流业务色 */
--truck-color: #fa8c16;   /* 卡车 */
--ship-color: #1890ff;    /* 船舶 */
--plane-color: #52c41a;   /* 航空 */
--train-color: #722ed1;   /* 铁路 */
```

### 4. 字体参考

```css
/* 字体栈 */
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;

/* 数字字体 */
font-family-number: 'DIN Alternate', 'DIN Alternate Bold', sans-serif;

/* 字体层级 */
H1: 30px, line-height: 38px, font-weight: 600
H2: 24px, line-height: 32px, font-weight: 600
H3: 20px, line-height: 28px, font-weight: 600
H4: 16px, line-height: 24px, font-weight: 600
Body: 16px, line-height: 24px, font-weight: 400
Small: 14px, line-height: 22px, font-weight: 400
Caption: 12px, line-height: 20px, font-weight: 400
```

### 5. 间距参考

```css
/* 间距系统 (8px基础) */
--spacing-xs: 4px;
--spacing-sm: 8px;
--spacing-md: 16px;
--spacing-lg: 24px;
--spacing-xl: 32px;

/* 常用间距 */
卡片内部: 24px
区块间距: 32px
页面边距: 24px (移动端), 48px (桌面端)
```

### 6. 阴影参考

```css
/* 阴影系统 */
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
--shadow-base: 0 3px 6px -4px rgba(0, 0, 0, 0.12);
--shadow-lg: 0 6px 16px 0 rgba(0, 0, 0, 0.08);
--shadow-xl: 0 9px 28px 8px rgba(0, 0, 0, 0.05);
```

### 7. 组件参考

#### 按钮
```html
<!-- 主要按钮 -->
<button class="btn btn-primary">主要按钮</button>

<!-- 次要按钮 -->
<button class="btn btn-secondary">次要按钮</button>

<!-- 幽灵按钮 -->
<button class="btn btn-ghost">幽灵按钮</button>
```

#### 卡片
```html
<div class="card">
  <div class="card-header">标题</div>
  <div class="card-body">内容</div>
  <div class="card-footer">底部</div>
</div>
```

#### 状态标签
```html
<span class="tag tag-success">成功</span>
<span class="tag tag-warning">警告</span>
<span class="tag tag-error">错误</span>
<span class="tag tag-info">信息</span>
```

## 设计原则

### 1. 数据优先
所有设计决策服务于数据展示效率

### 2. 响应式
支持从移动端到大屏的全设备适配

### 3. 无障碍
符合WCAG 2.1 AA标准

## 最佳实践

### ✅ 推荐做法
- 使用系统字体栈确保跨平台一致性
- 保持8px间距系统的严格应用
- 数据可视化使用业务专用颜色编码
- 确保文字对比度符合WCAG AA标准
- 响应式设计优先考虑移动端体验

### ❌ 避免做法
- 不要使用超过3种主要颜色
- 不要使用小于12px的字体
- 不要创建无边框的卡片
- 不要在暗色背景上使用低对比度文字
- 不要过度使用动画效果

## 扩展设计系统

如需扩展设计系统，可以参考以下资源：

### 从 awesome-design-md 选择其他风格

- **Vercel** - 黑白精确、Geist字体
- **Linear** - 超极简、精确、紫色强调
- **Stripe** - 紫色渐变、优雅

访问 [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) 查看完整集合。

### 自定义设计系统

1. 复制 `DESIGN.md` 文件
2. 修改颜色、字体、间距等值
3. 更新预览文件
4. 测试AI代理生成效果

## 故障排除

### Q: AI代理生成的UI不符合设计系统
A: 确保在提示词中明确指定使用 `DESIGN.md` 文件，并提供具体的设计要求。

### Q: 颜色值不正确
A: 检查 `DESIGN.md` 中的颜色定义，确保使用正确的HEX值。

### Q: 组件样式不一致
A: 使用 `preview.html` 作为参考，确保组件样式与设计系统一致。

## 相关资源

- [awesome-design-md GitHub](https://github.com/VoltAgent/awesome-design-md)
- [Google Stitch DESIGN.md](https://stitch.withgoogle.com/docs/design-md/overview/)
- [DESIGN.md 格式规范](https://stitch.withgoogle.com/docs/design-md/format/)
- [Ant Design](https://ant.design/)
- [Naive UI](https://www.naiveui.com/)

## 更新日志

### v1.0.0 (2026-04-15)
- 初始版本
- 集成 awesome-design-md 设计系统
- 创建外运物流控制塔专用设计规范
- 提供亮色和暗色主题预览
- 编写使用指南文档