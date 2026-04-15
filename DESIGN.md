# 外运物流控制塔 - 设计系统 (DESIGN.md)

> 基于 awesome-design-md 企业级设计规范

## 1. Visual Theme & Atmosphere

**设计哲学**: 专业、高效、可信赖的企业级物流管理平台
**密度**: 信息密集型仪表板，注重数据可视化
**情感**: 冷静、精确、技术感、可信赖

**核心原则**:
- 数据优先：所有设计决策服务于数据展示效率
- 响应式：支持从移动端到大屏的全设备适配
- 无障碍：符合WCAG 2.1 AA标准

## 2. Color Palette & Roles

### 主色调 (Primary)
| 名称 | HEX值 | 角色 |
|------|-------|------|
| Primary Blue | `#1890ff` | 主要操作按钮、链接、重点标识 |
| Primary Hover | `#40a9ff` | 悬停状态 |
| Primary Active | `#096dd9` | 激活状态 |
| Primary Light | `#e6f7ff` | 浅色背景、选中状态 |

### 功能色 (Semantic)
| 名称 | HEX值 | 角色 |
|------|-------|------|
| Success | `#52c41a` | 成功状态、正向指标 |
| Warning | `#faad14` | 警告状态、注意事项 |
| Error | `#f5222d` | 错误状态、负向指标 |
| Info | `#1890ff` | 信息提示 |

### 中性色 (Neutral)
| 名称 | HEX值 | 角色 |
|------|-------|------|
| Text Primary | `rgba(0, 0, 0, 0.85)` | 主要文本 |
| Text Secondary | `rgba(0, 0, 0, 0.65)` | 次要文本 |
| Text Disabled | `rgba(0, 0, 0, 0.25)` | 禁用文本 |
| Border Base | `#d9d9d9` | 基础边框 |
| Border Split | `#f0f0f0` | 分割线 |
| Bg Base | `#ffffff` | 基础背景 |
| Bg Layout | `#f0f2f5` | 布局背景 |
| Bg Component | `#ffffff` | 组件背景 |

### 物流业务色
| 名称 | HEX值 | 角色 |
|------|-------|------|
| Truck Orange | `#fa8c16` | 卡车运输 |
| Ship Blue | `#1890ff` | 船舶运输 |
| Plane Green | `#52c41a` | 航空运输 |
| Train Purple | `#722ed1` | 铁路运输 |

## 3. Typography Rules

### 字体栈
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
font-family-number: 'DIN Alternate', 'DIN Alternate Bold', sans-serif;
```

### 字体层级
| 级别 | 字号 | 行高 | 字重 | 用途 |
|------|------|------|------|------|
| H1 | 30px | 38px | 600 | 页面标题 |
| H2 | 24px | 32px | 600 | 区域标题 |
| H3 | 20px | 28px | 600 | 卡片标题 |
| H4 | 16px | 24px | 600 | 小节标题 |
| Body | 16px | 24px | 400 | 正文内容 |
| Small | 14px | 22px | 400 | 辅助文本 |
| Caption | 12px | 20px | 400 | 注释、标签 |

## 4. Component Stylings

### 按钮系统
**主要按钮**
- 背景色: Primary Blue (`#1890ff`)
- 文字色: 白色
- 圆角: 8px
- 内边距: 8px 16px
- 悬停: Primary Hover (`#40a9ff`)

**次要按钮**
- 边框: 1px solid Border Base (`#d9d9d9`)
- 背景色: 透明
- 文字色: Text Primary

**幽灵按钮**
- 背景色: 透明
- 边框: 1px solid Primary Blue

### 卡片系统
- 背景色: Bg Component (`#ffffff`)
- 边框: 1px solid Border Split (`#f0f0f0`)
- 圆角: 12px
- 阴影: `0 3px 6px -4px rgba(0, 0, 0, 0.12)`
- 内边距: 24px

### 输入框
- 高度: 32px (小), 40px (中), 48px (大)
- 边框: 1px solid Border Base (`#d9d9d9`)
- 圆角: 8px
- 聚焦边框: Primary Blue

