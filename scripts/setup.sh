#!/usr/bin/env bash
# setup.sh - 首次使用依赖检测与安装
# Usage: bash scripts/setup.sh

set -e

echo "🔍 检测依赖..."

MISSING=0

if ! python3 -c "import httpx" 2>/dev/null; then
  echo "📦 安装 httpx..."
  pip install -q httpx
  MISSING=1
fi

if ! python3 -c "import markdownify" 2>/dev/null; then
  echo "📦 安装 markdownify..."
  pip install -q markdownify
  MISSING=1
fi

if [ "$MISSING" -eq 0 ]; then
  echo "✅ 所有依赖已就绪"
else
  echo "✅ 依赖安装完成"
fi

# 最终验证
python3 -c "import httpx; print('验证通过: httpx')"
python3 -c "import markdownify; print('验证通过: markdownify')"
echo "🎉 setup 完成，可以正常使用"
