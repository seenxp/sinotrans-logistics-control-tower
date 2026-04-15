# 外运物流控制塔 - 预测服务

基于TimesFM的时间序列预测服务，为物流控制塔提供智能预测能力。

## 功能特性

- 物流需求预测
- 运力需求预测
- 成本趋势预测
- 风险预警预测
- 多变量预测支持

## 技术栈

- **模型**: TimesFM 2.5 (200M参数)
- **框架**: FastAPI
- **深度学习**: PyTorch
- **数据处理**: Pandas + NumPy
- **可视化**: Matplotlib + Plotly

## 快速开始

### 环境要求
- Python 3.9+
- PyTorch 2.0+
- CUDA 11.8+ (可选，用于GPU加速)

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

3. 下载预训练模型
```bash
python download_model.py
```

4. 启动服务
```bash
python -m uvicorn prediction.app:app --reload --host 0.0.0.0 --port 8001
```

## 模型说明

### TimesFM 2.5
- **参数量**: 200M
- **上下文长度**: 最大16k
- **预测范围**: 最大1k
- **支持功能**: 点预测、分位数预测、协变量支持

### 预测类型
1. **需求预测**: 预测未来物流需求量
2. **运力预测**: 预测所需运力资源
3. **成本预测**: 预测物流成本趋势
4. **风险预测**: 预测潜在风险事件

## API接口

### 预测接口
```python
POST /api/v1/predict
```

请求体:
```json
{
  "data": [1.0, 2.0, 3.0, 4.0, 5.0],
  "horizon": 12,
  "frequency": "daily",
  "prediction_type": "demand"
}
```

响应:
```json
{
  "point_forecast": [6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0],
  "quantile_forecast": {
    "10": [5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5, 15.5, 16.5],
    "90": [6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5, 15.5, 16.5, 17.5]
  },
  "metadata": {
    "model": "timesfm-2.5-200m",
    "device": "cuda",
    "inference_time": 0.5
  }
}
```

### 批量预测
```python
POST /api/v1/predict/batch
```

### 模型信息
```python
GET /api/v1/models
```

### 健康检查
```python
GET /health
```

## 配置说明

### 环境变量
```bash
# 模型配置
TIMESFM_MODEL_PATH=google/timesfm-2.5-200m-pytorch
TIMESFM_DEVICE=cuda  # 或 cpu
TIMESFM_MAX_CONTEXT=1024
TIMESFM_MAX_HORIZON=256

# 服务配置
APP_HOST=0.0.0.0
APP_PORT=8001
APP_DEBUG=true

# 数据配置
DATA_DIR=./data
MODEL_DIR=./models
```

### 预测配置
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

PREDICTION_TYPES = {
    "demand": {
        "description": "物流需求预测",
        "features": ["历史订单量", "季节性", "促销活动"],
    },
    "capacity": {
        "description": "运力需求预测",
        "features": ["需求预测", "运力利用率", "天气条件"],
    },
    "cost": {
        "description": "成本趋势预测",
        "features": ["燃油价格", "人工成本", "设备维护"],
    },
    "risk": {
        "description": "风险预警预测",
        "features": ["天气预警", "交通状况", "政策变化"],
    },
}
```

## 数据格式

### 输入数据
```python
# 时间序列数据
time_series = [
    {"timestamp": "2024-01-01", "value": 100},
    {"timestamp": "2024-01-02", "value": 120},
    {"timestamp": "2024-01-03", "value": 110},
]

# 协变量数据
covariates = [
    {"timestamp": "2024-01-01", "weather": "sunny", "promotion": false},
    {"timestamp": "2024-01-02", "weather": "rainy", "promotion": true},
    {"timestamp": "2024-01-03", "weather": "cloudy", "promotion": false},
]
```

### 输出数据
```python
# 点预测
point_forecast = [130, 140, 150, 160, 170]

# 分位数预测
quantile_forecast = {
    "10": [120, 130, 140, 150, 160],
    "50": [130, 140, 150, 160, 170],
    "90": [140, 150, 160, 170, 180],
}
```

## 模型训练

### 数据准备
```python
# 准备训练数据
python prepare_data.py --input data/raw --output data/processed
```

### 模型微调
```python
# 微调模型
python fine_tune.py --data data/processed --model google/timesfm-2.5-200m-pytorch
```

### 模型评估
```python
# 评估模型
python evaluate.py --model models/fine_tuned --data data/test
```

## 性能优化

### GPU加速
```python
# 使用GPU加速
import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
```

### 批处理
```python
# 批量预测
batch_predictions = model.forecast_batch(batch_data)
```

### 缓存
```python
# 缓存预测结果
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_predict(data_hash, horizon):
    return model.forecast(data, horizon)
```

## 监控指标

### 系统指标
- 请求延迟
- 吞吐量
- 错误率
- GPU利用率

### 业务指标
- 预测准确率
- 预测覆盖率
- 预测及时性

## 故障排除

### 常见问题

1. 模型加载失败
   - 检查模型路径
   - 检查CUDA版本
   - 检查内存空间

2. 预测结果异常
   - 检查输入数据格式
   - 检查数据预处理
   - 检查模型配置

3. 性能问题
   - 启用GPU加速
   - 使用批处理
   - 优化数据预处理

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License

## 致谢

本服务基于Google Research的TimesFM项目，感谢开源社区的贡献。

- TimesFM仓库: https://github.com/google-research/timesfm
- 论文: A decoder-only foundation model for time-series forecasting, ICML 2024