### 数据表格
- 表头背景: Bg Layout (`#f0f2f5`)
- 行高: 54px
- 边框: 1px solid Border Split (`#f0f0f0`)
- 悬停行: Primary Light (`#e6f7ff`)

## 5. Layout Principles

### 间距系统 (8px基础)
| 名称 | 值 | 用途 |
|------|-----|------|
| xs | 4px | 极小间距 |
| sm | 8px | 小间距 |
| md | 16px | 中等间距 |
| lg | 24px | 大间距 |
| xl | 32px | 超大间距 |

### 网格系统
- 列数: 24列
- 间距: 16px (水平), 16px (垂直)
- 响应式断点:
  - xs: < 576px
  - sm: ≥ 576px
  - md: ≥ 768px
  - lg: ≥ 992px
  - xl: ≥ 1200px
  - xxl: ≥ 1600px

### 留白哲学
- 卡片内部: 24px
- 区块间距: 32px
- 页面边距: 24px (移动端), 48px (桌面端)

## 6. Depth & Elevation

### 阴影系统
| 级别 | 值 | 用途 |
|------|-----|------|
| sm | `0 1px 2px 0 rgba(0, 0, 0, 0.03)` | 轻微阴影 |
| base | `0 3px 6px -4px rgba(0, 0, 0, 0.12)` | 卡片阴影 |
| lg | `0 6px 16px 0 rgba(0, 0, 0, 0.08)` | 弹窗阴影 |
| xl | `0 9px 28px 8px rgba(0, 0, 0, 0.05)` | 模态框阴影 |

### 表面层级
- 层级0: Bg Layout (`#f0f2f5`) - 页面背景
- 层级1: Bg Component (`#ffffff`) - 卡片、面板
- 层级2: 带阴影的卡片
- 层级3: 弹窗、下拉菜单
- 层级4: 模态框

## 7. Do's and Don'ts

### ✅ 设计规范
- 使用系统字体栈确保跨平台一致性
- 保持8px间距系统的严格应用
- 数据可视化使用业务专用颜色编码
- 确保文字对比度符合WCAG AA标准
- 响应式设计优先考虑移动端体验

### ❌ 禁止事项
- 不要使用超过3种主要颜色
- 不要使用小于12px的字体
- 不要创建无边框的卡片
- 不要在暗色背景上使用低对比度文字
- 不要过度使用动画效果

## 8. Responsive Behavior

### 断点策略
- **移动端** (< 576px): 单列布局，隐藏侧边栏
- **平板** (576-992px): 双列布局，可折叠侧边栏
- **桌面** (> 992px): 三列布局，固定侧边栏
- **大屏** (> 1600px): 固定最大宽度，居中布局

### 触摸目标
- 最小触摸区域: 44px × 44px
- 按钮最小高度: 32px
- 链接最小点击区域: 24px × 24px

## 9. Agent Prompt Guide

### 快速颜色参考
```
主色: #1890ff
成功: #52c41a
警告: #faad14
错误: #f5222d
文字: rgba(0, 0, 0, 0.85)
背景: #f0f2f5
```

### 设计系统提示词
```
使用外运物流控制塔设计系统创建UI组件：
- 主色调: #1890ff
- 卡片圆角: 12px
- 按钮圆角: 8px
- 间距系统: 8px倍数
- 字体: 系统字体栈
- 阴影: 0 3px 6px -4px rgba(0, 0, 0, 0.12)
```

### 组件生成示例
```
创建一个物流订单卡片：
- 使用Bg Component背景 (#ffffff)
- 添加12px圆角
- 应用base阴影
- 内部间距24px
- 标题使用H4样式
- 状态标签使用功能色
```

## 附录: 预览文件

- `preview.html` - 亮色主题预览
- `preview-dark.html` - 暗色主题预览

## 参考来源

本设计系统参考了以下优秀设计：
- Vercel - 黑白精确设计
- Linear - 超极简工程风格
- Stripe - 紫色渐变优雅风格
- Ant Design - 企业级UI规范

---

**更新日期**: 2026年4月15日
**版本**: 1.0.0
**适用项目**: 外运物流控制塔