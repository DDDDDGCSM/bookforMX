#!/bin/bash

# 安装依赖并启动应用的脚本

cd "$(dirname "$0")"

echo "🔧 BookForMX 安装和启动脚本"
echo "================================"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3"
    echo "请先安装 Python 3"
    exit 1
fi

echo "✅ Python 版本: $(python3 --version)"
echo ""

# 检查Flask是否已安装
if python3 -c "import flask" 2>/dev/null; then
    echo "✅ Flask 已安装"
    FLASK_VERSION=$(python3 -c "import flask; print(flask.__version__)" 2>/dev/null)
    echo "   版本: $FLASK_VERSION"
    echo ""
else
    echo "📦 正在安装依赖..."
    echo ""
    
    # 尝试多种安装方法
    echo "方法 1: 使用 --trusted-host 参数..."
    if python3 -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org Flask==3.0.0 Flask-CORS==4.0.0 2>&1 | tee /tmp/pip_install.log; then
        echo "✅ 依赖安装成功！"
    else
        echo "⚠️  方法 1 失败，尝试方法 2: 使用 --user 参数..."
        if python3 -m pip install --user --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org Flask==3.0.0 Flask-CORS==4.0.0 2>&1 | tee /tmp/pip_install.log; then
            echo "✅ 依赖安装成功（用户目录）！"
        else
            echo "❌ 安装失败"
            echo ""
            echo "请手动运行以下命令："
            echo "  pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt"
            echo ""
            echo "或查看 INSTALL.md 获取更多帮助"
            exit 1
        fi
    fi
    echo ""
fi

# 验证安装
if ! python3 -c "import flask" 2>/dev/null; then
    echo "❌ Flask 安装验证失败"
    exit 1
fi

echo "🚀 启动 Flask 应用..."
echo "================================"
echo "📱 访问地址: http://localhost:5000"
echo "🛑 按 Ctrl+C 停止服务"
echo "================================"
echo ""

# 启动应用
python3 app.py

