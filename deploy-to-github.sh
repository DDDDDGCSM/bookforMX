#!/bin/bash

echo "🚀 BookForMX 部署到 GitHub"
echo "============================================================"

# 检查是否在正确的目录
if [ ! -f "app.py" ]; then
    echo "❌ 错误：请在 bookforMX 目录下运行此脚本"
    exit 1
fi

# 检查是否已经配置了remote
if git remote get-url origin &> /dev/null; then
    echo "✅ Git remote 已配置"
    echo "📍 Remote URL: $(git remote get-url origin)"
else
    echo "❌ 请先配置 GitHub 仓库地址："
    echo ""
    echo "1. 在 GitHub 创建新仓库（不要初始化 README）"
    echo "2. 运行以下命令："
    echo ""
    echo "   git remote add origin https://github.com/YOUR_USERNAME/bookforMX.git"
    echo ""
    echo "或者运行: ./一键部署.sh"
    exit 1
fi

# 初始化Git（如果需要）
if [ ! -d ".git" ]; then
    echo "📦 初始化 Git 仓库..."
    git init
    git branch -M main
fi

echo ""
echo "📦 准备提交..."
git add .
git commit -m "Update: BookForMX - $(date +'%Y-%m-%d %H:%M:%S')" 2>/dev/null || echo "代码已是最新"

echo ""
echo "🚀 推送到 GitHub..."
if git push -u origin main; then
    echo "✅ 推送成功！"
else
    echo "❌ 推送失败"
    echo ""
    echo "💡 可能需要："
    echo "  1. 输入 GitHub 用户名和密码"
    echo "  2. 或使用 Personal Access Token"
    echo "  3. 访问: https://github.com/settings/tokens"
    exit 1
fi

echo ""
echo "✅ 部署完成！"
echo ""
echo "📝 下一步："
echo "1. 访问 https://vercel.com"
echo "2. 导入你的 GitHub 仓库"
echo "3. 点击 Deploy"
echo "4. 等待部署完成，获得访问链接"
echo ""
echo "🎉 完成后即可访问你的 BookForMX 图书交换平台！"
