#!/bin/bash

# 外运物流控制塔 - 设计系统预览启动脚本

echo "=========================================="
echo "外运物流控制塔 - 设计系统预览"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 需要Python 3"
    exit 1
fi

# 启动HTTP服务器
echo -e "${GREEN}启动HTTP服务器...${NC}"
echo ""

# 检查端口8080是否被占用
if lsof -i :8080 > /dev/null 2>&1; then
    echo -e "${YELLOW}端口8080已被占用，尝试使用端口8081...${NC}"
    PORT=8081
else
    PORT=8080
fi

echo "启动服务器在端口 $PORT..."
echo ""

# 启动服务器
cd "$(dirname "$0")"
python3 -m http.server $PORT &

# 获取服务器PID
SERVER_PID=$!

echo -e "${GREEN}服务器已启动 (PID: $SERVER_PID)${NC}"
echo ""
echo "=========================================="
echo "设计系统预览地址"
echo "=========================================="
echo ""
echo "亮色主题: http://localhost:$PORT/preview.html"
echo "暗色主题: http://localhost:$PORT/preview-dark.html"
echo ""
echo "=========================================="
echo "设计系统文档"
echo "=========================================="
echo ""
echo "DESIGN.md - 设计系统规范"
echo "DESIGN_GUIDE.md - 使用指南"
echo ""
echo "=========================================="
echo "按 Ctrl+C 停止服务器"
echo "=========================================="

# 捕获退出信号
trap "echo ''; echo '停止服务器...'; kill $SERVER_PID; exit 0" INT TERM

# 等待服务器进程
wait $SERVER_PID