# 外运物流控制塔 - 后端服务

基于FastAPI的智能物流控制塔后端服务。

## 功能特性

- RESTful API 接口
- 实时数据流处理
- 预测模型集成
- 数据治理服务
- 用户认证授权

## 技术栈

- **框架**: FastAPI
- **数据库**: PostgreSQL + TimescaleDB
- **缓存**: Redis
- **消息队列**: RabbitMQ
- **AI服务**: TimesFM + PyTorch
- **认证**: JWT + OAuth 2.0

## 快速开始

### 环境要求
- Python 3.9+
- PostgreSQL 14+
- Redis 7+

### 安装步骤

1. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件
```

4. 初始化数据库
```bash
python -m alembic upgrade head
```

5. 启动服务
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API文档

启动服务后访问:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 项目结构

```
backend/
├── app/
│   ├── api/            # API接口
│   │   ├── v1/        # API版本1
│   │   └── deps.py    # 依赖注入
│   ├── core/           # 核心配置
│   │   ├── config.py  # 配置管理
│   │   ├── security.py # 安全相关
│   │   └── logging.py # 日志配置
│   ├── models/         # 数据模型
│   │   ├── user.py    # 用户模型
│   │   ├── order.py   # 订单模型
│   │   └── prediction.py # 预测模型
│   ├── services/       # 业务逻辑
│   │   ├── auth.py    # 认证服务
│   │   ├── order.py   # 订单服务
│   │   └── prediction.py # 预测服务
│   ├── utils/          # 工具函数
│   │   ├── database.py # 数据库工具
│   │   ├── cache.py   # 缓存工具
│   │   └── helpers.py # 辅助函数
│   └── main.py         # 应用入口
├── alembic/            # 数据库迁移
├── tests/              # 测试代码
├── requirements.txt    # 依赖列表
├── .env.example        # 环境变量示例
└── README.md
```

## 配置说明

### 环境变量
```bash
# 数据库
DATABASE_URL=postgresql://user:password@localhost:5432/logistics_control_tower

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# TimesFM
TIMESFM_MODEL_PATH=google/timesfm-2.5-200m-pytorch
TIMESFM_DEVICE=cuda

# 应用
APP_ENV=development
APP_DEBUG=true
```

## 开发指南

### 代码规范
- 使用 Black 格式化代码
- 使用 isort 排序导入
- 使用 flake8 检查代码风格

### 测试
```bash
# 运行测试
pytest

# 生成测试覆盖率报告
pytest --cov=app tests/
```

### 数据库迁移
```bash
# 创建迁移
alembic revision --autogenerate -m "description"

# 应用迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

## 部署

### Docker部署
```bash
# 构建镜像
docker build -t logistics-control-tower-backend .

# 运行容器
docker run -d -p 8000:8000 logistics-control-tower-backend
```

### 生产环境
```bash
# 使用gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## 监控

### 健康检查
```bash
curl http://localhost:8000/health
```

### 指标监控
- Prometheus: http://localhost:8000/metrics
- Grafana: 配置Prometheus数据源

## 故障排除

### 常见问题

1. 数据库连接失败
   - 检查DATABASE_URL配置
   - 确保PostgreSQL服务运行中

2. Redis连接失败
   - 检查REDIS_URL配置
   - 确保Redis服务运行中

3. 模型加载失败
   - 检查TIMESFM_MODEL_PATH配置
   - 确保模型文件存在

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License