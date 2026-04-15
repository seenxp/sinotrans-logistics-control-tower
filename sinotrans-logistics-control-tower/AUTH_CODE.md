# GitHub认证 - 设备代码

## 🔐 认证步骤

GitHub CLI需要您完成设备认证。请按照以下步骤操作:

### 步骤1: 打开认证页面

在浏览器中打开:
```
https://github.com/login/device
```

### 步骤2: 输入设备代码

输入以下代码:
```
A471-EC11
```

### 步骤3: 授权

1. 登录您的GitHub账号 (seenxp@gmail.com)
2. 点击 "Authorize" 授权GitHub CLI
3. 等待页面显示认证成功

### 步骤4: 创建仓库

认证成功后，运行以下命令:

```bash
cd /home/ubuntu/sinotrans-logistics-control-tower

# 创建仓库并推送
gh repo create sinotrans-logistics-control-tower \
  --public \
  --description "基于数字孪生、AI预测和可视化大屏的智能物流管理平台" \
  --source=. \
  --push
```

---

## 📋 完整命令

```bash
# 1. 登录GitHub (设备代码方式)
gh auth login --web

# 2. 按照提示在浏览器中完成认证

# 3. 创建仓库并推送
gh repo create sinotrans-logistics-control-tower \
  --public \
  --description "基于数字孪生、AI预测和可视化大屏的智能物流管理平台" \
  --source=. \
  --push
```

---

## 🔗 您的仓库地址

```
https://github.com/seenxp/sinotrans-logistics-control-tower
```

---

## ❓ 遇到问题?

### 代码过期?

如果代码过期，重新运行:
```bash
gh auth login --web
```

### 认证失败?

尝试使用Personal Access Token:
```bash
# 1. 创建Token: https://github.com/settings/tokens/new
# 2. 勾选: repo, read:org, gist
# 3. 运行:
gh auth login --with-token
# 粘贴您的token
```

---

**注意**: 设备代码有效期约10分钟，请尽快完成认证！