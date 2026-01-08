# BookForMX 安装指南

## 🔧 解决 SSL 证书问题

如果遇到 SSL 证书验证错误，请使用以下方法：

### 方法一：使用信任主机参数（推荐）

```bash
cd "/Users/a58/cursor/归档/OK 调研/bookforMX"
pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### 方法二：配置 pip 使用信任主机

创建或编辑 `~/.pip/pip.conf` 文件（macOS/Linux）：

```bash
mkdir -p ~/.pip
cat > ~/.pip/pip.conf << EOF
[global]
trusted-host = pypi.org
               pypi.python.org
               files.pythonhosted.org
EOF
```

然后正常安装：
```bash
pip3 install -r requirements.txt
```

### 方法三：使用 --user 参数

```bash
pip3 install --user --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org Flask==3.0.0 Flask-CORS==4.0.0
```

### 方法四：安装/更新证书（macOS）

```bash
# 安装 Python 证书
/Applications/Python\ 3.12/Install\ Certificates.command

# 或者手动运行
python3 -m pip install --upgrade certifi
```

## 🚀 快速启动

安装完依赖后，运行：

```bash
cd "/Users/a58/cursor/归档/OK 调研/bookforMX"
python3 app.py
```

或者使用启动脚本：

```bash
./install_and_run.sh
```

## 📱 访问应用

启动成功后，访问：http://localhost:5000

## 🆘 常见问题

### Q: 仍然提示 SSL 错误？

A: 尝试以下步骤：
1. 更新 pip: `python3 -m pip install --upgrade pip --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org`
2. 清除 pip 缓存: `pip3 cache purge`
3. 使用 `--user` 参数安装到用户目录

### Q: Permission denied 错误？

A: 使用 `--user` 参数：
```bash
pip3 install --user --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### Q: 找不到 python3？

A: 检查 Python 安装：
```bash
which python3
python3 --version
```

如果未安装，请访问 https://www.python.org/downloads/

