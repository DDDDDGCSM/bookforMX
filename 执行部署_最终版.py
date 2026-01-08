#!/usr/bin/env python3
import subprocess, os, sys
from datetime import datetime

DIR = "/Users/a58/cursor/归档/OK 调研/bookforMX"
USER = "DDDDDGCSM"
REPO = "bookforMX"
URL = f"https://github.com/{USER}/{REPO}.git"

def git(args):
    r = subprocess.run(['git'] + args, cwd=DIR, capture_output=True, text=True, check=False)
    return r.stdout.strip(), r.stderr.strip(), r.returncode

print("🚀 BookForMX 部署执行中...\n")

# 1. 初始化
if not os.path.exists(f"{DIR}/.git"):
    git(['init'])
    print("✅ Git 初始化")
git(['branch', '-M', 'main'])

# 2. 添加
git(['add', '.'])
stdout, _, _ = git(['status', '--short'])
count = len([l for l in stdout.split('\n') if l.strip()])
print(f"✅ 已添加 {count} 个文件")

# 3. 提交
msg = f"Deploy: BookForMX - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
_, stderr, code = git(['commit', '-m', msg])
if code == 0:
    stdout, _, _ = git(['log', '-1', '--pretty=format:%h'])
    print(f"✅ 已提交 (ID: {stdout})")
elif 'nothing to commit' not in stderr.lower():
    print(f"⚠️  提交失败: {stderr[:100]}")

# 4. 远程
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

# 5. 推送
print("\n🚀 推送到 GitHub...")
stdout, stderr, code = git(['push', '-u', 'origin', 'main'])
if code == 0:
    print("✅ 推送成功！")
    print(f"\n🌐 GitHub: {URL}")
    print("\n📝 下一步：在 Vercel 部署")
    print("  访问: https://vercel.com/new")
    print("  导入: bookforMX 仓库")
else:
    err = stderr[:300] if stderr else stdout[:300]
    print(f"⚠️  推送失败")
    if "repository not found" in err.lower():
        print("💡 请先创建 GitHub 仓库: https://github.com/new")
    elif "authentication" in err.lower():
        print("💡 需要认证，使用 Personal Access Token")
        print("   访问: https://github.com/settings/tokens")
    else:
        print(f"   错误: {err}")

print("\n📊 状态：")
print("   - 本地代码: ✅ 已提交")
stdout, _, code = git(['remote', 'get-url', 'origin'])
if code == 0 and stdout:
    print(f"   - GitHub: ✅ 已配置")
    if code == 0:  # 检查推送结果
        push_check = git(['push', '-u', 'origin', 'main'])
        if push_check[2] == 0:
            print("   - 推送: ✅ 成功")
        else:
            print("   - 推送: ⏳ 待完成")
print("   - Vercel: ⏳ 待部署")


