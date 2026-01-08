#!/bin/bash

# BookForMX 立即部署脚本
# 执行此脚本完成自动化部署

cd "$(dirname "$0")"

clear
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         🚀 BookForMX 立即部署 🚀                              ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# 检查目录
if [ ! -f "app.py" ]; then
    echo "❌ 错误：请在 bookforMX 目录下运行"
    exit 1
fi

echo "📋 步骤 1/4: 初始化 Git..."
echo "----------------------------------------"

# 初始化Git
if [ ! -d ".git" ]; then
    git init
    git branch -M main
    echo "✅ Git 已初始化"
else
    echo "✅ Git 已存在"
fi

# 添加文件
echo ""
echo "📋 步骤 2/4: 添加文件..."
git add .
echo "✅ 文件已添加"

# 提交
echo ""
echo "📋 步骤 3/4: 提交代码..."
git commit -m "Deploy: BookForMX - $(date +'%Y-%m-%d %H:%M:%S')" 2>/dev/null || git commit -m "Deploy: BookForMX"
echo "✅ 代码已提交"

# 检查远程仓库
echo ""
echo "📋 步骤 4/4: 检查远程仓库..."
if git remote get-url origin &> /dev/null; then
    REMOTE_URL=$(git remote get-url origin)
    echo "✅ 远程仓库已配置: $REMOTE_URL"
    echo ""
    echo "🚀 推送到 GitHub..."
    if git push -u origin main; then
        echo "✅ 推送成功！"
        echo ""
        echo "🎉 代码已推送到 GitHub！"
        echo ""
        echo "📝 下一步：在 Vercel 部署"
        echo "  1. 访问: https://vercel.com/new"
        echo "  2. 导入 bookforMX 仓库"
        echo "  3. 点击 Deploy"
    else
        echo "❌ 推送失败，请检查："
        echo "  - GitHub 仓库是否已创建"
        echo "  - 认证信息是否正确"
        echo "  - 是否需要 Personal Access Token"
    fi
else
    echo "⚠️  远程仓库未配置"
    echo ""
    echo "请先创建 GitHub 仓库，然后执行："
    echo ""
    echo "  git remote add origin https://github.com/YOUR_USERNAME/bookforMX.git"
    echo "  git push -u origin main"
    echo ""
    echo "或者运行: ./一键部署.sh"
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                    部署准备完成！                              ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""


