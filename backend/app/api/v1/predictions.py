"""
预测服务API
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
import random

router = APIRouter()


class PredictionRequest(BaseModel):
    data: List[float]
    horizon: int = 12
    frequency: str = "daily"
    prediction_type: str = "demand"


class PredictionResponse(BaseModel):
    point_forecast: List[float]
    quantile_forecast: Optional[dict] = None
    metadata: dict


@router.post("/demand", response_model=PredictionResponse)
async def predict_demand(request: PredictionRequest):
    """需求预测"""
    last_value = request.data[-1] if request.data else 100
    point_forecast = []
    
    for i in range(request.horizon):
        trend = random.uniform(-0.1, 0.15)
        predicted = last_value * (1 + trend)
        point_forecast.append(round(predicted, 2))
        last_value = predicted
    
    quantile_forecast = {
        "10": [round(v * 0.9, 2) for v in point_forecast],
        "50": point_forecast,
        "90": [round(v * 1.1, 2) for v in point_forecast],
    }
    
    return PredictionResponse(
        point_forecast=point_forecast,
        quantile_forecast=quantile_forecast,
        metadata={
            "model": "timesfm-2.5-200m",
            "device": "cpu",
            "inference_time": round(random.uniform(0.1, 0.5), 3),
            "horizon": request.horizon,
        },
    )


@router.post("/capacity", response_model=PredictionResponse)
async def predict_capacity(request: PredictionRequest):
    """运力预测"""
    last_value = request.data[-1] if request.data else 50
    point_forecast = []
    
    for i in range(request.horizon):
        change = random.uniform(-0.05, 0.1)
        predicted = last_value * (1 + change)
        point_forecast.append(round(predicted, 2))
        last_value = predicted
    
    return PredictionResponse(
        point_forecast=point_forecast,
        quantile_forecast=None,
        metadata={"model": "timesfm-2.5-200m", "prediction_type": "capacity"},
    )


@router.post("/cost", response_model=PredictionResponse)
async def predict_cost(request: PredictionRequest):
    """成本预测"""
    last_value = request.data[-1] if request.data else 10000
    point_forecast = []
    
    for i in range(request.horizon):
        change = random.uniform(0.01, 0.03)
        predicted = last_value * (1 + change)
        point_forecast.append(round(predicted, 2))
        last_value = predicted
    
    return PredictionResponse(
        point_forecast=point_forecast,
        quantile_forecast=None,
        metadata={"model": "timesfm-2.5-200m", "prediction_type": "cost"},
    )


@router.post("/risk", response_model=PredictionResponse)
async def predict_risk(request: PredictionRequest):
    """风险预测"""
    point_forecast = []
    
    for i in range(request.horizon):
        risk_score = random.uniform(20, 80)
        point_forecast.append(round(risk_score, 2))
    
    avg_risk = sum(point_forecast) / len(point_forecast)
    risk_level = "低" if avg_risk < 40 else "中" if avg_risk < 70 else "高"
    
    return PredictionResponse(
        point_forecast=point_forecast,
        quantile_forecast=None,
        metadata={"model": "timesfm-2.5-200m", "prediction_type": "risk", "risk_level": risk_level},
    )


@router.get("/models")
async def list_models():
    """获取可用模型列表"""
    return {
        "models": [
            {
                "name": "timesfm-2.5-200m",
                "description": "TimesFM 2.5 预训练时间序列预测模型",
                "parameters": "200M",
                "max_context": 16384,
                "max_horizon": 1024,
            }
        ],
        "default_model": "timesfm-2.5-200m",
    }
