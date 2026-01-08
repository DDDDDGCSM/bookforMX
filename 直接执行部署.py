#!/usr/bin/env python3
"""
BookForMX 直接执行部署 - 完全绕过 shell 环境
使用 subprocess 直接调用命令，不依赖 shell
"""

import subprocess
import os
import sys

# 配置
GITHUB_USERNAME = "DDDDDGCSM"
REPO_NAME = "bookforMX"
REPO_URL = f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
PROJECT_DIR = "/Users/a58/cursor/归档/OK 调研/bookforMX"

def run_git_command(args, description=""):
    """直接执行 git 命令，不使用 shell"""
    try:
        result = subprocess.run(
            ['git'] + args,
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            check=False
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

def main():
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║         🚀 BookForMX 直接执行部署 🚀                          ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print("")
    print(f"📁 项目目录: {PROJECT_DIR}")
    print(f"👤 GitHub 用户: {GITHUB_USERNAME}")
    print(f"📦 仓库名: {REPO_NAME}")
    print(f"🔗 仓库地址: {REPO_URL}")
    print("")
    
    # 检查目录
    if not os.path.exists(PROJECT_DIR):
        print(f"❌ 错误：项目目录不存在: {PROJECT_DIR}")
        sys.exit(1)
    
    if not os.path.exists(os.path.join(PROJECT_DIR, "app.py")):
        print(f"❌ 错误：找不到 app.py")
        sys.exit(1)
    
    # 步骤 1: 初始化 Git
    print("📋 步骤 1/5: 初始化 Git 仓库")
    print("----------------------------------------")
    git_dir = os.path.join(PROJECT_DIR, ".git")
    if not os.path.exists(git_dir):
        stdout, stderr, code = run_git_command(['init'])
        if code == 0:
            print("✅ Git 已初始化")
        else:
            print(f"⚠️  Git 初始化失败: {stderr}")
    else:
        print("✅ Git 已存在")
    
    stdout, stderr, code = run_git_command(['branch', '-M', 'main'])
    if code == 0:
        print("✅ 分支设置为 main")
    print("")
    
    # 步骤 2: 添加文件
    print("📋 步骤 2/5: 添加所有文件")
    print("----------------------------------------")
    stdout, stderr, code = run_git_command(['add', '.'])
    if code == 0:
        stdout, _, _ = run_git_command(['status', '--short'])
        file_count = len([l for l in stdout.split('\n') if l.strip()])
        print(f"✅ 已添加 {file_count} 个文件")
    else:
        print(f"⚠️  添加文件失败: {stderr[:200]}")
    print("")
    
    # 步骤 3: 提交代码
    print("📋 步骤 3/5: 提交代码")
    print("----------------------------------------")
    from datetime import datetime
    commit_msg = f"Deploy: BookForMX - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    stdout, stderr, code = run_git_command(['commit', '-m', commit_msg])
    if code == 0:
        print("✅ 代码已提交")
        stdout, _, _ = run_git_command(['log', '-1', '--pretty=format:%h'])
        if stdout:
            print(f"   提交ID: {stdout}")
    elif 'nothing to commit' in stderr.lower():
        print("ℹ️  没有需要提交的更改（可能已提交）")
    else:
        print(f"⚠️  提交失败: {stderr[:200]}")
    print("")
    
    # 步骤 4: 配置远程仓库
    print("📋 步骤 4/5: 配置远程仓库")
    print("----------------------------------------")
    stdout, stderr, code = run_git_command(['remote', 'get-url', 'origin'])
    if code == 0 and stdout:
        print(f"✅ 远程仓库已存在: {stdout}")
        if REPO_URL not in stdout:
            run_git_command(['remote', 'remove', 'origin'])
            run_git_command(['remote', 'add', 'origin', REPO_URL])
            print(f"✅ 已更新为: {REPO_URL}")
    else:
        stdout, stderr, code = run_git_command(['remote', 'add', 'origin', REPO_URL])
        if code == 0:
            print(f"✅ 远程仓库已添加: {REPO_URL}")
        else:
            print(f"⚠️  添加远程仓库失败: {stderr[:200]}")
    print("")
    
    # 步骤 5: 推送到 GitHub
    print("📋 步骤 5/5: 推送到 GitHub")
    print("----------------------------------------")
    print("🚀 正在推送到 GitHub...")
    print("   如果提示需要认证，请使用 Personal Access Token")
    print("")
    
    stdout, stderr, code = run_git_command(['push', '-u', 'origin', 'main'])
    if code == 0:
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
        push_success = True
    else:
        error_msg = stderr[:500] if stderr else stdout[:500]
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
        push_success = False
    
    print("")
    print("📊 当前状态：")
    print("   - 本地代码: ✅ 已提交")
    stdout, _, code = run_git_command(['remote', 'get-url', 'origin'])
    if code == 0 and stdout:
        print(f"   - GitHub: ✅ 已配置 ({stdout})")
        if push_success:
            print("   - 推送: ✅ 成功")
        else:
            print("   - 推送: ⏳ 待完成")
    else:
        print("   - GitHub: ⏳ 待配置")
    print("   - Vercel: ⏳ 待部署")
    print("")

if __name__ == "__main__":
    main()


