# 🚀 BookForMX 快速启动

## ⚡ 一键启动（推荐）

在终端运行：

```bash
cd "/Users/a58/cursor/归档/OK 调研/bookforMX"
./install_and_run.sh
```

## 📝 手动启动步骤

### 步骤 1: 安装依赖

```bash
cd "/Users/a58/cursor/归档/OK 调研/bookforMX"
pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org Flask==3.0.0 Flask-CORS==4.0.0
```

### 步骤 2: 启动应用

```bash
python3 app.py
```

### 步骤 3: 访问应用

打开浏览器访问：**http://localhost:5000**

## 🎯 功能页面

- **图书广场**: http://localhost:5000/
- **交换墙**: http://localhost:5000/exchange-wall
- **书籍详情**: http://localhost:5000/book/1

## ⚠️ 如果遇到 SSL 错误

使用以下命令安装（添加了信任主机参数）：

```bash
pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
```

或者查看 `INSTALL.md` 获取更多解决方案。

## ✅ 启动成功标志

看到以下信息表示启动成功：

```
🚀 BookForMX - 墨西哥图书交换平台
============================================================
✅ 服务启动成功
📱 访问地址: http://localhost:5000
📚 图书广场: http://localhost:5000/
🤝 交换墙: http://localhost:5000/exchange-wall
============================================================
🛑 按 Ctrl+C 停止服务
============================================================
```

然后就可以在浏览器访问了！

