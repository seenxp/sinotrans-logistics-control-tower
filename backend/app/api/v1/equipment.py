"""
设备管理API
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class ForkliftData(BaseModel):
    """叉车数据模型"""
    Id: int
    FltNo: str
    FltName: str
    WarehouseCode: str
    OnlineStatusText: str
    SlamOnLineStatusText: str
    ScanOnLineStatusText: str
    StatusText: str
    UpgradeText: str
    Ip: Optional[str] = None
    SlamIp: Optional[str] = None
    ModelText: Optional[str] = None
    SlamModelText: Optional[str] = None
    ScanModelText: Optional[str] = None
    Owners: Optional[str] = None
    EnabledText: str
    Enabled: bool
    Remark: Optional[str] = None
    SlamVersion: Optional[str] = None
    ShelfPushStatus: Optional[int] = None
    ShelfPushStatusText: Optional[str] = None
    Model: Optional[str] = None
    SlamModel: Optional[str] = None
    ScanModel: Optional[str] = None
    SlamLastPullTime: Optional[str] = None
    ScanLastReportTime: Optional[str] = None
    LastOnlineTime: Optional[str] = None
    PlateNumber: Optional[str] = None
    AbnormalId: Optional[str] = None
    AbnormalDescription: Optional[str] = None


class EquipmentStats(BaseModel):
    """设备统计模型"""
    type: str
    total: int
    online: int
    offline: int


class TaskStats(BaseModel):
    """任务统计模型"""
    total: int
    completed: int
    completion_rate: float


@router.get("/forklifts", summary="获取叉车列表")
async def get_forklifts(
    warehouseCode: Optional[str] = Query(None, description="库房编号")
):
    """
    获取叉车列表，可按库房筛选
    """
    try:
        # 模拟数据 - 实际应该调用外部接口或数据库
        mock_data = [
            {
                "Id": 113,
                "FltNo": "F001",
                "FltName": "F001",
                "WarehouseCode": "WH002010",
                "OnlineStatusText": "离线",
                "SlamOnLineStatusText": "离线",
                "ScanOnLineStatusText": "离线",
                "StatusText": "空闲",
                "UpgradeText": "初始状态",
                "Ip": "10.3.75.232",
                "SlamIp": "10.125.129.88",
                "ModelText": "林德",
                "SlamModelText": "镭神1",
                "ScanModelText": "默认",
                "Owners": "管理员",
                "EnabledText": "启用",
                "Enabled": True,
                "Remark": None,
                "SlamVersion": "1.11.18",
                "ShelfPushStatus": 0,
                "ShelfPushStatusText": "初始状态",
                "Model": "LinDe",
                "SlamModel": "LeiShen1",
                "ScanModel": "Scan1",
                "SlamLastPullTime": "2025-02-21 11:22:57",
                "ScanLastReportTime": "2026-04-13 10:22:13",
                "LastOnlineTime": "2025-09-23 16:23:34",
                "PlateNumber": "辽A0F001",
                "AbnormalId": "32",
                "AbnormalDescription": "故障"
            },
            {
                "Id": 114,
                "FltNo": "F002",
                "FltName": "F002",
                "WarehouseCode": "WH002010",
                "OnlineStatusText": "在线",
                "SlamOnLineStatusText": "在线",
                "ScanOnLineStatusText": "在线",
                "StatusText": "执行任务",
                "UpgradeText": "初始状态",
                "Ip": "10.3.75.233",
                "SlamIp": "10.125.129.89",
                "ModelText": "林德",
                "SlamModelText": "镭神1",
                "ScanModelText": "默认",
                "Owners": "管理员",
                "EnabledText": "启用",
                "Enabled": True,
                "Remark": None,
                "SlamVersion": "1.11.18",
                "ShelfPushStatus": 0,
                "ShelfPushStatusText": "初始状态",
                "Model": "LinDe",
                "SlamModel": "LeiShen1",
                "ScanModel": "Scan1",
                "SlamLastPullTime": "2025-02-21 11:22:57",
                "ScanLastReportTime": "2026-04-13 10:22:13",
                "LastOnlineTime": "2026-04-16 09:45:12",
                "PlateNumber": "辽A0F002",
                "AbnormalId": "",
                "AbnormalDescription": ""
            },
            {
                "Id": 115,
                "FltNo": "F003",
                "FltName": "F003",
                "WarehouseCode": "WH001001",
                "OnlineStatusText": "在线",
                "SlamOnLineStatusText": "在线",
                "ScanOnLineStatusText": "在线",
                "StatusText": "空闲",
                "UpgradeText": "初始状态",
                "Ip": "10.3.75.234",
                "SlamIp": "10.125.129.90",
                "ModelText": "林德",
                "SlamModelText": "镭神1",
                "ScanModelText": "默认",
                "Owners": "操作员A",
                "EnabledText": "启用",
                "Enabled": True,
                "Remark": "正常运行",
                "SlamVersion": "1.11.18",
                "ShelfPushStatus": 1,
                "ShelfPushStatusText": "已下发",
                "Model": "LinDe",
                "SlamModel": "LeiShen1",
                "ScanModel": "Scan1",
                "SlamLastPullTime": "2026-04-16 08:30:00",
                "ScanLastReportTime": "2026-04-16 09:50:00",
                "LastOnlineTime": "2026-04-16 09:50:00",
                "PlateNumber": "京A0F003",
                "AbnormalId": "",
                "AbnormalDescription": ""
            }
        ]
        
        # 如果指定了库房编号，进行筛选
        if warehouseCode:
            filtered_data = [item for item in mock_data if item["WarehouseCode"] == warehouseCode]
        else:
            filtered_data = mock_data
        
        return {
            "code": 200,
            "message": "操作成功",
            "data": filtered_data,
            "timestamp": int(datetime.now().timestamp() * 1000),
            "success": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/forklifts/{forklift_id}", summary="获取单个叉车详情")
async def get_forklift_by_id(forklift_id: int):
    """
    根据ID获取叉车详情
    """
    try:
        # 模拟数据
        mock_data = {
            "Id": forklift_id,
            "FltNo": f"F{forklift_id:03d}",
            "FltName": f"F{forklift_id:03d}",
            "WarehouseCode": "WH002010",
            "OnlineStatusText": "在线",
            "SlamOnLineStatusText": "在线",
            "ScanOnLineStatusText": "在线",
            "StatusText": "空闲",
            "UpgradeText": "初始状态",
            "Ip": "10.3.75.232",
            "SlamIp": "10.125.129.88",
            "ModelText": "林德",
            "SlamModelText": "镭神1",
            "ScanModelText": "默认",
            "Owners": "管理员",
            "EnabledText": "启用",
            "Enabled": True,
            "Remark": None,
            "SlamVersion": "1.11.18",
            "ShelfPushStatus": 0,
            "ShelfPushStatusText": "初始状态",
            "Model": "LinDe",
            "SlamModel": "LeiShen1",
            "ScanModel": "Scan1",
            "SlamLastPullTime": "2025-02-21 11:22:57",
            "ScanLastReportTime": "2026-04-13 10:22:13",
            "LastOnlineTime": "2025-09-23 16:23:34",
            "PlateNumber": "辽A0F001",
            "AbnormalId": "",
            "AbnormalDescription": ""
        }
        
        return {
            "code": 200,
            "message": "操作成功",
            "data": mock_data,
            "timestamp": int(datetime.now().timestamp() * 1000),
            "success": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", summary="获取设备统计")
async def get_equipment_stats():
    """
    获取设备统计信息
    """
    try:
        stats = [
            {"type": "AGV", "total": 45, "online": 42, "offline": 3},
            {"type": "AGF", "total": 28, "online": 25, "offline": 3},
            {"type": "CTU", "total": 36, "online": 33, "offline": 3},
            {"type": "盘点机器", "total": 15, "online": 12, "offline": 3},
            {"type": "智能叉车", "total": 32, "online": 28, "offline": 4}
        ]
        
        return {
            "code": 200,
            "message": "操作成功",
            "data": stats,
            "timestamp": int(datetime.now().timestamp() * 1000),
            "success": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks/stats", summary="获取任务统计")
async def get_task_stats():
    """
    获取任务统计信息
    """
    try:
        stats = {
            "total": 1250,
            "completed": 1180,
            "completion_rate": 94.4
        }
        
        return {
            "code": 200,
            "message": "操作成功",
            "data": stats,
            "timestamp": int(datetime.now().timestamp() * 1000),
            "success": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/forklifts/query", summary="叉车列表查询（兼容外部接口）")
async def query_forklifts(
    warehouseCode: Optional[str] = Query(None, description="库房编号")
):
    """
    兼容外部接口的叉车列表查询
    """
    try:
        # 模拟数据 - 与外部接口格式保持一致
        mock_data = [
            {
                "Id": 113,
                "FltNo": "F001",
                "FltName": "F001",
                "WarehouseCode": "WH002010",
                "OnlineStatusText": "离线",
                "SlamOnLineStatusText": "离线",
                "ScanOnLineStatusText": "离线",
                "StatusText": "空闲",
                "UpgradeText": "初始状态",
                "Ip": "10.3.75.232",
                "SlamIp": "10.125.129.88",
                "ModelText": "林德",
                "SlamModelText": "镭神1",
                "ScanModelText": "默认",
                "Owners": "管理员",
                "EnabledText": "启用",
                "Enabled": True,
                "Remark": None,
                "SlamVersion": "1.11.18",
                "ShelfPushStatus": 0,
                "ShelfPushStatusText": "初始状态",
                "Model": "LinDe",
                "SlamModel": "LeiShen1",
                "ScanModel": "Scan1",
                "SlamLastPullTime": "2025-02-21 11:22:57",
                "ScanLastReportTime": "2026-04-13 10:22:13",
                "LastOnlineTime": "2025-09-23 16:23:34",
                "PlateNumber": "辽A0F001",
                "AbnormalId": "32",
                "AbnormalDescription": "故障"
            }
        ]
        
        # 如果指定了库房编号，进行筛选
        if warehouseCode:
            filtered_data = [item for item in mock_data if item["WarehouseCode"] == warehouseCode]
        else:
            filtered_data = mock_data
        
        return {
            "code": 200,
            "message": "成功",
            "timestamp": int(datetime.now().timestamp() * 1000),
            "data": filtered_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))