#!/bin/bash

clear
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         🚀 BookForMX 一键部署助手 🚀                          ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# 检查是否在正确的目录
if [ ! -f "app.py" ]; then
    echo "❌ 错误：请在 bookforMX 目录下运行此脚本"
    echo "   cd '/Users/a58/cursor/归档/OK 调研/bookforMX'"
    exit 1
fi

echo "📋 准备工作..."
echo ""

# 配置 Git 用户信息
echo "🔧 步骤 1/5: 配置 Git 用户信息"
echo "----------------------------------------"
read -p "请输入您的 GitHub 用户名: " github_username
read -p "请输入您的邮箱: " github_email

git config --global user.name "$github_username"
git config --global user.email "$github_email"

echo "✅ Git 配置完成"
echo ""

# 获取 GitHub 仓库名
echo "🔧 步骤 2/5: 准备 GitHub 仓库"
echo "----------------------------------------"
echo "请先在浏览器中完成以下操作："
echo "  1. 访问 https://github.com/new"
echo "  2. 仓库名称输入: bookforMX"
echo "  3. 选择 Public（公开）"
echo "  4. 不要勾选 'Add a README file'"
echo "  5. 不要勾选 'Add .gitignore'"
echo "  6. 不要勾选 'Choose a license'"
echo "  7. 点击 'Create repository'"
echo ""
read -p "完成后按回车继续..."
echo ""

# 初始化Git（如果需要）
if [ ! -d ".git" ]; then
    echo "📦 初始化 Git 仓库..."
    git init
    git branch -M main
    echo "✅ Git 已初始化"
fi

# 添加远程仓库
echo "🔧 步骤 3/5: 连接 GitHub 仓库"
echo "----------------------------------------"
git_url="https://github.com/$github_username/bookforMX.git"
echo "正在连接到: $git_url"

# 删除已存在的 origin（如果有）
git remote remove origin 2>/dev/null

git remote add origin "$git_url"
echo "✅ 仓库连接成功"
echo ""

# 提交代码
echo "🔧 步骤 4/5: 推送代码到 GitHub"
echo "----------------------------------------"
git add .
git commit -m "Deploy: BookForMX 图书交换平台 - $(date +'%Y-%m-%d %H:%M:%S')" 2>/dev/null || echo "代码已是最新"

echo "正在推送到 GitHub..."
if git push -u origin main; then
    echo "✅ 代码推送成功！"
else
    echo "❌ 推送失败，可能需要输入 GitHub 密码或 Personal Access Token"
    echo ""
    echo "💡 如果需要 Token，请："
    echo "  1. 访问 https://github.com/settings/tokens"
    echo "  2. 点击 'Generate new token (classic)'"
    echo "  3. 勾选 'repo' 权限"
    echo "  4. 生成并复制 token"
    echo "  5. 使用 token 作为密码重新运行此脚本"
    exit 1
fi
echo ""

# 部署到 Vercel
echo "🔧 步骤 5/5: 部署到 Vercel"
echo "----------------------------------------"
echo "接下来请在浏览器中完成部署："
echo ""
echo "  1. 访问 https://vercel.com/signup"
echo "  2. 点击 'Continue with GitHub' 使用 GitHub 登录"
echo "  3. 授权 Vercel 访问您的 GitHub"
echo "  4. 点击 'Import Project'"
echo "  5. 选择 'bookforMX' 仓库"
echo "  6. 保持默认设置，点击 'Deploy'"
echo "  7. 等待 1-2 分钟部署完成"
echo ""
echo "📱 部署完成后，您将获得一个访问链接！"
echo ""

# 自动打开浏览器
read -p "是否自动打开 Vercel 网站？(y/n): " open_browser
if [ "$open_browser" = "y" ] || [ "$open_browser" = "Y" ]; then
    open "https://vercel.com/new"
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                    🎉 部署准备完成！                          ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "✅ GitHub 仓库: https://github.com/$github_username/bookforMX"
echo "✅ 代码已推送"
echo "🚀 等待 Vercel 部署..."
echo ""
echo "💡 提示："
echo "  - Vercel 部署通常需要 1-2 分钟"
echo "  - 部署完成后会自动生成访问链接"
echo "  - 每次推送代码都会自动重新部署"
echo ""
echo "🆘 需要帮助？查看 DEPLOY_VERCEL.md"
echo ""
