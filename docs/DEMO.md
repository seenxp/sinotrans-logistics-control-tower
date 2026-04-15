# 外运物流控制塔项目演示

## 概述
外运物流控制塔是一个基于数字孪生、AI预测和可视化大屏的智能物流管理平台。本文档展示项目的核心功能和演示方法。

## 演示环境

### 快速启动
```bash
# 克隆项目
git clone https://github.com/seenxp/sinotrans-logistics-control-tower.git
cd sinotrans-logistics-control-tower

# 启动项目
./start.sh

# 或者使用Docker Compose
docker-compose up -d
```

### 访问地址
- **前端应用**: http://localhost:3000
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **预测服务**: http://localhost:8001

## 核心功能演示

### 1. 控制塔大屏演示

#### 功能展示
- **3D地球可视化**: 全球物流网络实时监控
- **运力监控**: 实时运力分布与状态
- **异常预警**: 智能异常检测与预警
- **KPI展示**: 关键绩效指标实时展示

#### 演示步骤
1. 访问 http://localhost:3000
2. 点击"控制塔大屏"菜单
3. 查看3D地球可视化
4. 查看实时运力分布
5. 查看异常事件预警

#### 演示数据
```json
{
  "vehicles": [
    {
      "id": "truck-001",
      "type": "truck",
      "position": {"lat": 39.9042, "lng": 116.4074},
      "status": "active",
      "speed": 60,
      "destination": "上海仓库"
    },
    {
      "id": "ship-001",
      "type": "ship",
      "position": {"lat": 31.2304, "lng": 121.4737},
      "status": "active",
      "speed": 20,
      "destination": "深圳港口"
    }
  ],
  "warehouses": [
    {
      "id": "warehouse-beijing",
      "name": "北京仓库",
      "position": {"lat": 39.9042, "lng": 116.4074},
      "capacity": 10000,
      "current": 7500
    }
  ]
}
```

### 2. 预测分析中心演示

#### 功能展示
- **需求预测**: 基于TimesFM的物流需求预测
- **运力预测**: 运力需求预测与优化
- **成本预测**: 物流成本趋势预测
- **风险预测**: 潜在风险预警预测

#### 演示步骤
1. 访问 http://localhost:3000
2. 点击"预测分析中心"菜单
3. 选择预测类型
4. 输入历史数据
5. 查看预测结果

#### API演示
```bash
# 需求预测
curl -X POST http://localhost:8001/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "data": [100, 120, 110, 130, 140, 150, 160, 170, 180, 190],
    "horizon": 7,
    "frequency": "daily",
    "prediction_type": "demand"
  }'

# 批量预测
curl -X POST http://localhost:8001/api/v1/predict/batch \
  -H "Content-Type: application/json" \
  -d '{
    "datasets": [
      {
        "name": "需求预测",
        "data": [100, 120, 110, 130, 140]
      },
      {
        "name": "成本预测",
        "data": [1000, 1100, 1050, 1200, 1150]
      }
    ],
    "horizon": 7
  }'
```

### 3. 运营指挥中心演示

#### 功能展示
- **订单跟踪**: 实时订单状态跟踪
- **运力调度**: 智能运力调度优化
- **异常处理**: 异常事件快速处理
- **资源配置**: 资源优化配置建议

#### 演示步骤
1. 访问 http://localhost:3000
2. 点击"运营指挥中心"菜单
3. 查看订单跟踪
4. 查看运力调度
5. 查看异常处理

#### 演示数据
```json
{
  "orders": [
    {
      "id": "order-001",
      "customer": "客户A",
      "status": "运输中",
      "origin": "北京仓库",
      "destination": "上海客户",
      "estimated_arrival": "2026-04-16 14:00:00",
      "vehicle": "truck-001"
    }
  ],
  "alerts": [
    {
      "id": "alert-001",
      "type": "延迟",
      "severity": "中等",
      "message": "订单order-001预计延迟2小时",
      "timestamp": "2026-04-15 10:00:00"
    }
  ]
}
```

### 4. 数据治理中心演示

#### 功能展示
- **数据质量**: 数据质量监控与评估
- **数据血缘**: 数据血缘追踪与分析
- **数据安全**: 数据安全管控与审计
- **数据服务**: 数据服务管理与发布

#### 演示步骤
1. 访问 http://localhost:3000
2. 点击"数据治理中心"菜单
3. 查看数据质量报告
4. 查看数据血缘图
5. 查看数据安全审计

## 技术演示

### 1. 3D可视化演示

