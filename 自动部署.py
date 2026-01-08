#!/usr/bin/env python3
"""
BookForMX 自动部署脚本
使用 GitHub 用户名: DDDDDGCSM
"""

import subprocess
import os
import sys

# 配置
GITHUB_USERNAME = "DDDDDGCSM"
REPO_NAME = "bookforMX"
REPO_URL = f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"

# 切换到项目目录
project_dir = "/Users/a58/cursor/归档/OK 调研/bookforMX"
os.chdir(project_dir)

print("╔═══════════════════════════════════════════════════════════════╗")
print("║         🚀 BookForMX 自动部署 🚀                              ║")
print("╚═══════════════════════════════════════════════════════════════╝")
print("")
print(f"📁 项目目录: {project_dir}")
print(f"👤 GitHub 用户: {GITHUB_USERNAME}")
print(f"📦 仓库名: {REPO_NAME}")
print(f"🔗 仓库地址: {REPO_URL}")
print("")

# 步骤 1: 初始化 Git
print("📋 步骤 1/5: 初始化 Git 仓库")
print("----------------------------------------")
if not os.path.exists('.git'):
    result = subprocess.run(['git', 'init'], capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Git 已初始化")
    else:
        print(f"⚠️  Git 初始化失败: {result.stderr}")
        sys.exit(1)
else:
    print("✅ Git 已存在")

result = subprocess.run(['git', 'branch', '-M', 'main'], capture_output=True, text=True)
if result.returncode == 0:
    print("✅ 分支设置为 main")
print("")

# 步骤 2: 添加文件
print("📋 步骤 2/5: 添加所有文件")
print("----------------------------------------")
result = subprocess.run(['git', 'add', '.'], capture_output=True, text=True)
if result.returncode == 0:
    # 统计文件数
    status = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True)
    file_count = len([l for l in status.stdout.split('\n') if l.strip()])
    print(f"✅ 已添加 {file_count} 个文件")
else:
    print(f"⚠️  添加文件失败: {result.stderr}")
print("")

# 步骤 3: 提交代码
print("📋 步骤 3/5: 提交代码")
print("----------------------------------------")
from datetime import datetime
commit_msg = f"Deploy: BookForMX - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
result = subprocess.run(['git', 'commit', '-m', commit_msg], capture_output=True, text=True)
if result.returncode == 0:
    print("✅ 代码已提交")
    # 获取提交hash
    commit_hash = subprocess.run(['git', 'log', '-1', '--pretty=format:%h'], 
                                capture_output=True, text=True)
    if commit_hash.stdout:
        print(f"   提交ID: {commit_hash.stdout.strip()}")
elif 'nothing to commit' in result.stderr.lower():
    print("ℹ️  没有需要提交的更改（可能已提交）")
else:
    print(f"⚠️  提交失败: {result.stderr[:200]}")
print("")

# 步骤 4: 配置远程仓库
print("📋 步骤 4/5: 配置远程仓库")
print("----------------------------------------")
# 检查是否已存在
check_remote = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                              capture_output=True, text=True)
if check_remote.returncode == 0 and check_remote.stdout.strip():
    print(f"✅ 远程仓库已存在: {check_remote.stdout.strip()}")
    # 如果URL不对，更新它
    if REPO_URL not in check_remote.stdout:
        subprocess.run(['git', 'remote', 'remove', 'origin'], check=False)
        subprocess.run(['git', 'remote', 'add', 'origin', REPO_URL], check=False)
        print(f"✅ 已更新为: {REPO_URL}")
else:
    # 添加远程仓库
    result = subprocess.run(['git', 'remote', 'add', 'origin', REPO_URL], 
                           capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ 远程仓库已添加: {REPO_URL}")
    else:
        print(f"⚠️  添加远程仓库失败: {result.stderr}")
print("")

# 步骤 5: 推送到 GitHub
print("📋 步骤 5/5: 推送到 GitHub")
print("----------------------------------------")
print("🚀 正在推送到 GitHub...")
print("   如果提示需要认证，请使用 Personal Access Token")
print("")

result = subprocess.run(['git', 'push', '-u', 'origin', 'main'], 
                       capture_output=True, text=True)
if result.returncode == 0:
    print("✅ 推送成功！")
    print("")
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║              ✅ 代码已推送到 GitHub！                        ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print("")
    print("📝 下一步：在 Vercel 部署")
    print("  1. 访问: https://vercel.com/new")
    print("  2. 导入: bookforMX 仓库")
    print("  3. 点击: Deploy")
    print("")
    print(f"🌐 GitHub 仓库: {REPO_URL}")
else:
    error_msg = result.stderr[:500] if result.stderr else result.stdout[:500]
    print(f"⚠️  推送失败")
    print("")
    if "repository not found" in error_msg.lower():
        print("💡 提示: GitHub 仓库可能还未创建")
        print("   请先访问: https://github.com/new")
        print(f"   创建仓库: {REPO_NAME}")
        print("   然后重新运行此脚本")
    elif "authentication" in error_msg.lower() or "permission" in error_msg.lower():
        print("💡 提示: 需要 GitHub 认证")
        print("   1. 访问: https://github.com/settings/tokens")
        print("   2. 生成 Personal Access Token（勾选 repo 权限）")
        print("   3. 使用 token 作为密码")
        print("   4. 重新运行此脚本")
    else:
        print(f"   错误信息: {error_msg}")

print("")
print("📊 当前状态：")
print("   - 本地代码: ✅ 已提交")
check_remote = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                              capture_output=True, text=True)
if check_remote.returncode == 0 and check_remote.stdout.strip():
    print(f"   - GitHub: ✅ 已配置 ({check_remote.stdout.strip()})")
    if result.returncode == 0:
        print("   - 推送: ✅ 成功")
    else:
        print("   - 推送: ⏳ 待完成")
else:
    print("   - GitHub: ⏳ 待配置")
print("   - Vercel: ⏳ 待部署")
print("")


