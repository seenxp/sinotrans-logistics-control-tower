# 外运物流控制塔 - 设计系统

基于awesome-design-md的设计规范，为物流控制塔提供统一的设计语言。

## 设计理念

### 核心原则
1. **一致性** - 统一的设计语言，确保用户体验一致性
2. **效率性** - 高效的信息传达，减少认知负荷
3. **可访问性** - 支持所有用户，包括残障人士
4. **响应式** - 适配各种设备和屏幕尺寸

### 设计价值观
- **清晰** - 信息层次分明，易于理解
- **简洁** - 去除冗余，突出重点
- **专业** - 体现物流行业的专业性和可靠性
- **智能** - 展现AI驱动的智能化特性

## 设计令牌 (Design Tokens)

### 颜色系统
```scss
// 主色
$primary-100: #e6f7ff;
$primary-200: #bae7ff;
$primary-300: #91d5ff;
$primary-400: #69c0ff;
$primary-500: #1890ff;  // 主色
$primary-600: #096dd9;
$primary-700: #0050b3;
$primary-800: #003a8c;
$primary-900: #002766;

// 功能色
$success-color: #52c41a;
$warning-color: #faad14;
$error-color: #f5222d;
$info-color: #1890ff;

// 中性色
$gray-100: #fafafa;
$gray-200: #f5f5f5;
$gray-300: #e8e8e8;
$gray-400: #d9d9d9;
$gray-500: #bfbfbf;
$gray-600: #8c8c8c;
$gray-700: #595959;
$gray-800: #434343;
$gray-900: #262626;
$gray-1000: #1f1f1f;
$gray-1100: #141414;

// 语义色
$text-primary: rgba(0, 0, 0, 0.85);
$text-secondary: rgba(0, 0, 0, 0.65);
$text-disabled: rgba(0, 0, 0, 0.25);
$text-inverse: #ffffff;

$bg-base: #ffffff;
$bg-layout: #f0f2f5;
$bg-component: #ffffff;
$bg-mask: rgba(0, 0, 0, 0.45);

$border-color-base: #d9d9d9;
$border-color-split: #f0f0f0;
```

### 字体系统
```scss
// 字体族
$font-family-base: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
$font-family-number: 'DIN Alternate', 'DIN Alternate Bold', 'Roboto', sans-serif;
$font-family-chinese: 'PingFang SC', 'Microsoft YaHei', '微软雅黑', sans-serif;

// 字体大小
$font-size-xs: 12px;
$font-size-sm: 14px;
$font-size-base: 16px;
$font-size-lg: 20px;
$font-size-xl: 24px;
$font-size-xxl: 30px;
$font-size-display-1: 38px;
$font-size-display-2: 46px;
$font-size-display-3: 56px;

// 字体重量
$font-weight-light: 300;
$font-weight-regular: 400;
$font-weight-medium: 500;
$font-weight-semibold: 600;
$font-weight-bold: 700;

// 行高
$line-height-base: 1.5;
$line-height-lg: 2;
$line-height-sm: 1;

// 字母间距
$letter-spacing-base: 0;
$letter-spacing-wide: 0.5px;
$letter-spacing-wider: 1px;
```

### 间距系统
```scss
// 基础单位
$spacing-unit: 8px;

// 间距
$spacing-xs: 4px;   // 0.5倍
$spacing-sm: 8px;   // 1倍
$spacing-md: 16px;  // 2倍
$spacing-lg: 24px;  // 3倍
$spacing-xl: 32px;  // 4倍
$spacing-xxl: 48px; // 6倍

// 内边距
$padding-xs: 4px;
$padding-sm: 8px;
$padding-md: 16px;
$padding-lg: 24px;
$padding-xl: 32px;

// 外边距
$margin-xs: 4px;
$margin-sm: 8px;
$margin-md: 16px;
$margin-lg: 24px;
$margin-xl: 32px;
```

