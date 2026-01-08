#!/usr/bin/env python3
"""
BookForMX 自动化部署脚本
使用 Python 执行 Git 操作，避免 shell 环境问题
"""

import subprocess
import os
import sys
from datetime import datetime

def run_cmd(cmd, check=True):
    """执行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=check
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.CalledProcessError as e:
        return e.stdout.strip(), e.stderr.strip(), e.returncode

def main():
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║         🚀 BookForMX 自动化部署 🚀                            ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print("")
    
    # 切换到脚本目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"📁 工作目录: {os.getcwd()}")
    print("")
    
    # 检查 app.py
    if not os.path.exists("app.py"):
        print("❌ 错误：找不到 app.py，请在 bookforMX 目录下运行")
        sys.exit(1)
    
    # 步骤 1: 初始化 Git
    print("📋 步骤 1/4: 初始化 Git 仓库")
    print("----------------------------------------")
    if not os.path.exists(".git"):
        stdout, stderr, code = run_cmd("git init", check=False)
        if code == 0:
            print("✅ Git 已初始化")
        else:
            print(f"⚠️  Git 初始化失败: {stderr}")
    else:
        print("✅ Git 已存在")
    
    # 设置分支
    stdout, stderr, code = run_cmd("git branch -M main", check=False)
    if code == 0:
        print("✅ 分支设置为 main")
    print("")
    
    # 步骤 2: 添加文件
    print("📋 步骤 2/4: 添加所有文件")
    print("----------------------------------------")
    stdout, stderr, code = run_cmd("git add .", check=False)
    if code == 0:
        # 统计文件数
        stdout, _, _ = run_cmd("git status --short", check=False)
        file_count = len([l for l in stdout.split('\n') if l.strip()])
        print(f"✅ 已添加文件到暂存区")
    else:
        print(f"⚠️  添加文件失败: {stderr}")
    print("")
    
    # 步骤 3: 提交
    print("📋 步骤 3/4: 提交代码")
    print("----------------------------------------")
    commit_msg = f"Deploy: BookForMX - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    stdout, stderr, code = run_cmd(f'git commit -m "{commit_msg}"', check=False)
    if code == 0:
        print("✅ 代码已提交")
        # 获取提交hash
        stdout, _, _ = run_cmd("git log -1 --pretty=format:%h", check=False)
        if stdout:
            print(f"   提交ID: {stdout}")
    else:
        if "nothing to commit" in stderr.lower():
            print("ℹ️  没有需要提交的更改")
        else:
            print(f"⚠️  提交失败: {stderr}")
    print("")
    
    # 步骤 4: 检查远程仓库
    print("📋 步骤 4/4: 检查远程仓库")
    print("----------------------------------------")
    stdout, stderr, code = run_cmd("git remote get-url origin", check=False)
    if code == 0 and stdout:
        print(f"✅ 远程仓库已配置: {stdout}")
        print("")
        print("🚀 推送到 GitHub...")
        stdout, stderr, code = run_cmd("git push -u origin main", check=False)
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
        else:
            print(f"⚠️  推送失败: {stderr}")
            print("")
            print("💡 可能需要：")
            print("  - 输入 GitHub 用户名和密码")
            print("  - 或使用 Personal Access Token")
            print("  - 访问: https://github.com/settings/tokens")
    else:
        print("⚠️  远程仓库未配置")
        print("")
        print("📝 下一步操作：")
        print("")
        print("1️⃣  创建 GitHub 仓库：")
        print("   访问: https://github.com/new")
        print("   仓库名: bookforMX")
        print("   不要勾选任何选项")
        print("   点击: Create repository")
        print("")
        print("2️⃣  连接并推送：")
        print("   执行以下命令（替换 YOUR_USERNAME）：")
        print("")
        print("   git remote add origin https://github.com/YOUR_USERNAME/bookforMX.git")
        print("   git push -u origin main")
        print("")
    
    print("")
    print("📊 当前状态：")
    print("   - 本地代码: ✅ 已提交")
    stdout, _, code = run_cmd("git remote get-url origin", check=False)
    if code == 0 and stdout:
        print("   - GitHub: ✅ 已配置")
    else:
        print("   - GitHub: ⏳ 待配置")
    print("   - Vercel: ⏳ 待部署")
    print("")

if __name__ == "__main__":
    main()


