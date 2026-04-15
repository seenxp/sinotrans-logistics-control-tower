"""
仓库管理API
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class WarehouseResponse(BaseModel):
    id: str
    name: str
    address: str
    city: str
    capacity: float
    current_load: float
    status: str
    utilization_rate: float


warehouses_db = [
    {"id": "WH001", "name": "北京中央仓库", "address": "大兴区物流园区", "city": "北京", "capacity": 10000, "current_load": 7500, "status": "active"},
    {"id": "WH002", "name": "上海分拨中心", "address": "浦东新区自贸区", "city": "上海", "capacity": 15000, "current_load": 12000, "status": "active"},
    {"id": "WH003", "name": "广州南部中心", "address": "白云区物流港", "city": "广州", "capacity": 8000, "current_load": 5600, "status": "active"},
    {"id": "WH004", "name": "深圳跨境仓库", "address": "前海自贸区", "city": "深圳", "capacity": 12000, "current_load": 9600, "status": "active"},
    {"id": "WH005", "name": "成都西部枢纽", "address": "双流区物流园", "city": "成都", "capacity": 6000, "current_load": 3600, "status": "active"},
]


@router.get("/", response_model=List[WarehouseResponse])
async def get_warehouses(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)):
    """获取仓库列表"""
    result = []
    for wh in warehouses_db[skip:skip + limit]:
        wh_copy = wh.copy()
        wh_copy["utilization_rate"] = round(wh["current_load"] / wh["capacity"] * 100, 2)
        result.append(wh_copy)
    return result


@router.get("/{warehouse_id}", response_model=WarehouseResponse)
async def get_warehouse(warehouse_id: str):
    """获取单个仓库详情"""
    for wh in warehouses_db:
        if wh["id"] == warehouse_id:
            wh_copy = wh.copy()
            wh_copy["utilization_rate"] = round(wh["current_load"] / wh["capacity"] * 100, 2)
            return wh_copy
    raise HTTPException(status_code=404, detail="仓库不存在")


@router.get("/stats/summary")
async def get_warehouse_stats():
    """获取仓库统计信息"""
    total = len(warehouses_db)
    total_capacity = sum(w["capacity"] for w in warehouses_db)
    total_load = sum(w["current_load"] for w in warehouses_db)
    
    return {
        "total_warehouses": total,
        "total_capacity": total_capacity,
        "total_load": total_load,
        "overall_utilization": round(total_load / total_capacity * 100, 2) if total_capacity > 0 else 0,
    }