### 圆角系统
```scss
$border-radius-base: 4px;
$border-radius-sm: 2px;
$border-radius-lg: 8px;
$border-radius-xl: 12px;
$border-radius-xxl: 16px;
$border-radius-circle: 50%;
$border-radius-pill: 9999px;
```

### 阴影系统
```scss
$box-shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.03), 0 1px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px 0 rgba(0, 0, 0, 0.02);
$box-shadow-base: 0 3px 6px -4px rgba(0, 0, 0, 0.12), 0 6px 16px 0 rgba(0, 0, 0, 0.08), 0 9px 28px 8px rgba(0, 0, 0, 0.05);
$box-shadow-lg: 0 6px 16px 0 rgba(0, 0, 0, 0.08), 0 3px 6px -4px rgba(0, 0, 0, 0.12), 0 9px 28px 8px rgba(0, 0, 0, 0.05);
$box-shadow-xl: 0 9px 28px 8px rgba(0, 0, 0, 0.05), 0 6px 16px 0 rgba(0, 0, 0, 0.08), 0 3px 6px -4px rgba(0, 0, 0, 0.12);

$shadow-color: rgba(0, 0, 0, 0.15);
$shadow-color-light: rgba(0, 0, 0, 0.08);
```

### 动画系统
```scss
// 动画时长
$duration-fast: 0.1s;
$duration-normal: 0.2s;
$duration-slow: 0.3s;
$duration-slower: 0.4s;

// 动画曲线
$ease-base: cubic-bezier(0.645, 0.045, 0.355, 1);
$ease-in: cubic-bezier(0.12, 0, 0.39, 0);
$ease-out: cubic-bezier(0.61, 1, 0.88, 1);
$ease-in-out: cubic-bezier(0.37, 0, 0.63, 1);

// 动画延迟
$delay-fast: 0.05s;
$delay-normal: 0.1s;
$delay-slow: 0.15s;
```

## 组件库

### 基础组件
- **Button** - 按钮组件
- **Input** - 输入框组件
- **Select** - 选择器组件
- **Checkbox** - 复选框组件
- **Radio** - 单选框组件
- **Switch** - 开关组件
- **Slider** - 滑块组件
- **DatePicker** - 日期选择器
- **TimePicker** - 时间选择器

### 数据展示
- **Table** - 表格组件
- **Card** - 卡片组件
- **List** - 列表组件
- **Tree** - 树形组件
- **Tabs** - 标签页组件
- **Tag** - 标签组件
- **Badge** - 徽标组件
- **Avatar** - 头像组件
- **Tooltip** - 文字提示

### 反馈
- **Alert** - 警告提示
- **Message** - 全局提示
- **Notification** - 通知提醒
- **Modal** - 对话框
- **Drawer** - 抽屉
- **Progress** - 进度条
- **Skeleton** - 骨架屏
- **Spin** - 加载中

### 导航
- **Menu** - 导航菜单
- **Breadcrumb** - 面包屑
- **Pagination** - 分页
- **Steps** - 步骤条
- **Dropdown** - 下拉菜单

### 业务组件
- **KPIWidget** - KPI指标组件
- **AlertCard** - 预警卡片
- **Timeline** - 时间线
- **PredictChart** - 预测图表
- **OrderTrack** - 订单跟踪
- **Map3D** - 3D地图组件
- **Gauge** - 仪表盘组件

## 页面模板

### 控制塔大屏
- 全球物流网络监控
- 实时运力监控
- 异常事件预警
- KPI指标展示

### 预测分析中心
- 需求预测分析
- 运力预测分析
- 成本预测分析
- 风险预测分析

### 运营指挥中心
- 实时订单跟踪
- 运力调度优化
- 异常事件处理
- 资源优化配置

### 数据治理中心
- 数据质量监控
- 数据血缘追踪
- 数据安全管控
- 数据服务管理

## 设计资源

