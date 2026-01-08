# 📚 BookForMX - 墨西哥图书交换平台

一个温暖的图书交换社区，让每本书找到新的主人。

## ✨ 功能特性

- 📖 **20本精选图书**：每本书都有独特的故事
- 💬 **故事分享**：了解每本书背后的情感
- 🤝 **交换申请**：简单的申请流程
- 📱 **移动端适配**：完美支持手机访问
- 💬 **WhatsApp 集成**：直接联系交换伙伴
- 🌐 **西班牙语界面**：符合本地表达习惯

## 🚀 快速部署

### 方法一：自动化部署（推荐）

#### 一键部署（半自动）

```bash
python3 一键部署.py your_github_token
```

自动完成：
- ✅ 推送到 GitHub
- ✅ 提供 Vercel 部署指引

#### 完全自动部署

```bash
python3 完全自动部署.py github_token vercel_token
```

自动完成：
- ✅ 推送到 GitHub
- ✅ 创建 Vercel 项目
- ✅ 触发部署
- ✅ 完全无需手动操作

详细说明请查看：[自动化部署说明.md](自动化部署说明.md)

### 方法二：网页部署

1. 访问: https://vercel.com/new
2. 使用 GitHub 登录
3. 导入仓库: `DDDDDGCSM/bookforMX`
4. 点击: "Deploy"

详细步骤请查看：[快速部署指南.md](快速部署指南.md)

### 方法三：使用 Vercel CLI

```bash
npm install -g vercel
vercel login
vercel
```

## 📁 项目结构

```
bookforMX/
├── app.py                    # Flask 后端应用
├── requirements.txt          # Python 依赖
├── vercel.json              # Vercel 配置
├── 一键部署.py              # 半自动部署脚本
├── 完全自动部署.py          # 全自动部署脚本
├── templates/               # HTML 模板
│   └── index.html          # 主页面
└── static/                 # 静态资源
    ├── css/
    │   └── style.css       # 样式文件
    └── js/                 # JavaScript 文件
```

## 🛠️ 本地开发

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行应用

```bash
python3 app.py
```

访问: http://localhost:5000

## 📋 技术栈

- **后端**: Flask 3.0.0
- **前端**: HTML, CSS, JavaScript
- **部署**: Vercel
- **语言**: 西班牙语

## 🌐 部署后访问

部署成功后，您将获得一个 Vercel 链接，例如：
```
https://bookformx.vercel.app
```

## 📝 更新部署

修改代码后，只需运行部署脚本：

```bash
# 使用一键部署
python3 一键部署.py your_token

# 或使用完全自动部署
python3 完全自动部署.py github_token vercel_token
```

Vercel 会自动检测并重新部署（约 1-2 分钟）

## 📚 相关文档

- [自动化部署说明.md](自动化部署说明.md) - 自动化部署详细说明
- [快速部署指南.md](快速部署指南.md) - 网页部署步骤
- [VERCEL_DEPLOY_GUIDE.md](VERCEL_DEPLOY_GUIDE.md) - Vercel 完整指南

## 🎯 下一步

1. 运行自动化部署脚本
2. 测试所有功能
3. 收集用户反馈
4. 持续优化体验

---

**祝您部署顺利！** 🚀
