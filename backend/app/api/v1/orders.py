"""
订单管理API
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class OrderResponse(BaseModel):
    id: str
    origin: str
    destination: str
    cargo_type: str
    weight: float
    priority: str
    status: str
    created_at: datetime


orders_db = [
    {"id": "ORD001", "origin": "北京", "destination": "上海", "cargo_type": "电子产品", "weight": 500, "priority": "high", "status": "in_transit", "created_at": datetime.now()},
    {"id": "ORD002", "origin": "广州", "destination": "深圳", "cargo_type": "服装", "weight": 200, "priority": "normal", "status": "processing", "created_at": datetime.now()},
    {"id": "ORD003", "origin": "成都", "destination": "重庆", "cargo_type": "食品", "weight": 300, "priority": "urgent", "status": "pending", "created_at": datetime.now()},
]


@router.get("/", response_model=List[OrderResponse])
async def get_orders(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)):
    """获取订单列表"""
    return orders_db[skip:skip + limit]


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str):
    """获取单个订单详情"""
    for order in orders_db:
        if order["id"] == order_id:
            return order
    raise HTTPException(status_code=404, detail="订单不存在")


@router.get("/stats/summary")
async def get_order_stats():
    """获取订单统计信息"""
    total = len(orders_db)
    pending = len([o for o in orders_db if o["status"] == "pending"])
    in_transit = len([o for o in orders_db if o["status"] == "in_transit"])
    delivered = len([o for o in orders_db if o["status"] == "delivered"])
    return {
        "total": total,
        "pending": pending,
        "in_transit": in_transit,
        "delivered": delivered,
        "completion_rate": round(delivered / total * 100, 2) if total > 0 else 0,
    }
