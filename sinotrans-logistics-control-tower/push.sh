#!/bin/bash

# 外运物流控制塔 - GitHub推送脚本
# 在终端中运行: bash push.sh

cd /home/ubuntu/sinotrans-logistics-control-tower

echo ""
echo "=========================================="
echo "  外运物流控制塔 - GitHub推送"
echo "=========================================="
echo ""
echo "请创建GitHub Personal Access Token:"
echo ""
echo "1. 打开: https://github.com/settings/tokens/new"
echo "2. Note: sinotrans-logistics-control-tower"
echo "3. 勾选: repo, read:org, gist"
echo "4. 点击 Generate token"
echo "5. 复制token (以ghp_开头)"
echo ""
read -p "请输入您的GitHub用户名: " username
read -sp "请输入您的GitHub Token: " token
echo ""

if [ -z "$token" ]; then
    echo "错误: Token不能为空"
    exit 1
fi

# 配置远程仓库
git remote set-url origin https://$username:$token@github.com/seenxp/sinotrans-logistics-control-tower.git

# 推送代码
echo ""
echo "正在推送代码..."
git push -u origin master

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "  ✅ 推送成功！"
    echo "=========================================="
    echo ""
    echo "仓库地址: https://github.com/seenxp/sinotrans-logistics-control-tower"
    echo ""
else
    echo ""
    echo "推送失败，请检查token是否正确"
fi

# 恢复远程仓库URL
git remote set-url origin https://github.com/seenxp/sinotrans-logistics-control-tower.git
