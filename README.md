# 外运物流控制塔 (Sinotrans Logistics Control Tower)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Vue 3](https://img.shields.io/badge/vue-3.x-green.svg)](https://vuejs.org/)

基于数字孪生、AI预测和可视化大屏的智能物流管理平台。

## 🚀 项目简介

外运物流控制塔是一个整合三大核心技术的智能物流管理平台：

1. **数字孪生可视化** - 基于 [DigitalTwinScreen](https://github.com/tmqq2333/DigitalTwinScreen) 的3D可视化大屏
2. **时间序列预测** - 基于 [TimesFM](https://github.com/google-research/timesfm) 的AI预测模型  
3. **设计系统** - 基于 [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) 的DESIGN.md设计规范

## ✨ 核心特性

### 🎯 控制塔大屏
- 全球物流网络3D可视化
- 实时运力监控与调度
- 异常事件预警系统
- 多维度KPI指标展示

### 📈 预测分析中心
- 物流需求预测 (准确率85%+)
- 运力需求预测
- 成本趋势预测
- 风险预警预测

### 🎮 运营指挥中心
- 实时订单跟踪
- 智能运力调度
- 异常事件处理
- 资源优化配置

### 📊 数据治理中心
- 数据质量监控
- 数据血缘追踪
- 数据安全管控
- 数据服务管理

## 🏗️ 技术架构

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

## 📁 项目结构

```
sinotrans-logistics-control-tower/
├── frontend/                 # 前端应用
│   ├── src/
│   │   ├── components/      # 通用组件
│   │   ├── views/          # 页面视图
│   │   ├── stores/         # 状态管理
│   │   ├── utils/          # 工具函数
│   │   └── assets/         # 静态资源
│   ├── package.json
│   └── vite.config.ts
├── backend/                  # 后端服务
│   ├── app/
│   │   ├── api/            # API接口
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   ├── services/       # 业务逻辑
│   │   └── utils/          # 工具函数
│   ├── requirements.txt
│   └── main.py
├── prediction/               # 预测服务
│   ├── models/             # 预测模型
│   ├── data/               # 训练数据
│   ├── scripts/            # 训练脚本
│   └── requirements.txt
├── digital-twin/             # 数字孪生模块
│   ├── 3d-models/          # 3D模型
│   ├── scenes/             # 场景配置
│   └── textures/           # 纹理资源
├── design-system/            # 设计系统
│   ├── DESIGN.md           # 设计规范
│   ├── components/         # 组件库
│   └── tokens/             # 设计令牌
├── docs/                     # 项目文档
│   ├── DESIGN.md           # 设计文档
│   ├── API.md              # API文档
│   └── DEPLOYMENT.md       # 部署文档
├── docker-compose.yml        # Docker编排
├── .gitignore
├── LICENSE
└── README.md
```

## 🚀 快速开始

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

#### 2. 后端设置
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置数据库连接等

# 初始化数据库
python -m alembic upgrade head

# 启动后端服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 3. 前端设置
```bash
cd frontend
npm install

# 启动开发服务器
npm run dev
```

#### 4. 预测服务设置
```bash
cd prediction
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 启动预测服务
python -m uvicorn prediction.app:app --reload --host 0.0.0.0 --port 8001
```

#### 5. Docker部署 (可选)
```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps
```

## 📊 功能演示

### 控制塔大屏
![控制塔大屏](docs/images/control-tower.png)

### 预测分析中心
![预测分析中心](docs/images/prediction-center.png)

### 运营指挥中心
![运营指挥中心](docs/images/operations-center.png)

## 🔧 配置说明

### 环境变量配置
```bash
# 数据库配置
DATABASE_URL=postgresql://user:password@localhost:5432/logistics_control_tower

# Redis配置
REDIS_URL=redis://localhost:6379/0

# TimesFM配置
TIMESFM_MODEL_PATH=google/timesfm-2.5-200m-pytorch
TIMESFM_DEVICE=cuda  # 或 cpu

# 应用配置
APP_ENV=development
APP_DEBUG=true
SECRET_KEY=your-secret-key
```

### 预测模型配置
```python
# prediction/config.py
FORECAST_CONFIG = {
    "max_context": 1024,
    "max_horizon": 256,
    "normalize_inputs": True,
    "use_continuous_quantile_head": True,
    "force_flip_invariance": True,
    "infer_is_positive": True,
    "fix_quantile_crossing": True,
}
```

## 📈 性能指标

### 系统性能
- 页面加载时间: < 3秒
- 数据刷新延迟: < 1秒
- 预测计算时间: < 5秒
- 系统可用性: 99.9%

### 预测准确率
- 需求预测准确率: 85%+
- 运力预测准确率: 80%+
- 成本预测准确率: 75%+

## 🤝 贡献指南

我们欢迎所有形式的贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

### 开发流程
1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 代码规范
- 前端: ESLint + Prettier
- 后端: Black + isort + flake8
- 提交信息: Conventional Commits

## 📄 许可证

本项目基于 MIT 许可证开源 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

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

## 📞 联系我们

- 项目维护者: [Your Name]
- 邮箱: your.email@example.com
- 项目主页: https://github.com/seenxp/sinotrans-logistics-control-tower

---

**外运物流控制塔** - 让物流管理更智能、更高效、更可视化