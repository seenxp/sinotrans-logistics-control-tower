# 物流AI控制塔 Grafana Dashboard 使用指南

## 📋 Dashboard 概览

已生成完整的 Grafana Dashboard JSON，包含 **19个面板**：

### 面板布局
```
+--------------------------------------------------+
|  📊 核心运营指标 (Row)                            |
|  [总在途量] [OTD准时率] [AI处理率] [成本节省]     |
+--------------------------------------------------+
|  🗺️ 运力分布地图 (Row)                           |
|  [实时车辆GPS地图]  [仓库利用率热力图]            |
+--------------------------------------------------+
|  📈 趋势分析 (Row)                               |
|  [OTD趋势图]      [延误趋势图]                   |
+--------------------------------------------------+
|  [Escalation漏斗] [风险仪表] [AI建议表格]         |
+--------------------------------------------------+
|  [Top异常条形图]  [承运商绩效表格]                |
+--------------------------------------------------+
|  [运单状态饼图] [库存预警] [系统健康监控]         |
+--------------------------------------------------+
```

---

## 🚀 一、如何导入到 Grafana

### 方法1: 通过 Grafana UI 导入

1. 登录 Grafana (默认 http://localhost:3000)
2. 点击左侧菜单 "+" → "Import dashboard"
3. 选择 "Upload JSON file" 或直接粘贴 JSON 内容
4. 选择 Prometheus 数据源
5. 点击 "Import"

### 方法2: 通过 API 导入

```bash
# 假设 Grafana 运行在 localhost:3000
curl -X POST \
  http://admin:admin@localhost:3000/api/dashboards/db \
  -H 'Content-Type: application/json' \
  -d @logistics-ai-control-tower.json
```

### 方法3: 放入 provisioning 目录

```bash
# 复制到 Grafana provisioning 目录
cp logistics-ai-control-tower.json /etc/grafana/provisioning/dashboards/

# 重启 Grafana
sudo systemctl restart grafana-server
```

---

## 📊 二、需要的数据源字段 (Prometheus Metrics)

### 核心指标

| 指标名称 | 类型 | 标签 | 说明 |
|---------|------|------|------|
| `logistics_shipment_in_transit_total` | Gauge | region | 在途运单总数 |
| `logistics_otd_percent` | Gauge | region | 准时交付率(%) |
| `logistics_ai_resolved_total` | Counter | region | AI处理事件数 |
| `logistics_incident_total` | Counter | region | 异常事件总数 |
| `logistics_cost_saving_total` | Counter | region | 成本节省累计(元) |

### 地图与位置

| 指标名称 | 类型 | 标签 | 说明 |
|---------|------|------|------|
| `logistics_vehicle_location` | Gauge | vehicle_id, status, region | 车辆GPS位置(lat/lon) |
| `logistics_warehouse_capacity_percent` | Gauge | warehouse | 仓库利用率(%) |

### 趋势与延迟

| 指标名称 | 类型 | 标签 | 说明 |
|---------|------|------|------|
| `logistics_delay_total` | Counter | delay_reason, region | 延误事件数 |
| `logistics_otd_target` | Gauge | - | OTD目标值(如95) |

### Escalation 漏斗

| 指标名称 | 类型 | 标签 | 说明 |
|---------|------|------|------|
| `logistics_ai_handled_total` | Counter | region | AI处理的事件 |
| `logistics_escalated_total` | Counter | region | 升级到人工的事件 |
| `logistics_resolved_total` | Counter | region | 已解决事件 |

### AI 智能建议

| 指标名称 | 类型 | 标签 | 说明 |
|---------|------|------|------|
| `logistics_ai_recommendation` | Info | priority, category, recommendation, affected_shipments, estimated_impact | AI建议(文本) |
| `logistics_risk_score` | Gauge | region | 风险指数(0-100) |
| `logistics_anomaly_total` | Counter | anomaly_type, region | 异常事件数 |

### 承运商与库存

| 指标名称 | 类型 | 标签 | 说明 |
|---------|------|------|------|
| `logistics_carrier_performance` | Gauge | carrier, otd_percent, cost_efficiency, damage_rate, score | 承运商绩效 |
| `logistics_shipment_by_status` | Gauge | status | 运单状态分布 |
| `logistics_inventory_alert` | Gauge | warehouse, sku, product_name, alert_level, days_remaining | 库存预警 |

### 系统监控

| 指标名称 | 类型 | 标签 | 说明 |
|---------|------|------|------|
| `up{job="logistics-*"}` | Gauge | job | 服务健康状态 |

---

## 🔧 三、Prometheus 配置示例

### prometheus.yml 配置

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  # 外运物流控制塔后端
  - job_name: 'logistics-backend'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
    
  # 预测服务
  - job_name: 'logistics-prediction'
    static_configs:
      - targets: ['localhost:8001']
    metrics_path: '/metrics'

  # AI Agent 服务
  - job_name: 'logistics-ai-agent'
    static_configs:
      - targets: ['localhost:40000']
    metrics_path: '/metrics'
```

### 指标暴露端点示例 (FastAPI)

```python
# app/metrics.py
from prometheus_client import Counter, Gauge, Info, generate_latest

# 定义指标
shipment_in_transit = Gauge(
    'logistics_shipment_in_transit_total',
    'Total shipments in transit',
    ['region']
)

otd_percent = Gauge(
    'logistics_otd_percent',
    'On-time delivery percentage',
    ['region']
)

ai_resolved = Counter(
    'logistics_ai_resolved_total',
    'Total incidents resolved by AI',
    ['region']
)

cost_saving = Counter(
    'logistics_cost_saving_total',
    'Cumulative cost savings in CNY',
    ['region']
)

vehicle_location = Gauge(
    'logistics_vehicle_location',
    'Vehicle GPS location',
    ['vehicle_id', 'status', 'region']
)

ai_recommendation = Info(
    'logistics_ai_recommendation',
    'AI recommendations'
)

risk_score = Gauge(
    'logistics_risk_score',
    'AI risk assessment score',
    ['region']
)

# 在 FastAPI 中暴露
from fastapi import Response

@app.get('/metrics')
async def metrics():
    return Response(
        content=generate_latest(),
        media_type='text/plain'
    )
```

---

## 🤖 四、结合 Hermes Agent 实时推送数据

### 架构概览

```
Hermes Agent (AI大脑)
    ↓
    ├─→ 定时分析 (Cron Job)
    │   ├─→ 检查延误预警
    │   ├─→ 生成AI建议
    │   └─→ 更新Prometheus指标
    │
    ├─→ 实时监控 (Watch Pattern)
    │   ├─→ 检测异常事件
    │   └─→ 触发自动处置
    │
    └─→ Grafana Dashboard
        └─→ 30秒自动刷新展示
```

### 步骤1: 安装 Prometheus Client

```bash
cd ~/sinotrans-logistics-control-tower
pip install prometheus-client
```

### 步骤2: 创建指标更新脚本

```python
# scripts/update_metrics.py
import time
import random
from prometheus_client import CollectorRegistry, Gauge, Counter, push_to_gateway

# 模拟数据 - 实际应从数据库或API获取
def get_real_time_data():
    return {
        'in_transit': random.randint(200, 500),
        'otd': random.uniform(92, 98),
        'ai_handled': random.randint(50, 100),
        'cost_saving': random.randint(5000, 20000),
        'risk_score': random.randint(20, 60)
    }

# 更新指标
def update_metrics():
    data = get_real_time_data()
    shipment_in_transit.labels(region='华东').set(data['in_transit'])
    otd_percent.labels(region='华东').set(data['otd'])
    risk_score.labels(region='华东').set(data['risk_score'])

if __name__ == '__main__':
    while True:
        update_metrics()
        time.sleep(30)  # 30秒更新一次
```

### 步骤3: 创建 Hermes Cron Job

在 Hermes Agent 中创建定时任务：

```bash
# 创建每5分钟运行的监控任务
hermes cron create \
  --name "物流AI控制塔监控" \
  --schedule "*/5 * * * *" \
  --task "检查外运物流控制塔状态，分析延误预警，更新Grafana指标" \
  --skills "systematic-debugging"
```

### 步骤4: 创建实时预警任务

```bash
# 创建实时告警监控
hermes cron create \
  --name "延误预警实时监控" \
  --schedule "*/1 * * * *" \
  --task "监控延误率超过阈值的情况，生成AI建议并推送到控制塔" \
  --deliver "telegram:物流控制塔群"
```

### 步骤5: 通过 API 更新 AI 建议

```python
# scripts/ai_recommendations.py
import httpx
from datetime import datetime

async def push_ai_recommendation(recommendation: dict):
    """推送AI建议到Grafana Annotation"""
    grafana_url = "http://localhost:3000"
    auth = ("admin", "admin")
    
    annotation = {
        "dashboardUID": "logistics-ai-control-tower-v1",
        "time": int(datetime.now().timestamp() * 1000),
        "tags": ["ai-recommendation", recommendation.get("priority", "medium")],
        "text": recommendation.get("text", "")
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{grafana_url}/api/annotations",
            json=annotation,
            auth=auth
        )
        return response.json()

# 示例使用
recommendation = {
    "priority": "high",
    "text": "🔴 建议将上海仓部分订单转移至苏州仓，预计可减少延误订单30%"
}
```

---

## 📱 五、大屏展示配置

### 浏览器全屏模式

1. 打开 Grafana Dashboard
2. 按 `F11` 进入浏览器全屏
3. 按 `d` + `e` 进入 Grafana 展示模式

### 自动刷新设置

Dashboard 已配置 30秒 自动刷新，可在右上角调整：
- 5s / 10s / 30s / 1m / 5m

### TV 大屏优化

```bash
# 安装 unattended-upgrades 确保系统稳定
sudo apt install unattended-upgrades

# 设置屏幕不休眠
sudo systemctl mask sleep.target suspend.target

# Firefox 自动全屏启动
firefox --kiosk "http://localhost:3000/d/logistics-ai-control-tower-v1"
```

---

## 🎨 六、颜色方案

Dashboard 使用物流行业专业配色：

| 颜色 | 色值 | 用途 |
|------|------|------|
| 主色-物流蓝 | `#0077B6` | 正常状态、主要指标 |
| 成功-绿色 | `#06D6A0` | 达标、已解决 |
| 警告-黄色 | `#FFD166` | 需关注、中等风险 |
| 危险-红色 | `#FF6B6B` | 异常、延误、紧急 |
| AI-紫色 | `#7B2CBF` | AI处理相关 |

---

## 🔗 七、相关链接

- 外运物流控制塔主系统: http://localhost
- 红芯智答AI助手: http://localhost:40000
- Grafana Dashboard: http://localhost:3000/d/logistics-ai-control-tower-v1

---

## 📝 注意事项

1. **数据源配置**: 导入前确保 Prometheus 数据源已配置
2. **指标实现**: 需要在后端实现上述 Prometheus 指标暴露
3. **GPS数据**: 地图面板需要车辆GPS坐标数据支持
4. **AI建议**: 需要集成LLM服务生成实时建议
5. **权限管理**: 生产环境请修改 Grafana 默认密码

如需进一步定制或集成支持，请告知具体需求！
