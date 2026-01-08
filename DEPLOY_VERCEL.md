# BookForMX Vercel 部署指南

参考 smartval-simple 项目的部署方式，快速部署 BookForMX 到 Vercel。

## 🚀 快速部署（3步完成）

### 第一步：创建 GitHub 仓库

1. 访问 [GitHub](https://github.com/new)
2. 仓库名称：`bookforMX`
3. **重要**：不要勾选 "Initialize this repository with a README"
4. 点击 "Create repository"

### 第二步：上传代码到 GitHub

在终端执行：

```bash
cd "/Users/a58/cursor/归档/OK 调研/bookforMX"

# 初始化 Git（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: BookForMX"

# 添加远程仓库（替换 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/bookforMX.git

# 推送代码
git push -u origin main
```

**如果提示需要认证**：
- 使用 GitHub Personal Access Token 代替密码
- 访问：https://github.com/settings/tokens
- 生成 token（勾选 `repo` 权限）

### 第三步：部署到 Vercel

1. 访问 [Vercel](https://vercel.com)
2. 使用 GitHub 账号登录
3. 点击 **"New Project"**
4. 导入 `bookforMX` 仓库
5. **配置设置**：
   - Framework Preset: **Other**
   - Root Directory: `./`（默认）
   - Build Command: （留空）
   - Output Directory: （留空）
6. 点击 **"Deploy"**
7. 等待 1-2 分钟部署完成

## ✅ 部署完成

部署成功后，你将获得：
- ✅ 访问链接：`https://bookformx.vercel.app`（或自定义域名）
- ✅ 自动 HTTPS 证书
- ✅ 全球 CDN 加速
- ✅ 自动重新部署（每次 push 到 GitHub）

## 📱 访问你的应用

部署完成后：
- 主页面：`https://your-project.vercel.app/`
- 所有功能都在一个页面完成

## 🔧 环境变量（可选）

目前应用使用模拟数据，**无需配置环境变量**。

如需添加数据库等功能，可在 Vercel 项目设置中添加：
- `DATABASE_URL` - 数据库连接
- `SECRET_KEY` - Flask 密钥

## 🔄 更新部署

每次修改代码后：

```bash
git add .
git commit -m "Update: 描述更改"
git push origin main
```

Vercel 会自动重新部署（约 1-2 分钟）

## 🆘 常见问题

### Q: 部署失败？
A: 检查：
1. `vercel.json` 配置是否正确
2. `requirements.txt` 是否包含所有依赖
3. 查看 Vercel 部署日志

### Q: 页面显示 404？
A: 确保：
1. 代码已推送到 GitHub
2. `app.py` 中有 `@app.route('/')` 路由
3. `templates/index.html` 文件存在

### Q: 如何绑定自定义域名？
A: 
1. Vercel Dashboard → 项目 → Settings → Domains
2. 添加你的域名
3. 按提示配置 DNS 记录

## 📊 项目结构

```
bookforMX/
├── app.py              # Flask 后端
├── requirements.txt    # Python 依赖
├── vercel.json        # Vercel 配置
├── templates/
│   └── index.html     # 主页面
└── static/            # 静态资源（可选）
```

## 🎯 与 smartval-simple 的对比

| 项目 | BookForMX | smartval-simple |
|------|-----------|----------------|
| 框架 | Flask | Flask |
| 部署 | Vercel | Vercel |
| 配置 | vercel.json | vercel.json |
| 数据库 | 模拟数据 | 可选（Neon/Supabase） |
| 复杂度 | 简单 | 中等 |

## ✨ 部署优势

- ✅ **零配置**：无需服务器，无需数据库（当前版本）
- ✅ **自动部署**：Git push 即部署
- ✅ **全球加速**：Vercel CDN
- ✅ **免费额度**：足够个人项目使用

---

**部署完成后，分享链接给用户即可使用！** 🎉