#### Three.js演示
```javascript
// 创建3D场景
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// 添加车辆模型
const loader = new THREE.GLTFLoader();
loader.load('models/truck.glb', (gltf) => {
  scene.add(gltf.scene);
});

// 动画循环
function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}
animate();
```

#### Cesium.js演示
```javascript
// 初始化Cesium
const viewer = new Cesium.Viewer('cesiumContainer', {
  terrainProvider: Cesium.createWorldTerrain(),
});

// 添加物流点
viewer.entities.add({
  position: Cesium.Cartesian3.fromDegrees(116.3974, 39.9093, 0),
  point: {
    pixelSize: 10,
    color: Cesium.Color.RED,
  },
  label: {
    text: '北京仓库',
    font: '14pt sans-serif',
  },
});
```

### 2. 预测服务演示

#### TimesFM演示
```python
import torch
import numpy as np
import timesfm

# 加载模型
model = timesfm.TimesFM_2p5_200M_torch.from_pretrained("google/timesfm-2.5-200m-pytorch")

# 配置预测参数
model.compile(
    timesfm.ForecastConfig(
        max_context=1024,
        max_horizon=256,
        normalize_inputs=True,
        use_continuous_quantile_head=True,
        force_flip_invariance=True,
        infer_is_positive=True,
        fix_quantile_crossing=True,
    )
)

# 进行预测
point_forecast, quantile_forecast = model.forecast(
    horizon=12,
    inputs=[
        np.linspace(0, 1, 100),
        np.sin(np.linspace(0, 20, 67)),
    ],
)

print(f"点预测形状: {point_forecast.shape}")  # (2, 12)
print(f"分位数预测形状: {quantile_forecast.shape}")  # (2, 12, 10)
```

### 3. 设计系统演示

#### 组件演示
```vue
<template>
  <div class="kpi-widget">
    <div class="kpi-title">{{ title }}</div>
    <div class="kpi-value">{{ value }}</div>
    <div class="kpi-trend" :class="trendClass">
      <span>{{ trendText }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title: string
  value: number | string
  trend: 'up' | 'down' | 'stable'
}

const props = defineProps<Props>()

const trendClass = computed(() => {
  return {
    'trend-up': props.trend === 'up',
    'trend-down': props.trend === 'down',
    'trend-stable': props.trend === 'stable',
  }
})

const trendText = computed(() => {
  const texts = {
    up: '↑ 上升',
    down: '↓ 下降',
    stable: '→ 稳定',
  }
  return texts[props.trend]
})
</script>

<style scoped>
.kpi-widget {
  padding: 16px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.kpi-title {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.kpi-value {
  font-size: 32px;
  font-weight: bold;
  color: #1890ff;
}

.kpi-trend {
  font-size: 12px;
  margin-top: 8px;
}

.trend-up {
  color: #52c41a;
}

.trend-down {
  color: #f5222d;
}

.trend-stable {
  color: #666;
}
</style>
```

## 性能演示

### 1. 响应时间测试
```bash
# 测试后端API响应时间
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/health

# 测试预测服务响应时间
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8001/health
```

### 2. 并发测试
```bash
# 使用ab进行并发测试
ab -n 1000 -c 100 http://localhost:8000/api/v1/orders
```

### 3. 内存使用监控
```bash
# 查看Docker容器资源使用
docker stats

# 查看系统资源使用
htop
```

## 部署演示

### 1. Docker部署
```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 2. Kubernetes部署
```bash
# 创建命名空间
kubectl create namespace logistics

# 部署应用
kubectl apply -f k8s/

# 查看部署状态
kubectl get pods -n logistics
```

## 故障排除

### 常见问题

1. **服务启动失败**
   ```bash
   # 查看日志
   docker-compose logs [服务名]
   
   # 检查端口占用
   netstat -tulpn | grep [端口号]
   
   # 重启服务
   docker-compose restart [服务名]
   ```

2. **数据库连接失败**
   ```bash
   # 检查数据库状态
   docker-compose exec postgres psql -U postgres
   
   # 检查连接字符串
   echo $DATABASE_URL
   ```

3. **模型加载失败**
   ```bash
   # 检查模型文件
   ls -la prediction/models/
   
   # 检查CUDA状态
   python -c "import torch; print(torch.cuda.is_available())"
   ```

## 总结

外运物流控制塔项目提供了完整的演示环境，包括：

1. **控制塔大屏**: 3D可视化全球物流网络
2. **预测分析中心**: AI驱动的需求预测
3. **运营指挥中心**: 智能运力调度
4. **数据治理中心**: 数据质量管控

通过本文档的演示步骤，可以全面了解项目的功能和特性。

---

*演示文档版本: v1.0*
*最后更新: 2026年4月15日*