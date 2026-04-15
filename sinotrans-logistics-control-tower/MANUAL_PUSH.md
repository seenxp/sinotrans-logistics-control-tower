# GitHub推送 - 终端操作指南

## 📋 请在您的终端中运行以下命令

### 步骤1: 创建GitHub Token

1. 打开浏览器访问: https://github.com/settings/tokens/new
2. Note: `sinotrans-logistics-control-tower`
3. 勾选权限: `repo`, `read:org`, `gist`
4. 点击 "Generate token"
5. **复制生成的token** (以 `ghp_` 开头)

### 步骤2: 在终端中运行推送命令

打开一个新的终端窗口，运行以下命令:

```bash
# 进入项目目录
cd /home/ubuntu/sinotrans-logistics-control-tower

# 设置远程仓库 (替换 YOUR_TOKEN 为您复制的token)
git remote set-url origin https://seenxp:YOUR_TOKEN@github.com/seenxp/sinotrans-logistics-control-tower.git

# 推送代码
git push -u origin master

# 恢复远程仓库URL
git remote set-url origin https://github.com/seenxp/sinotrans-logistics-control-tower.git
```

### 示例

如果您的token是 `ghp_xxxxxxxxxxxxxxxxxxxx`，运行:

```bash
cd /home/ubuntu/sinotrans-logistics-control-tower
git remote set-url origin https://seenxp:ghp_xxxxxxxxxxxxxxxxxxxx@github.com/seenxp/sinotrans-logistics-control-tower.git
git push -u origin master
git remote set-url origin https://github.com/seenxp/sinotrans-logistics-control-tower.git
```

---

## ✅ 推送成功后

访问您的仓库:
```
https://github.com/seenxp/sinotrans-logistics-control-tower
```

您应该能看到所有项目文件！

---

## 🔒 安全提示

- Token只会显示一次，请立即复制保存
- 不要将Token分享给他人
- 推送完成后，建议删除Token或设置过期时间