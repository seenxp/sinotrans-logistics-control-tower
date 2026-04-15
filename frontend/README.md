# 外运物流控制塔 - 前端应用

基于Vue 3 + TypeScript的智能物流控制塔前端应用。

## 功能特性

- 3D数字孪生可视化
- 实时数据监控
- 预测分析展示
- 响应式设计
- 主题定制

## 技术栈

- **框架**: Vue 3 + TypeScript
- **3D引擎**: Three.js + Cesium.js
- **图表库**: ECharts 5 + D3.js
- **UI组件**: 自定义组件库
- **状态管理**: Pinia
- **构建工具**: Vite
- **样式**: SCSS + CSS Variables

## 快速开始

### 环境要求
- Node.js 18+
- npm 9+ 或 yarn 1.22+

### 安装步骤

1. 安装依赖
```bash
npm install
# 或
yarn install
```

2. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件
```

3. 启动开发服务器
```bash
npm run dev
# 或
yarn dev
```

4. 构建生产版本
```bash
npm run build
# 或
yarn build
```

## 项目结构

```
frontend/
├── src/
│   ├── assets/          # 静态资源
│   │   ├── images/     # 图片资源
│   │   ├── styles/     # 样式文件
│   │   └── fonts/      # 字体文件
│   ├── components/      # 通用组件
│   │   ├── common/     # 基础组件
│   │   ├── charts/     # 图表组件
│   │   ├── 3d/         # 3D组件
│   │   └── business/   # 业务组件
│   ├── views/          # 页面视图
│   │   ├── dashboard/  # 控制塔大屏
│   │   ├── prediction/ # 预测分析
│   │   ├── operations/ # 运营指挥
│   │   └── data/       # 数据治理
│   ├── stores/         # 状态管理
│   │   ├── user.ts     # 用户状态
│   │   ├── order.ts    # 订单状态
│   │   └── prediction.ts # 预测状态
│   ├── router/         # 路由配置
│   ├── services/       # API服务
│   ├── utils/          # 工具函数
│   ├── composables/    # 组合式函数
│   ├── types/          # 类型定义
│   ├── App.vue         # 根组件
│   └── main.ts         # 入口文件
├── public/             # 静态文件
├── index.html          # HTML模板
├── vite.config.ts      # Vite配置
├── tsconfig.json       # TypeScript配置
├── package.json        # 项目配置
└── README.md
```

## 组件库

### 基础组件
- `BaseButton` - 按钮组件
- `BaseInput` - 输入框组件
- `BaseSelect` - 选择器组件
- `BaseTable` - 表格组件
- `BaseModal` - 模态框组件

### 图表组件
- `LineChart` - 折线图
- `BarChart` - 柱状图
- `PieChart` - 饼图
- `MapChart` - 地图图表
- `GaugeChart` - 仪表盘

### 3D组件
- `Map3D` - 3D地图
- `Model3D` - 3D模型
- `Scene3D` - 3D场景
- `Particle3D` - 粒子效果

### 业务组件
- `KPIWidget` - KPI组件
- `AlertCard` - 预警卡片
- `Timeline` - 时间线
- `PredictChart` - 预测图表
- `OrderTrack` - 订单跟踪

## 设计系统

基于DESIGN.md的设计规范，包含：

### 设计令牌 (Design Tokens)
```scss
// 颜色
$primary-color: #1890ff;
$success-color: #52c41a;
$warning-color: #faad14;
$error-color: #f5222d;
$neutral-color: #8c8c8c;

// 字体
$font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto;
$font-family-number: 'DIN Alternate', 'DIN Alternate Bold';

// 间距
$spacing-unit: 8px;
$spacing-small: 8px;
$spacing-medium: 16px;
$spacing-large: 24px;

// 圆角
$border-radius-small: 4px;
$border-radius-medium: 8px;
$border-radius-large: 12px;

// 阴影
$box-shadow-small: 0 2px 8px rgba(0, 0, 0, 0.15);
$box-shadow-medium: 0 4px 16px rgba(0, 0, 0, 0.15);
$box-shadow-large: 0 8px 24px rgba(0, 0, 0, 0.15);
```

### 主题配置
```typescript
// src/theme/theme.ts
export const theme = {
  light: {
    primary: '#1890ff',
    background: '#ffffff',
    text: '#333333',
  },
  dark: {
    primary: '#177ddc',
    background: '#141414',
    text: '#ffffff',
  },
};
```

## 配置说明

### 环境变量
```bash
# API配置
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_WS_BASE_URL=ws://localhost:8000/ws

# 地图配置
VITE_CESIUM_ION_TOKEN=your-cesium-ion-token

# 预测服务
VITE_PREDICTION_API_URL=http://localhost:8001/api/v1

# 应用配置
VITE_APP_TITLE=外运物流控制塔
VITE_APP_ENV=development
```

### Vite配置
```typescript
// vite.config.ts
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
});
```

## 开发指南

### 代码规范
- 使用 ESLint + Prettier
- 使用 TypeScript 严格模式
- 遵循 Vue 3 组合式 API 风格

### 提交规范
```bash
# 功能
git commit -m "feat: 添加新功能"

# 修复
git commit -m "fix: 修复问题"

# 文档
git commit -m "docs: 更新文档"

# 样式
git commit -m "style: 代码格式调整"

# 重构
git commit -m "refactor: 代码重构"

# 测试
git commit -m "test: 添加测试"

# 构建
git commit -m "build: 构建相关"
```

### 测试
```bash
# 运行单元测试
npm run test:unit

# 运行端到端测试
npm run test:e2e

# 生成测试覆盖率
npm run test:coverage
```

## 构建部署

### 开发环境
```bash
npm run dev
```

### 生产环境
```bash
# 构建
npm run build

# 预览构建结果
npm run preview

# 部署到服务器
npm run deploy
```

### Docker部署
```dockerfile
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 性能优化

### 代码分割
- 路由懒加载
- 组件异步加载
- 第三方库按需加载

### 资源优化
- 图片压缩
- 字体子集化
- 代码压缩

### 缓存策略
- 浏览器缓存
- Service Worker
- 本地存储

## 故障排除

### 常见问题

1. 依赖安装失败
   - 清除npm缓存: `npm cache clean --force`
   - 删除node_modules: `rm -rf node_modules package-lock.json`

2. 构建失败
   - 检查Node.js版本
   - 检查TypeScript类型错误

3. 3D渲染问题
   - 检查WebGL支持
   - 检查显卡驱动

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License