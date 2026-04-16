"""
API路由聚合
"""
from fastapi import APIRouter

from app.api.v1 import vehicles, orders, predictions, warehouses, dashboard, equipment

api_router = APIRouter()

api_router.include_router(vehicles.router, prefix="/vehicles", tags=["车辆管理"])
api_router.include_router(orders.router, prefix="/orders", tags=["订单管理"])
api_router.include_router(predictions.router, prefix="/predictions", tags=["预测服务"])
api_router.include_router(warehouses.router, prefix="/warehouses", tags=["仓库管理"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["控制台"])
api_router.include_router(equipment.router, prefix="/equipment", tags=["设备管理"])
