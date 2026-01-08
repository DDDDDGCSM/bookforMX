#!/usr/bin/env python3
"""
带 GitHub 认证的部署脚本
使用方法: python3 带认证的部署.py YOUR_TOKEN
"""
import subprocess
import os
import sys
from datetime import datetime

DIR = "/Users/a58/cursor/归档/OK 调研/bookforMX"
USER = "DDDDDGCSM"
REPO = "bookforMX"

# 从命令行参数获取 token，或从环境变量
TOKEN = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('GITHUB_TOKEN')
if not TOKEN:
    print("❌ 错误: 需要提供 GitHub Personal Access Token")
    print("   使用方法: python3 带认证的部署.py YOUR_TOKEN")
    print("   或设置环境变量: export GITHUB_TOKEN=YOUR_TOKEN")
    sys.exit(1)

# 使用 token 的 URL
URL = f"https://{TOKEN}@github.com/{USER}/{REPO}.git"
PUBLIC_URL = f"https://github.com/{USER}/{REPO}.git"

def git(args):
    r = subprocess.run(['/usr/bin/git'] + args, cwd=DIR, capture_output=True, text=True, check=False)
    return r.stdout.strip(), r.stderr.strip(), r.returncode

print("╔═══════════════════════════════════════════════════════════════╗")
print("║      🚀 BookForMX 部署执行（带认证）🚀                        ║")
print("╚═══════════════════════════════════════════════════════════════╝")
print("")
print(f"📁 目录: {DIR}")
print(f"👤 GitHub: {USER}")
print(f"📦 仓库: {REPO}")
print("")

# 1. 检查 Git 状态
print("📋 步骤 1/4: 检查 Git 状态...")
stdout, _, code = git(['status', '--short'])
if code == 0:
    count = len([l for l in stdout.split('\n') if l.strip()])
    if count > 0:
        print(f"⚠️  发现 {count} 个未提交的文件，正在添加...")
        git(['add', '.'])
        msg = f"Deploy: BookForMX - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        git(['commit', '-m', msg])
        print("✅ 已提交")
    else:
        print("✅ 所有文件已提交")
else:
    print("⚠️  无法检查状态，继续...")

# 2. 配置远程仓库（使用 token）
print("\n📋 步骤 2/4: 配置远程仓库（带认证）...")
stdout, _, code = git(['remote', 'get-url', 'origin'])
if code != 0 or not stdout:
    git(['remote', 'add', 'origin', URL])
    print(f"✅ 远程仓库已添加: {PUBLIC_URL}")
else:
    # 如果已存在，更新为带 token 的 URL
    git(['remote', 'set-url', 'origin', URL])
    print(f"✅ 远程仓库已更新: {PUBLIC_URL}")

# 3. 推送
print("\n📋 步骤 3/4: 推送到 GitHub...")
print("🚀 正在推送...")
stdout, stderr, code = git(['push', '-u', 'origin', 'main'])

if code == 0:
    print("✅ 推送成功！")
    print("")
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║          ✅ 代码已成功推送到 GitHub！                        ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print("")
    print("📝 下一步：在 Vercel 部署")
    print("  1. 访问: https://vercel.com/new")
    print("  2. 导入: bookforMX 仓库")
    print("  3. 点击: Deploy")
    print("")
    print(f"🌐 GitHub: {PUBLIC_URL}")
else:
    err = stderr[:400] if stderr else stdout[:400]
    print(f"⚠️  推送失败")
    if "repository not found" in err.lower():
        print("💡 GitHub 仓库可能还未创建")
        print("   请访问: https://github.com/new")
        print(f"   创建仓库: {REPO}")
    elif "authentication" in err.lower() or "invalid" in err.lower():
        print("💡 Token 可能无效或已过期")
        print("   请检查 Token 是否正确")
        print("   重新生成: https://github.com/settings/tokens")
    else:
        print(f"   错误: {err}")

# 4. 清理 token（安全）
print("\n📋 步骤 4/4: 清理认证信息...")
# 将远程 URL 改回公开 URL（不包含 token）
git(['remote', 'set-url', 'origin', PUBLIC_URL])
print("✅ 已清理认证信息（安全）")

print("\n📊 最终状态：")
stdout, _, code = git(['remote', 'get-url', 'origin'])
if code == 0 and PUBLIC_URL in stdout:
    print(f"   - GitHub: ✅ 已配置")
    _, _, push_code = git(['push', '-u', 'origin', 'main', '--dry-run'])
    if push_code == 0:
        print("   - 推送: ✅ 成功")
    else:
        print("   - 推送: ⏳ 待完成")
print("   - Vercel: ⏳ 待部署")
print("")

