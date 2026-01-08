#!/bin/bash

# BookForMX 启动脚本

cd "$(dirname "$0")"

echo "🚀 启动 BookForMX..."
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3"
    exit 1
fi

# 检查Flask是否已安装
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📦 正在安装依赖..."
    echo ""
    
    # 尝试使用不同的方法安装
    if python3 -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org Flask==3.0.0 Flask-CORS==4.0.0 2>&1; then
        echo "✅ 依赖安装成功"
    else
        echo "⚠️  尝试使用 --user 安装..."
        python3 -m pip install --user --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org Flask==3.0.0 Flask-CORS==4.0.0
    fi
fi

echo ""
echo "✅ 启动 Flask 应用..."
echo "📱 访问地址: http://localhost:5000"
echo "🛑 按 Ctrl+C 停止服务"
echo ""

# 启动应用
python3 app.py

