# GitHub仓库创建和推送指南

## 📋 前置条件

1. GitHub账号 (https://github.com)
2. Personal Access Token (PAT) 或 SSH密钥

---

## 🚀 方法1: 使用GitHub CLI (推荐)

### 步骤1: 登录GitHub

```bash
# 方式A: Web浏览器登录 (推荐)
gh auth login --web

# 方式B: 使用Token登录
# 1. 访问 https://github.com/settings/tokens
# 2. 点击 "Generate new token (classic)"
# 3. 勾选: repo, read:org, gist
# 4. 复制生成的token

# 然后执行:
gh auth login --with-token <<< "YOUR_TOKEN_HERE"
```

### 步骤2: 创建仓库并推送

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

## 🚀 方法2: 手动创建

### 步骤1: 在GitHub上创建仓库

1. 访问 https://github.com/new
2. 填写信息:
   - Repository name: `sinotrans-logistics-control-tower`
   - Description: `基于数字孪生、AI预测和可视化大屏的智能物流管理平台`
   - Visibility: **Public**
   - **不要勾选**任何初始化选项 (README, .gitignore, License)
3. 点击 "Create repository"

### 步骤2: 推送代码

#### 方式A: 使用HTTPS + Token

```bash
cd /home/ubuntu/sinotrans-logistics-control-tower

# 设置远程仓库 (使用Token)
git remote add origin https://YOUR_USERNAME:YOUR_TOKEN@github.com/seenxp/sinotrans-logistics-control-tower.git

# 或者使用 (会提示输入用户名和密码)
git remote add origin https://github.com/seenxp/sinotrans-logistics-control-tower.git

# 推送代码
git branch -M main
git push -u origin main
```

#### 方式B: 使用SSH

```bash
cd /home/ubuntu/sinotrans-logistics-control-tower

# 1. 首先将SSH公钥添加到GitHub
cat ~/.ssh/id_ed25519.pub
# 复制输出的内容

# 2. 访问 https://github.com/settings/ssh/new
# 3. 粘贴公钥并保存

# 4. 设置远程仓库
git remote add origin git@github.com:seenxp/sinotrans-logistics-control-tower.git

# 5. 推送代码
git branch -M main
git push -u origin main
```

---

## 🔧 故障排除

### 问题1: 认证失败

```bash
# 清除缓存的凭证
gh auth logout
git credential reject <<EOF
protocol=https
host=github.com
EOF

# 重新登录
gh auth login --web
```

### 问题2: 权限不足

确保Token有以下权限:
- repo (完整仓库访问)
- read:org
- gist

### 问题3: SSH连接失败

```bash
# 测试SSH连接
ssh -T git@github.com

# 如果失败，检查SSH配置
cat ~/.ssh/config

# 添加GitHub配置
echo "Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519" >> ~/.ssh/config
```

---

## ✅ 验证推送成功

推送后访问:
```
https://github.com/seenxp/sinotrans-logistics-control-tower
```

应该能看到所有项目文件。

---

## 📝 快速命令汇总

```bash
# 一键创建并推送 (需要先登录gh)
cd /home/ubuntu/sinotrans-logistics-control-tower
gh auth login --web
gh repo create sinotrans-logistics-control-tower --public --source=. --push
```

---

**提示**: 如果您能提供GitHub Personal Access Token，我可以直接帮您完成推送！