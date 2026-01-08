#!/usr/bin/env python3
"""
直接执行部署 - 不使用 shell
"""

import subprocess
import os

os.chdir('/Users/a58/cursor/归档/OK 调研/bookforMX')

print("🚀 开始部署 BookForMX...")
print("")

# 1. 初始化 Git
print("📋 步骤 1: 初始化 Git...")
if not os.path.exists('.git'):
    subprocess.run(['git', 'init'], check=False)
    print("✅ Git 已初始化")
else:
    print("✅ Git 已存在")

subprocess.run(['git', 'branch', '-M', 'main'], check=False)
print("✅ 分支设置为 main")
print("")

# 2. 添加文件
print("📋 步骤 2: 添加文件...")
subprocess.run(['git', 'add', '.'], check=False)
print("✅ 文件已添加")
print("")

# 3. 提交
print("📋 步骤 3: 提交代码...")
result = subprocess.run(['git', 'commit', '-m', 'Deploy: BookForMX'], 
                       capture_output=True, text=True, check=False)
if result.returncode == 0:
    print("✅ 代码已提交")
    commit = subprocess.run(['git', 'log', '-1', '--pretty=format:%h'], 
                          capture_output=True, text=True)
    if commit.stdout:
        print(f"   提交ID: {commit.stdout.strip()}")
elif 'nothing to commit' in result.stderr.lower():
    print("ℹ️  没有需要提交的更改")
else:
    print(f"⚠️  {result.stderr[:100]}")
print("")

# 4. 检查远程仓库
print("📋 步骤 4: 检查远程仓库...")
remote = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                       capture_output=True, text=True, check=False)
if remote.returncode == 0 and remote.stdout.strip():
    print(f"✅ 远程仓库: {remote.stdout.strip()}")
    print("")
    print("🚀 推送到 GitHub...")
    push = subprocess.run(['git', 'push', '-u', 'origin', 'main'], 
                         capture_output=True, text=True, check=False)
    if push.returncode == 0:
        print("✅ 推送成功！")
    else:
        print(f"⚠️  推送失败: {push.stderr[:200]}")
else:
    print("⚠️  远程仓库未配置")
    print("")
    print("📝 下一步：")
    print("1. 访问 https://github.com/new 创建仓库 bookforMX")
    print("2. 执行: git remote add origin https://github.com/YOUR_USERNAME/bookforMX.git")
    print("3. 执行: git push -u origin main")

print("")
print("✅ 本地部署准备完成！")


