#!/bin/bash

# 外运物流控制塔项目启动脚本

set -e

echo "=========================================="
echo "外运物流控制塔项目启动脚本"
echo "=========================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查Docker
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}错误: Docker未安装${NC}"
        echo "请先安装Docker: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}错误: Docker Compose未安装${NC}"
        echo "请先安装Docker Compose: https://docs.docker.com/compose/install/"
        exit 1
    fi
    
    echo -e "${GREEN}Docker环境检查通过${NC}"
}

# 检查环境变量
check_env() {
    if [ ! -f .env ]; then
        echo -e "${YELLOW}警告: .env文件不存在，正在创建...${NC}"
        cat > .env << EOF
# 数据库配置
DATABASE_URL=postgresql://postgres:password@postgres:5432/logistics_control_tower

# Redis配置
REDIS_URL=redis://redis:6379/0

# TimesFM配置
TIMESFM_MODEL_PATH=google/timesfm-2.5-200m-pytorch
TIMESFM_DEVICE=cpu

# 应用配置
APP_ENV=development
APP_DEBUG=true
SECRET_KEY=your-secret-key-here

# 前端配置
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_WS_BASE_URL=ws://localhost:8000/ws
VITE_APP_TITLE=外运物流控制塔
VITE_APP_ENV=development
EOF
        echo -e "${GREEN}.env文件已创建${NC}"
    else
        echo -e "${GREEN}.env文件已存在${NC}"
    fi
}

# 创建必要目录
create_dirs() {
    echo "创建必要目录..."
    mkdir -p backend/data
    mkdir -p backend/logs
    mkdir -p prediction/models
    mkdir -p prediction/data
    mkdir -p digital-twin/textures
    mkdir -p digital-twin/3d-models
    mkdir -p nginx/ssl
    mkdir -p monitoring/prometheus
    mkdir -p monitoring/grafana/provisioning
    echo -e "${GREEN}目录创建完成${NC}"
}

# 启动服务
start_services() {
    echo "启动Docker服务..."
    
    # 构建并启动所有服务
    docker-compose up -d --build
    
    echo -e "${GREEN}服务启动完成${NC}"
}

# 检查服务状态
check_services() {
    echo "检查服务状态..."
    
    # 等待服务启动
    sleep 10
    
    # 检查后端服务
    if curl -s http://localhost:8000/health > /dev/null; then
        echo -e "${GREEN}后端服务运行正常${NC}"
    else
        echo -e "${YELLOW}后端服务启动中...${NC}"
    fi
    
    # 检查前端服务
    if curl -s http://localhost:3000 > /dev/null; then
        echo -e "${GREEN}前端服务运行正常${NC}"
    else
        echo -e "${YELLOW}前端服务启动中...${NC}"
    fi
    
    # 检查预测服务
    if curl -s http://localhost:8001/health > /dev/null; then
        echo -e "${GREEN}预测服务运行正常${NC}"
    else
        echo -e "${YELLOW}预测服务启动中...${NC}"
    fi
}

# 显示访问信息
show_info() {
    echo ""
    echo "=========================================="
    echo "外运物流控制塔项目已启动"
    echo "=========================================="
    echo ""
    echo "访问地址:"
    echo "  前端应用: http://localhost:3000"
    echo "  后端API: http://localhost:8000"
    echo "  API文档: http://localhost:8000/docs"
    echo "  预测服务: http://localhost:8001"
    echo ""
    echo "管理界面:"
    echo "  RabbitMQ管理: http://localhost:15672"
    echo "  Prometheus: http://localhost:9090"
    echo "  Grafana: http://localhost:3001"
    echo ""
    echo "数据库连接:"
    echo "  PostgreSQL: localhost:5432"
    echo "  Redis: localhost:6379"
    echo ""
    echo "常用命令:"
    echo "  查看日志: docker-compose logs -f [服务名]"
    echo "  停止服务: docker-compose down"
    echo "  重启服务: docker-compose restart"
    echo "  进入容器: docker-compose exec [服务名] bash"
    echo ""
    echo "=========================================="
}

# 主函数
main() {
    echo "开始初始化外运物流控制塔项目..."
    
    # 检查Docker环境
    check_docker
    
    # 检查环境变量
    check_env
    
    # 创建必要目录
    create_dirs
    
    # 启动服务
    start_services
    
    # 检查服务状态
    check_services
    
    # 显示访问信息
    show_info
}

# 执行主函数
main