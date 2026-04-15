#!/bin/bash

# 外运物流控制塔 - GitHub仓库创建脚本
# 使用方法: ./setup_github.sh

set -e

echo ""
echo "=========================================="
echo "  外运物流控制塔 - GitHub仓库创建向导"
echo "=========================================="
echo ""

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

echo -e "${BLUE}当前目录: $(pwd)${NC}"
echo ""

# 步骤1: 检查Git状态
echo -e "${YELLOW}[步骤 1/4] 检查Git状态...${NC}"
if [ -d ".git" ]; then
    echo -e "${GREEN}✓ Git仓库已初始化${NC}"
    echo "  提交次数: $(git rev-list --count HEAD)"
    echo "  最新提交: $(git log -1 --pretty=format:'%s')"
else
    echo -e "${RED}✗ Git仓库未初始化${NC}"
    exit 1
fi
echo ""

# 步骤2: 创建Personal Access Token
echo -e "${YELLOW}[步骤 2/4] 创建GitHub Personal Access Token${NC}"
echo ""
echo "请在浏览器中完成以下操作:"
echo ""
echo -e "${BLUE}1. 打开链接: https://github.com/settings/tokens/new${NC}"
echo "2. Note: 输入 'sinotrans-logistics-control-tower'"
echo "3. Expiration: 选择 'No expiration' 或 '90 days'"
echo "4. 勾选以下权限:"
echo "   ☑ repo (Full control of private repositories)"
echo "   ☑ read:org (Read organization data)"
echo "   ☑ gist (Create gists)"
echo "5. 点击 'Generate token'"
echo "6. 复制生成的token (以 ghp_ 开头)"
echo ""
echo -e "${YELLOW}注意: Token只会显示一次，请立即复制保存！${NC}"
echo ""
read -p "按Enter键打开浏览器创建Token..." 
xdg-open "https://github.com/settings/tokens/new" 2>/dev/null || echo "请手动打开浏览器"
echo ""

# 等待用户输入Token
read -p "请输入您的GitHub Personal Access Token: " GITHUB_TOKEN

if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${RED}错误: Token不能为空${NC}"
    exit 1
fi

# 验证Token格式
if [[ ! "$GITHUB_TOKEN" =~ ^ghp_ ]]; then
    echo -e "${YELLOW}警告: Token格式可能不正确 (应该以ghp_开头)${NC}"
    read -p "是否继续? (y/n): " confirm
    if [ "$confirm" != "y" ]; then
        exit 1
    fi
fi
echo ""

# 步骤3: 登录GitHub
echo -e "${YELLOW}[步骤 3/4] 登录GitHub...${NC}"
echo "$GITHUB_TOKEN" | gh auth login --with-token 2>/dev/null

if gh auth status &>/dev/null; then
    echo -e "${GREEN}✓ GitHub登录成功${NC}"
    
    # 获取用户名
    GITHUB_USER=$(gh api user -q .login)
    echo "  用户名: $GITHUB_USER"
else
    echo -e "${RED}✗ GitHub登录失败${NC}"
    echo "请检查Token是否正确"
    exit 1
fi
echo ""

# 步骤4: 创建仓库并推送
echo -e "${YELLOW}[步骤 4/4] 创建GitHub仓库并推送代码...${NC}"

REPO_NAME="sinotrans-logistics-control-tower"
REPO_DESC="基于数字孪生、AI预测和可视化大屏的智能物流管理平台 - 外运物流控制塔"

# 检查仓库是否已存在
if gh repo view "$GITHUB_USER/$REPO_NAME" &>/dev/null; then
    echo -e "${YELLOW}仓库已存在，将推送到现有仓库${NC}"
    
    # 检查远程仓库配置
    if git remote get-url origin &>/dev/null; then
        echo "远程仓库已配置: $(git remote get-url origin)"
    else
        git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
        echo "已添加远程仓库"
    fi
    
    # 推送
    git branch -M main
    git push -u origin main --force
else
    echo "正在创建新仓库..."
    
    # 创建仓库并推送
    gh repo create "$REPO_NAME" \
        --public \
        --description "$REPO_DESC" \
        --source=. \
        --push \
        --remote origin
fi

echo ""

# 完成
echo -e "${GREEN}=========================================="
echo "  🎉 仓库创建成功！"
echo "=========================================="
echo ""
echo "仓库地址: https://github.com/$GITHUB_USER/$REPO_NAME"
echo ""
echo "接下来您可以:"
echo "  1. 访问仓库查看代码"
echo "  2. 添加仓库描述和主题标签"
echo "  3. 启用GitHub Pages"
echo "  4. 配置GitHub Actions CI/CD"
echo ""
echo "推荐的主题标签:"
echo "  logistics, digital-twin, timesfm, vue, fastapi, python"
echo ""
echo "==========================================${NC}"

# 自动打开仓库
read -p "是否打开仓库页面? (y/n): " open_browser
if [ "$open_browser" = "y" ]; then
    xdg-open "https://github.com/$GITHUB_USER/$REPO_NAME" 2>/dev/null || echo "请手动打开浏览器"
fi
