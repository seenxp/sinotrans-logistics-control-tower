#!/bin/bash

# 外运物流控制塔 - GitHub仓库推送脚本

cd /home/ubuntu/sinotrans-logistics-control-tower

echo "=========================================="
echo "外运物流控制塔 - GitHub仓库推送"
echo "=========================================="
echo ""

# 检查仓库是否存在
echo "检查仓库状态..."
if curl -s "https://api.github.com/repos/seenxp/sinotrans-logistics-control-tower" | grep -q '"id"'; then
    echo "✓ 仓库已存在"
else
    echo "仓库不存在，正在创建..."
    
    # 创建仓库
    curl -X POST "https://api.github.com/user/repos" \
        -H "Accept: application/vnd.github.v3+json" \
        -d '{
            "name": "sinotrans-logistics-control-tower",
            "description": "基于数字孪生、AI预测和可视化大屏的智能物流管理平台",
            "private": false,
            "auto_init": false
        }'
    
    echo ""
    echo "✓ 仓库创建成功"
fi

echo ""
echo "正在推送代码..."
git push -u origin master

echo ""
echo "=========================================="
echo "完成！"
echo "仓库地址: https://github.com/seenxp/sinotrans-logistics-control-tower"
echo "=========================================="
