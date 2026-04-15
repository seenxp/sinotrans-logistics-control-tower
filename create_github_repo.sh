#!/bin/bash

# GitHub仓库创建脚本

set -e

echo "=========================================="
echo "外运物流控制塔 - GitHub仓库创建脚本"
echo "=========================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 项目目录
PROJECT_DIR="/home/ubuntu/sinotrans-logistics-control-tower"

# 检查项目目录
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}错误: 项目目录不存在${NC}"
    exit 1
fi

cd "$PROJECT_DIR"

# 检查gh命令
if ! command -v gh &> /dev/null; then
    echo -e "${RED}错误: GitHub CLI未安装${NC}"
    echo "安装命令: sudo apt install gh"
    exit 1
fi

# 检查认证状态
echo "检查GitHub认证状态..."
if gh auth status &> /dev/null; then
    echo -e "${GREEN}GitHub已认证${NC}"
else
    echo -e "${YELLOW}GitHub未认证，需要登录${NC}"
    echo ""
    echo "请选择登录方式:"
    echo "1. Web浏览器登录 (推荐)"
    echo "2. 使用Personal Access Token"
    echo ""
    read -p "请选择 (1/2): " choice
    
    case $choice in
        1)
            echo "正在打开浏览器进行认证..."
            gh auth login --web --hostname github.com
            ;;
        2)
            echo ""
            echo "请创建Personal Access Token:"
            echo "1. 访问 https://github.com/settings/tokens"
            echo "2. 点击 'Generate new token (classic)'"
            echo "3. 勾选: repo, read:org, gist"
            echo "4. 复制生成的token"
            echo ""
            read -p "请输入您的GitHub Personal Access Token: " token
            
            if [ -z "$token" ]; then
                echo -e "${RED}错误: Token不能为空${NC}"
                exit 1
            fi
            
            echo "$token" | gh auth login --with-token
            ;;
        *)
            echo -e "${RED}无效选择${NC}"
            exit 1
            ;;
    esac
fi

# 创建仓库
echo ""
echo "创建GitHub仓库..."
gh repo create sinotrans-logistics-control-tower \
    --public \
    --description "基于数字孪生、AI预测和可视化大屏的智能物流管理平台" \
    --source=. \
    --push \
    --remote origin

echo ""
echo -e "${GREEN}=========================================="
echo "仓库创建成功！"
echo "=========================================="
echo ""
echo "仓库地址: https://github.com/seenxp/sinotrans-logistics-control-tower"
echo ""
echo "您现在可以:"
echo "1. 访问仓库查看代码"
echo "2. 邀请协作者"
echo "3. 设置GitHub Pages"
echo "4. 配置CI/CD"
echo ""
echo "==========================================${NC}"
