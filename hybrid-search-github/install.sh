#!/bin/bash
# Hybrid Search Skill 安裝腳本

set -e

echo "🔍 安裝 Hybrid Search Skill..."

# 檢查 Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ 需要 Python3，請先安裝"
    exit 1
fi

# 確定目標目錄
SKILL_DIR="${HOME}/.clawdbot/skills/hybrid-search"

# 如果已存在，備份
if [ -d "$SKILL_DIR" ]; then
    echo "📦 備份舊版本..."
    mv "$SKILL_DIR" "${SKILL_DIR}.backup.$(date +%Y%m%d%H%M%S)"
fi

# 取得腳本所在目錄
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 複製到目標
echo "📁 複製檔案..."
mkdir -p "$SKILL_DIR/scripts"
cp "$SCRIPT_DIR/SKILL.md" "$SKILL_DIR/"
cp "$SCRIPT_DIR/scripts/"*.py "$SKILL_DIR/scripts/"
chmod +x "$SKILL_DIR/scripts/"*.py

# 檢查環境變數
echo ""
echo "🔑 檢查 API Keys..."

if [ -z "$SERPER_API_KEY" ]; then
    echo "⚠️  SERPER_API_KEY 未設定"
    echo "   請在 ~/.bashrc 加入: export SERPER_API_KEY=\"你的key\""
else
    echo "✅ SERPER_API_KEY 已設定"
fi

if [ -z "$XAI_API_KEY" ]; then
    echo "⚠️  XAI_API_KEY 未設定"
    echo "   請在 ~/.bashrc 加入: export XAI_API_KEY=\"你的key\""
else
    echo "✅ XAI_API_KEY 已設定"
fi

echo ""
echo "✅ 安裝完成！"
echo ""
echo "📍 安裝位置: $SKILL_DIR"
echo ""
echo "🔄 請執行以下指令重啟 Gateway："
echo "   clawdbot gateway restart"
echo ""
