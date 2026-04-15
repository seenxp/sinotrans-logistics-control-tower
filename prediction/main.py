"""
外运物流控制塔 - 预测服务
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import random
from datetime import datetime, timedelta

app = FastAPI(
    title="预测服务",
    description="基于TimesFM的物流预测服务",
    version="0.1.0"
)

class PredictionRequest(BaseModel):
    prediction_type: str  # demand, capacity, cost, risk
    time_horizon: int = 7  # 预测天数
    parameters: Optional[dict] = None

class PredictionResult(BaseModel):
    prediction_type: str
    predictions: List[dict]
    confidence: float
    model_version: str
    created_at: datetime

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "service": "预测服务",
        "version": "0.1.0"
    }

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "欢迎使用外运物流控制塔预测服务",
        "docs": "/docs",
        "version": "0.1.0"
    }

@app.post("/predict", response_model=PredictionResult)
async def create_prediction(request: PredictionRequest):
    """创建预测"""
    # 模拟预测结果
    predictions = []
    base_date = datetime.now()
    
    for i in range(request.time_horizon):
        date = base_date + timedelta(days=i)
        value = random.uniform(100, 1000)
        predictions.append({
            "date": date.strftime("%Y-%m-%d"),
            "value": round(value, 2),
            "lower_bound": round(value * 0.9, 2),
            "upper_bound": round(value * 1.1, 2)
        })
    
    return PredictionResult(
        prediction_type=request.prediction_type,
        predictions=predictions,
        confidence=random.uniform(0.7, 0.95),
        model_version="timesfm-2.5-200m-pytorch",
        created_at=datetime.now()
    )

@app.get("/predictions/types")
async def get_prediction_types():
    """获取支持的预测类型"""
    return {
        "types": [
            {"id": "demand", "name": "物流需求预测", "description": "预测未来物流需求量"},
            {"id": "capacity", "name": "运力需求预测", "description": "预测运力需求"},
            {"id": "cost", "name": "成本趋势预测", "description": "预测物流成本趋势"},
            {"id": "risk", "name": "风险预警预测", "description": "预测潜在风险"}
        ]
    }

@app.get("/predictions/history")
async def get_prediction_history(limit: int = 10):
    """获取预测历史"""
    # 模拟历史数据
    history = []
    for i in range(limit):
        history.append({
            "id": i + 1,
            "prediction_type": random.choice(["demand", "capacity", "cost", "risk"]),
            "created_at": (datetime.now() - timedelta(days=i)).isoformat(),
            "confidence": random.uniform(0.7, 0.95)
        })
    return {"history": history}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)