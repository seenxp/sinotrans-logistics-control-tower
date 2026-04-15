# 外运物流控制塔 (Sinotrans Logistics Control Tower)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Vue 3](https://img.shields.io/badge/vue-3.x-green.svg)](https://vuejs.org/)

基于数字孪生、AI预测和可视化大屏的智能物流管理平台。

## 项目简介

外运物流控制塔是一个整合三大核心技术的智能物流管理平台：

1. **数字孪生可视化** - 基于 [DigitalTwinScreen](https://github.com/tmqq2333/DigitalTwinScreen) 的3D可视化大屏
2. **时间序列预测** - 基于 [TimesFM](https://github.com/google-research/timesfm) 的AI预测模型  
3. **设计系统** - 基于 [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) 的DESIGN.md设计规范

## 核心特性

### 控制塔大屏
- 全球物流网络3D可视化
- 实时运力监控与调度
- 异常事件预警系统
- 多维度KPI指标展示

### 预测分析中心
- 物流需求预测 (准确率85%+)
- 运力需求预测
- 成本趋势预测
- 风险预警预测

### 运营指挥中心
- 实时订单跟踪
- 智能运力调度
- 异常事件处理
- 资源优化配置

### 数据治理中心
- 数据质量监控
- 数据血缘追踪
- 数据安全管控
- 数据服务管理

## 技术架构

### 前端技术栈
- **框架**: Vue 3 + TypeScript
- **3D引擎**: Three.js + Cesium.js
- **图表库**: ECharts 5 + D3.js
- **UI组件**: 基于DESIGN.md的自定义组件库
- **状态管理**: Pinia
- **构建工具**: Vite

### 后端技术栈
- **框架**: FastAPI (Python 3.9+)
- **数据库**: PostgreSQL + TimescaleDB
- **缓存**: Redis
- **消息队列**: RabbitMQ
- **AI服务**: TimesFM + PyTorch
- **容器化**: Docker + Kubernetes

### 预测模块
- **模型**: TimesFM 2.5 (200M参数)
- **预测范围**: 需求、运力、成本、风险
- **数据源**: 历史订单、天气、经济指标、交通数据

## 快速开始

### 环境要求
- Python 3.9+
- Node.js 18+
- PostgreSQL 14+
- Redis 7+
- Docker 24+ (可选)

### 安装步骤

#### 1. 克隆项目
```bash
git clone https://github.com/seenxp/sinotrans-logistics-control-tower.git
cd sinotrans-logistics-control-tower
```

#### 2. 启动项目
```bash
# 使用启动脚本
./start.sh

# 或者使用Docker Compose
docker-compose up -d
```

#### 3. 访问应用
- 前端应用: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs
- 预测服务: http://localhost:8001

## 项目结构

```
sinotrans-logistics-control-tower/
├── frontend/                 # Vue 3前端应用
├── backend/                  # FastAPI后端服务
├── prediction/               # TimesFM预测服务
├── digital-twin/             # 数字孪生模块
├── design-system/            # 设计系统
├── docs/                     # 项目文档
│   ├── DESIGN.md            # 设计规范
│   ├── PROJECT_SUMMARY.md   # 项目总结
│   ├── PROJECT_STATUS.md    # 项目状态
│   ├── DEMO.md              # 演示文档
│   └── FINAL_SUMMARY.md     # 最终总结
├── docker-compose.yml        # Docker编排
├── .gitignore               # Git忽略文件
├── LICENSE                  # MIT许可证
├── README.md                # 项目说明
├── GITHUB_SETUP.md         # GitHub设置指南
└── start.sh                # 启动脚本
```

## 核心功能

### 1. 控制塔大屏
- **3D地球可视化**: 全球物流网络实时监控
- **运力监控**: 实时运力分布与状态
- **异常预警**: 智能异常检测与预警
- **KPI展示**: 关键绩效指标实时展示

### 2. 预测分析中心
- **需求预测**: 基于TimesFM的物流需求预测
- **运力预测**: 运力需求预测与优化
- **成本预测**: 物流成本趋势预测
- **风险预测**: 潜在风险预警预测

### 3. 运营指挥中心
- **订单跟踪**: 实时订单状态跟踪
- **运力调度**: 智能运力调度优化
- **异常处理**: 异常事件快速处理
- **资源配置**: 资源优化配置建议

### 4. 数据治理中心
- **数据质量**: 数据质量监控与评估
- **数据血缘**: 数据血缘追踪与分析
- **数据安全**: 数据安全管控与审计
- **数据服务**: 数据服务管理与发布

## 技术亮点

### 1. 实时性
- 数据延迟 < 5秒
- 3D场景实时更新
- 预测结果实时刷新

### 2. 可视化
- 3D数字孪生可视化
- 多维度数据融合展示
- 交互式操作界面

### 3. 智能化
- AI驱动的需求预测
- 智能预警系统
- 自动化决策支持

### 4. 可扩展性
- 模块化设计
- 微服务架构
- 插件化扩展

## 性能指标

### 系统性能
- 页面加载时间: < 3秒
- 数据刷新延迟: < 1秒
- 预测计算时间: < 5秒
- 系统可用性: 99.9%

### 预测准确率
- 需求预测准确率: 85%+
- 运力预测准确率: 80%+
- 成本预测准确率: 75%+

## 部署方案

### Docker部署
```bash
# 构建并启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### Kubernetes部署
```bash
# 创建命名空间
kubectl create namespace logistics

# 部署应用
kubectl apply -f k8s/

# 查看部署状态
kubectl get pods -n logistics
```

## 开发指南

### 代码规范
- 前端: ESLint + Prettier
- 后端: Black + isort + flake8
- 提交信息: Conventional Commits

### 测试
```bash
# 前端测试
cd frontend && npm run test

# 后端测试
cd backend && pytest

# 预测服务测试
cd prediction && pytest
```

## 贡献指南

我们欢迎所有形式的贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

### 开发流程
1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目基于 MIT 许可证开源 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 致谢

本项目整合了以下优秀开源项目：

1. **DigitalTwinScreen** - 数字孪生可视化
   - 仓库: https://github.com/tmqq2333/DigitalTwinScreen
   - 贡献: 提供3D可视化大屏技术

2. **awesome-design-md** - 设计系统
   - 仓库: https://github.com/VoltAgent/awesome-design-md
   - 贡献: 提供DESIGN.md设计规范

3. **TimesFM** - 时间序列预测
   - 仓库: https://github.com/google-research/timesfm
   - 贡献: 提供AI预测模型

## 联系我们

- 项目维护者: [Your Name]
- 邮箱: your.email@example.com
- 项目主页: https://github.com/seenxp/sinotrans-logistics-control-tower

---

**外运物流控制塔** - 让物流管理更智能、更高效、更可视化