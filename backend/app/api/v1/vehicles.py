"""
车辆管理API
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class VehicleResponse(BaseModel):
    id: str
    plate_number: str
    vehicle_type: str
    capacity: float
    current_lat: Optional[float] = None
    current_lng: Optional[float] = None
    status: str
    created_at: datetime


vehicles_db = [
    {"id": "V001", "plate_number": "京A12345", "vehicle_type": "truck", "capacity": 10, "current_lat": 39.9042, "current_lng": 116.4074, "status": "active", "created_at": datetime.now()},
    {"id": "V002", "plate_number": "沪B54321", "vehicle_type": "truck", "capacity": 15, "current_lat": 31.2304, "current_lng": 121.4737, "status": "active", "created_at": datetime.now()},
    {"id": "V003", "plate_number": "SHIP001", "vehicle_type": "ship", "capacity": 1000, "current_lat": 22.5431, "current_lng": 114.0579, "status": "active", "created_at": datetime.now()},
]


@router.get("/", response_model=List[VehicleResponse])
async def get_vehicles(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)):
    """获取车辆列表"""
    return vehicles_db[skip:skip + limit]


@router.get("/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(vehicle_id: str):
    """获取单个车辆详情"""
    for vehicle in vehicles_db:
        if vehicle["id"] == vehicle_id:
            return vehicle
    raise HTTPException(status_code=404, detail="车辆不存在")


@router.get("/stats/summary")
async def get_vehicle_stats():
    """获取车辆统计信息"""
    total = len(vehicles_db)
    active = len([v for v in vehicles_db if v["status"] == "active"])
    return {
        "total": total,
        "active": active,
        "idle": total - active,
        "utilization_rate": round(active / total * 100, 2) if total > 0 else 0,
    }
