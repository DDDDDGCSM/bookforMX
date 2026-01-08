#!/usr/bin/env python3
import subprocess
import os
from datetime import datetime

DIR = "/Users/a58/cursor/归档/OK 调研/bookforMX"
USER = "DDDDDGCSM"
REPO = "bookforMX"
URL = f"https://github.com/{USER}/{REPO}.git"

def git(args):
    r = subprocess.run(['/usr/bin/git'] + args, cwd=DIR, capture_output=True, text=True, check=False)
    return r.stdout.strip(), r.stderr.strip(), r.returncode

print("╔═══════════════════════════════════════════════════════════════╗")
print("║         🚀 BookForMX 立即执行部署 🚀                          ║")
print("╚═══════════════════════════════════════════════════════════════╝")
print("")
print(f"📁 目录: {DIR}")
print(f"👤 GitHub: {USER}")
print(f"📦 仓库: {REPO}")
print("")

# 步骤 1
print("📋 步骤 1/5: 初始化 Git...")
if not os.path.exists(f"{DIR}/.git"):
    _, _, code = git(['init'])
    if code == 0:
        print("✅ Git 已初始化")
    else:
        print("⚠️  Git 初始化失败")
else:
    print("✅ Git 已存在")
git(['branch', '-M', 'main'])

# 步骤 2
print("\n📋 步骤 2/5: 添加文件...")
git(['add', '.'])
stdout, _, _ = git(['status', '--short'])
count = len([l for l in stdout.split('\n') if l.strip()])
print(f"✅ 已添加 {count} 个文件")

# 步骤 3
print("\n📋 步骤 3/5: 提交代码...")
msg = f"Deploy: BookForMX - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
_, stderr, code = git(['commit', '-m', msg])
if code == 0:
    stdout, _, _ = git(['log', '-1', '--pretty=format:%h'])
    print(f"✅ 已提交 (ID: {stdout})")
elif 'nothing to commit' not in stderr.lower():
    print(f"⚠️  提交失败: {stderr[:100]}")

# 步骤 4
print("\n📋 步骤 4/5: 配置远程仓库...")
stdout, _, code = git(['remote', 'get-url', 'origin'])
if code != 0 or not stdout:
    git(['remote', 'add', 'origin', URL])
    print(f"✅ 远程仓库已配置: {URL}")
elif URL not in stdout:
    git(['remote', 'remove', 'origin'])
    git(['remote', 'add', 'origin', URL])
    print(f"✅ 远程仓库已更新: {URL}")
else:
    print(f"✅ 远程仓库: {stdout}")

# 步骤 5
print("\n📋 步骤 5/5: 推送到 GitHub...")
print("🚀 正在推送...")
stdout, stderr, code = git(['push', '-u', 'origin', 'main'])
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
    print(f"🌐 GitHub: {URL}")
else:
    err = stderr[:400] if stderr else stdout[:400]
    print(f"⚠️  推送失败")
    if "repository not found" in err.lower():
        print("💡 GitHub 仓库可能还未创建")
        print("   请访问: https://github.com/new")
        print(f"   创建仓库: {REPO}")
    elif "authentication" in err.lower() or "permission" in err.lower():
        print("💡 需要 GitHub 认证")
        print("   访问: https://github.com/settings/tokens")
        print("   生成 Personal Access Token（勾选 repo 权限）")
    else:
        print(f"   错误: {err}")

print("\n📊 最终状态：")
print("   - 本地代码: ✅ 已提交")
stdout, _, code = git(['remote', 'get-url', 'origin'])
if code == 0 and stdout:
    print(f"   - GitHub: ✅ 已配置")
    _, _, push_code = git(['push', '-u', 'origin', 'main'])
    if push_code == 0:
        print("   - 推送: ✅ 成功")
    else:
        print("   - 推送: ⏳ 待完成")
else:
    print("   - GitHub: ⏳ 待配置")
print("   - Vercel: ⏳ 待部署")
print("")