### 图标库
- **基础图标** - 线性图标，24x24
- **业务图标** - 物流行业专用图标
- **状态图标** - 表示不同状态的图标
- **动效图标** - 带动画的图标

### 插图库
- **空状态插图** - 表示空数据状态
- **错误插图** - 表示错误状态
- **成功插图** - 表示成功状态
- **引导插图** - 用户引导插图

### 图表样式
- **折线图** - 趋势分析
- **柱状图** - 对比分析
- **饼图** - 占比分析
- **地图** - 地理分布
- **仪表盘** - 指标监控

## 主题系统

### 亮色主题
```typescript
export const lightTheme = {
  colors: {
    primary: '#1890ff',
    success: '#52c41a',
    warning: '#faad14',
    error: '#f5222d',
    info: '#1890ff',
    background: '#ffffff',
    surface: '#fafafa',
    text: {
      primary: 'rgba(0, 0, 0, 0.85)',
      secondary: 'rgba(0, 0, 0, 0.65)',
      disabled: 'rgba(0, 0, 0, 0.25)',
    },
    border: '#d9d9d9',
  },
  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.03)',
    base: '0 3px 6px -4px rgba(0, 0, 0, 0.12)',
    lg: '0 6px 16px 0 rgba(0, 0, 0, 0.08)',
  },
};
```

### 暗色主题
```typescript
export const darkTheme = {
  colors: {
    primary: '#177ddc',
    success: '#49aa19',
    warning: '#d89614',
    error: '#a61d24',
    info: '#177ddc',
    background: '#141414',
    surface: '#1f1f1f',
    text: {
      primary: 'rgba(255, 255, 255, 0.85)',
      secondary: 'rgba(255, 255, 255, 0.65)',
      disabled: 'rgba(255, 255, 255, 0.25)',
    },
    border: '#434343',
  },
  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.16)',
    base: '0 3px 6px -4px rgba(0, 0, 0, 0.48)',
    lg: '0 6px 16px 0 rgba(0, 0, 0, 0.32)',
  },
};
```

## 设计工具

### 设计软件
- **Figma** - UI/UX设计
- **Sketch** - 矢量图形设计
- **Adobe XD** - 原型设计

### 开发工具
- **Storybook** - 组件开发环境
- **Styleguidist** - 样式指南
- **Chromatic** - 视觉回归测试

### 文档工具
- **Docusaurus** - 文档网站
- **VuePress** - Vue文档工具
- **GitBook** - 技术文档

## 设计流程

### 1. 需求分析
- 用户研究
- 竞品分析
- 需求文档

### 2. 设计阶段
- 线框图设计
- 视觉设计
- 交互设计
- 原型制作

### 3. 开发阶段
- 组件开发
- 页面实现
- 测试验证

### 4. 优化阶段
- 用户反馈
- 性能优化
- 体验优化

## 设计规范

### 命名规范
- **组件名** - PascalCase (如: KPIWidget)
- **类名** - kebab-case (如: kpi-widget)
- **变量名** - camelCase (如: kpiWidget)
- **常量名** - UPPER_SNAKE_CASE (如: KPI_WIDGET)

### 文件结构
```
components/
├── Button/
│   ├── Button.tsx
│   ├── Button.scss
│   ├── Button.stories.tsx
│   ├── Button.test.tsx
│   └── index.ts
├── Input/
│   ├── Input.tsx
│   ├── Input.scss
│   ├── Input.stories.tsx
│   ├── Input.test.tsx
│   └── index.ts
└── index.ts
```

### 代码规范
- 使用TypeScript严格模式
- 使用ESLint + Prettier
- 遵循组件化开发原则
- 编写单元测试和文档

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License

## 致谢

本设计系统基于awesome-design-md项目的设计理念，感谢开源社区的贡献。

- awesome-design-md仓库: https://github.com/VoltAgent/awesome-design-md
- Google Stitch DESIGN.md: https://stitch.withgoogle.com/docs/design-md/overview/