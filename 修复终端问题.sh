#!/bin/bash
# 修复 Cursor 终端环境问题
# 使用 bash 而不是 zsh，避免 cursor_snap_ENV_VARS 问题

export SHELL=/bin/bash
unset cursor_snap_ENV_VARS 2>/dev/null

cd "/Users/a58/cursor/归档/OK 调研/bookforMX"
/usr/bin/python3 执行部署_最终版.py


