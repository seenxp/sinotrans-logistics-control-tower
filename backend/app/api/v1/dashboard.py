"""
控制台数据API
"""
from fastapi import APIRouter
from datetime import datetime, timedelta
import random

router = APIRouter()


@router.get("/overview")
async def get_dashboard_overview():
    """获取控制台概览数据"""
    return {
        "kpi": {
            "total_orders": {"value": 15680, "change": 12.5, "trend": "up"},
            "active_vehicles": {"value": 342, "change": 8.3, "trend": "up"},
            "delivery_rate": {"value": 96.8, "change": 2.1, "trend": "up"},
            "avg_delivery_time": {"value": 2.4, "unit": "天", "change": -5.2, "trend": "down"},
        },
        "alerts": [
            {"id": "ALT001", "type": "delay", "severity": "medium", "message": "北京至上海线路预计延迟2小时", "timestamp": datetime.now().isoformat()},
            {"id": "ALT002", "type": "capacity", "severity": "high", "message": "上海分拨中心容量即将饱和", "timestamp": (datetime.now() - timedelta(hours=1)).isoformat()},
            {"id": "ALT003", "type": "weather", "severity": "low", "message": "华南地区明日有雨，注意货物防护", "timestamp": (datetime.now() - timedelta(hours=2)).isoformat()},
        ],
        "timestamp": datetime.now().isoformat(),
    }


@router.get("/realtime")
async def get_realtime_data():
    """获取实时数据"""
    return {
        "active_shipments": random.randint(500, 800),
        "vehicles_in_transit": random.randint(200, 350),
        "pending_orders": random.randint(50, 150),
        "completed_today": random.randint(300, 500),
        "timestamp": datetime.now().isoformat(),
    }


@router.get("/trends")
async def get_trends(days: int = 7):
    """获取趋势数据"""
    dates = []
    orders = []
    revenue = []
    
    for i in range(days):
        date = datetime.now() - timedelta(days=days - i - 1)
        dates.append(date.strftime("%Y-%m-%d"))
        orders.append(random.randint(1800, 2500))
        revenue.append(round(random.uniform(150000, 250000), 2))
    
    return {"dates": dates, "orders": orders, "revenue": revenue}


@router.get("/distribution")
async def get_distribution():
    """获取分布数据"""
    return {
        "vehicle_types": {"truck": 245, "ship": 12, "plane": 8, "train": 15},
        "order_status": {"pending": 156, "processing": 89, "in_transit": 423, "delivered": 1876},
        "regions": {"华东": 35, "华南": 28, "华北": 20, "西南": 12, "其他": 5},
    }


@router.get("/map-data")
async def get_map_data():
    """获取地图数据"""
    return {
        "warehouses": [
            {"id": "WH001", "name": "北京中央仓库", "lat": 39.9042, "lng": 116.4074, "type": "warehouse"},
            {"id": "WH002", "name": "上海分拨中心", "lat": 31.2304, "lng": 121.4737, "type": "warehouse"},
            {"id": "WH003", "name": "广州南部中心", "lat": 23.1291, "lng": 113.2644, "type": "warehouse"},
        ],
        "vehicles": [
            {"id": "V001", "lat": 35.5, "lng": 118.0, "type": "truck", "status": "active"},
            {"id": "V002", "lat": 28.5, "lng": 117.0, "type": "truck", "status": "active"},
        ],
    }
