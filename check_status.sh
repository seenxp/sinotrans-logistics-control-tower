#!/bin/bash

# 外运物流控制塔 - 服务状态检查脚本

echo "=========================================="
echo "外运物流控制塔 - 服务状态检查"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查后端服务
echo "检查后端服务 (端口 8000)..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}✓ 后端服务运行正常${NC}"
    echo "  健康检查: http://localhost:8000/health"
    echo "  API文档: http://localhost:8000/docs"
else
    echo -e "${RED}✗ 后端服务未运行${NC}"
fi

echo ""

# 检查前端服务
echo "检查前端服务 (端口 3000)..."
if curl -s http://localhost:3000 > /dev/null; then
    echo -e "${GREEN}✓ 前端服务运行正常${NC}"
    echo "  访问地址: http://localhost:3000"
else
    echo -e "${RED}✗ 前端服务未运行${NC}"
fi

echo ""

# 检查预测服务
echo "检查预测服务 (端口 8001)..."
if curl -s http://localhost:8001/health > /dev/null; then
    echo -e "${GREEN}✓ 预测服务运行正常${NC}"
    echo "  健康检查: http://localhost:8001/health"
else
    echo -e "${RED}✗ 预测服务未运行${NC}"
fi

echo ""

# 检查数据库
echo "检查PostgreSQL数据库..."
if sudo -u postgres psql -d logistics_control_tower -c "SELECT 1;" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ 数据库连接正常${NC}"
    echo "  数据库名: logistics_control_tower"
else
    echo -e "${RED}✗ 数据库连接失败${NC}"
fi

echo ""

# 检查Redis
echo "检查Redis缓存..."
if redis-cli ping > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Redis缓存正常${NC}"
else
    echo -e "${RED}✗ Redis缓存未运行${NC}"
fi

echo ""

# 检查Nginx
echo "检查Nginx反向代理..."
if systemctl is-active --quiet nginx; then
    echo -e "${GREEN}✓ Nginx运行正常${NC}"
    echo "  统一入口: http://localhost"
else
    echo -e "${RED}✗ Nginx未运行${NC}"
fi

echo ""

# 检查端口占用
echo "端口占用情况:"
echo "  8000 (后端): $(lsof -i :8000 | grep LISTEN | wc -l) 个进程"
echo "  3000 (前端): $(lsof -i :3000 | grep LISTEN | wc -l) 个进程"
echo "  8001 (预测): $(lsof -i :8001 | grep LISTEN | wc -l) 个进程"
echo "  5432 (数据库): $(lsof -i :5432 | grep LISTEN | wc -l) 个进程"
echo "  6379 (Redis): $(lsof -i :6379 | grep LISTEN | wc -l) 个进程"
echo "  80 (Nginx): $(lsof -i :80 | grep LISTEN | wc -l) 个进程"

echo ""

# 访问地址汇总
echo "=========================================="
echo "访问地址汇总"
echo "=========================================="
echo ""
echo "统一入口 (通过Nginx):"
echo "  主应用: http://localhost"
echo "  API: http://localhost/api/v1/"
echo "  预测服务: http://localhost/prediction/"
echo ""
echo "直接访问:"
echo "  后端API: http://localhost:8000"
echo "  前端开发服务器: http://localhost:3000"
echo "  预测服务: http://localhost:8001"
echo "  API文档: http://localhost:8000/docs"
echo ""
echo "=========================================="