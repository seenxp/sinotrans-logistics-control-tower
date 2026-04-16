"""
设备管理API
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime, timedelta
import random

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


# 设备类型定义
DEVICE_TYPES = [
    {"code": "xiaoyou", "name": "小悠盘"},
    {"code": "xiaoxun", "name": "小寻叉"},
    {"code": "agv", "name": "AGV"},
    {"code": "agf", "name": "AGF"},
    {"code": "ctu", "name": "CTU"},
    {"code": "autoLine", "name": "自动线体"},
    {"code": "dws", "name": "DWS"}
]

# 园区定义
PARKS = [
    {"code": "shanghai", "name": "上海奉贤", "location": [121.47, 31.23]},
    {"code": "guangzhou", "name": "广州东勤", "location": [113.25, 23.13]},
    {"code": "chongqing", "name": "重庆园区", "location": [106.55, 29.56]}
]


@router.get("/dashboard", summary="获取设备看板数据")
async def get_dashboard():
    """
    获取设备看板全景数据
    """
    try:
        # 生成模拟数据
        device_stats = []
        for device_type in DEVICE_TYPES:
            total = random.randint(20, 60)
            online = random.randint(int(total * 0.8), total)
            device_stats.append({
                "type": device_type["name"],
                "code": device_type["code"],
                "total": total,
                "online": online,
                "offline": total - online
            })

        park_stats = []
        for park in PARKS:
            park_stats.append({
                "code": park["code"],
                "name": park["name"],
                "location": park["location"],
                "deviceCount": random.randint(80, 200),
                "onlineCount": random.randint(60, 180),
                "taskCount": random.randint(50, 150)
            })

        return {
            "code": 200,
            "message": "操作成功",
            "data": {
                "deviceStats": device_stats,
                "parkStats": park_stats,
                "totalDevices": sum(d["total"] for d in device_stats),
                "totalOnline": sum(d["online"] for d in device_stats),
                "todayTasks": random.randint(800, 1500),
                "completedTasks": random.randint(700, 1400)
            },
            "timestamp": int(datetime.now().timestamp() * 1000),
            "success": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/parks", summary="获取园区列表")
async def get_parks():
    """
    获取所有物流园区列表
    """
    try:
        return {
            "code": 200,
            "message": "操作成功",
            "data": PARKS,
            "timestamp": int(datetime.now().timestamp() * 1000),
            "success": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/device-types", summary="获取设备类型列表")
async def get_device_types():
    """
    获取所有设备类型列表
    """
    try:
        return {
            "code": 200,
            "message": "操作成功",
            "data": DEVICE_TYPES,
            "timestamp": int(datetime.now().timestamp() * 1000),
            "success": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/online-rate", summary="获取设备在线率")
async def get_online_rate(
    park: Optional[str] = Query(None, description="园区代码")
):
    """
    获取各类设备在线率统计
    """
    try:
        result = []
        for device_type in DEVICE_TYPES:
            total = random.randint(20, 60)
            online = random.randint(int(total * 0.8), total)
            result.append({
                "type": device_type["name"],
                "code": device_type["code"],
                "total": total,
                "online": online,
                "rate": round(online / total * 100, 1)
            })

        return {
            "code": 200,
            "message": "操作成功",
            "data": result,
            "timestamp": int(datetime.now().timestamp() * 1000),
            "success": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/usage-duration", summary="获取设备使用时长")
async def get_usage_duration(
    device_type: Optional[str] = Query(None, description="设备类型"),
    time_range: Optional[str] = Query("today", description="时间范围: today/week/month")
):
    """
    获取设备使用时长统计
    """
    try:
        # 生成使用时长分布数据
        duration_distribution = [
            {"range": "≤2h", "count": random.randint(30, 50)},
            {"range": "2-4h", "count": random.randint(20, 40)},
            {"range": "4-6h", "count": random.randint(10, 25)},
            {"range": ">6h", "count": random.randint(5, 15)}
        ]

        return {
            "code": 200,
            "message": "操作成功",
            "data": {
                "distribution": duration_distribution,
                "avgDuration": random.randint(180, 360),  # 分钟
                "maxDuration": random.randint(420, 540),
                "minDuration": random.randint(60, 120)
            },
            "timestamp": int(datetime.now().timestamp() * 1000),
            "success": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trend/tasks", summary="获取任务趋势数据")
async def get_task_trend(
    time_range: str = Query("week", description="时间范围: week/month"),
    park: Optional[str] = Query(None, description="园区代码")
):
    """
    获取设备任务趋势数据
    """
    try:
        dates = []
        now = datetime.now()

        if time_range == "week":
            for i in range(6, -1, -1):
                date = now - timedelta(days=i)
                dates.append(date.strftime("%m-%d"))
        else:
            for i in range(11, -1, -1):
                date = now - timedelta(days=i * 30)
                dates.append(date.strftime("%Y-%m"))

        series = []
        for device_type in DEVICE_TYPES:
            data = []
            for _ in dates:
                data.append(random.randint(50, 150))
            series.append({
                "name": device_type["name"],
                "data": data
            })

        # 异常任务
        abnormal_data = [random.randint(5, 20) for _ in dates]

        return {
            "code": 200,
            "message": "操作成功",
            "data": {
                "dates": dates,
                "series": series,
                "abnormal": abnormal_data
            },
            "timestamp": int(datetime.now().timestamp() * 1000),
            "success": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trend/duration", summary="获取使用时长趋势")
async def get_duration_trend(
    time_range: str = Query("week", description="时间范围: week/month"),
    park: Optional[str] = Query(None, description="园区代码")
):
    """
    获取设备使用时长趋势数据
    """
    try:
        dates = []
        now = datetime.now()

        if time_range == "week":
            for i in range(6, -1, -1):
                date = now - timedelta(days=i)
                dates.append(date.strftime("%m-%d"))
        else:
            for i in range(11, -1, -1):
                date = now - timedelta(days=i * 30)
                dates.append(date.strftime("%Y-%m"))

        series = []
        for device_type in DEVICE_TYPES:
            data = []
            for _ in dates:
                data.append(random.randint(120, 420))  # 分钟
            series.append({
                "name": device_type["name"],
                "data": data
            })

        return {
            "code": 200,
            "message": "操作成功",
            "data": {
                "dates": dates,
                "series": series
            },
            "timestamp": int(datetime.now().timestamp() * 1000),
            "success": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/devices", summary="获取设备列表")
async def get_devices(
    device_type: Optional[str] = Query(None, description="设备类型"),
    park: Optional[str] = Query(None, description="园区代码"),
    status: Optional[str] = Query(None, description="设备状态")
):
    """
    获取设备实时状态列表
    """
    try:
        devices = []
        statuses = ["online", "offline", "error", "idle", "working"]

        for i in range(1, 51):
            dev_type = random.choice(DEVICE_TYPES)
            dev_status = random.choice(statuses)
            dev_park = random.choice(PARKS)

            devices.append({
                "deviceId": f"{dev_type['code'].upper()}-{str(i).padStart(4, '0')}",
                "deviceName": f"{dev_type['name']}-{i}",
                "deviceType": dev_type["code"],
                "park": dev_park["name"],
                "status": dev_status,
                "currentTask": random.choice(["入库作业", "出库作业", "盘点作业", "搬运作业", "扫描作业", "-"]) if dev_status == "working" else "-",
                "todayTasks": random.randint(10, 60),
                "todayDuration": random.randint(60, 480),
                "lastOnlineTime": (datetime.now() - timedelta(minutes=random.randint(0, 60))).strftime("%Y-%m-%d %H:%M:%S")
            })

        # 筛选
        if device_type:
            devices = [d for d in devices if d["deviceType"] == device_type]
        if park:
            park_name = next((p["name"] for p in PARKS if p["code"] == park), None)
            if park_name:
                devices = [d for d in devices if d["park"] == park_name]
        if status:
            devices = [d for d in devices if d["status"] == status]

        return {
            "code": 200,
            "message": "操作成功",
            "data": devices,
            "timestamp": int(datetime.now().timestamp() * 1000),
            "success": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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