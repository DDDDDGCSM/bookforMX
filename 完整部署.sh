#!/bin/bash

# BookForMX 完整自动化部署脚本
# 请在您的终端直接执行此脚本

set -e  # 遇到错误立即退出

cd "$(dirname "$0")"

clear
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         🚀 BookForMX 完整自动化部署 🚀                        ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# 检查目录
if [ ! -f "app.py" ]; then
    echo "❌ 错误：请在 bookforMX 目录下运行"
    exit 1
fi

echo "📋 步骤 1/5: 初始化 Git 仓库"
echo "----------------------------------------"
if [ ! -d ".git" ]; then
    git init
    git branch -M main
    echo "✅ Git 已初始化"
else
    echo "✅ Git 已存在"
fi

echo ""
echo "📋 步骤 2/5: 添加所有文件"
echo "----------------------------------------"
git add .
FILE_COUNT=$(git status --short | wc -l | tr -d ' ')
echo "✅ 已添加 $FILE_COUNT 个文件"

echo ""
echo "📋 步骤 3/5: 提交代码"
echo "----------------------------------------"
git commit -m "Deploy: BookForMX 图书交换平台 - $(date +'%Y-%m-%d %H:%M:%S')" 2>/dev/null || \
git commit -m "Deploy: BookForMX"
COMMIT_HASH=$(git log -1 --pretty=format:"%h")
echo "✅ 代码已提交 (commit: $COMMIT_HASH)"

echo ""
echo "📋 步骤 4/5: 检查远程仓库"
echo "----------------------------------------"
if git remote get-url origin &> /dev/null; then
    REMOTE_URL=$(git remote get-url origin)
    echo "✅ 远程仓库已配置: $REMOTE_URL"
    echo ""
    echo "🚀 推送到 GitHub..."
    if git push -u origin main; then
        echo "✅ 推送成功！"
        PUSH_SUCCESS=true
    else
        echo "⚠️  推送失败，请检查认证信息"
        PUSH_SUCCESS=false
    fi
else
    echo "⚠️  远程仓库未配置"
    PUSH_SUCCESS=false
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
if [ "$PUSH_SUCCESS" = true ]; then
    echo "║              ✅ 代码已推送到 GitHub！                        ║"
else
    echo "║              ⚠️  需要配置 GitHub 仓库                         ║"
fi
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

if [ "$PUSH_SUCCESS" = false ]; then
    echo "📝 下一步操作："
    echo ""
    echo "1️⃣  创建 GitHub 仓库："
    echo "   访问: https://github.com/new"
    echo "   仓库名: bookforMX"
    echo "   不要勾选任何选项"
    echo "   点击: Create repository"
    echo ""
    echo "2️⃣  连接并推送："
    echo "   执行以下命令（替换 YOUR_USERNAME）："
    echo ""
    echo "   git remote add origin https://github.com/YOUR_USERNAME/bookforMX.git"
    echo "   git push -u origin main"
    echo ""
fi

echo "3️⃣  在 Vercel 部署："
echo "   访问: https://vercel.com/new"
echo "   导入: bookforMX 仓库"
echo "   点击: Deploy"
echo ""

# 显示当前状态
echo "📊 当前状态："
echo "   - 本地代码: ✅ 已提交"
if [ "$PUSH_SUCCESS" = true ]; then
    echo "   - GitHub: ✅ 已推送"
else
    echo "   - GitHub: ⏳ 待配置"
fi
echo "   - Vercel: ⏳ 待部署"
echo ""

echo "💡 提示："
echo "   - 如果推送需要认证，使用 Personal Access Token"
echo "   - 访问: https://github.com/settings/tokens"
echo "   - 生成 token（勾选 repo 权限）"
echo ""


