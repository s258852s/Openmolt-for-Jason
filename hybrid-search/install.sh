#!/bin/bash
# Hybrid Search Skill 安裝腳本
# 用法: bash install.sh

SKILL_DIR="$HOME/.clawdbot/skills/hybrid-search"

echo "🔍 安裝 Hybrid Search Skill..."
echo ""

# 備份舊的（如果存在）
if [ -d "$SKILL_DIR" ]; then
    echo "📦 備份舊版本..."
    mv "$SKILL_DIR" "${SKILL_DIR}.backup.$(date +%Y%m%d%H%M%S)"
fi

# 創建目錄
mkdir -p "$SKILL_DIR/scripts"

# 複製檔案
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cp "$SCRIPT_DIR/SKILL.md" "$SKILL_DIR/"
cp "$SCRIPT_DIR/scripts/"*.py "$SKILL_DIR/scripts/"

# 設定可執行
chmod +x "$SKILL_DIR/scripts/"*.py

echo "✅ Skill 已安裝到: $SKILL_DIR"
echo ""

# 檢查 API Keys
echo "🔑 檢查 API Keys..."

if [ -z "$SERPER_API_KEY" ]; then
    echo "⚠️  SERPER_API_KEY 未設定"
else
    echo "✅ SERPER_API_KEY 已設定"
fi

if [ -z "$XAI_API_KEY" ]; then
    echo "⚠️  XAI_API_KEY 未設定"
else
    echo "✅ XAI_API_KEY 已設定"
fi

echo ""
echo "📝 如需設定 API Keys，請執行："
echo '   echo '\''export SERPER_API_KEY="your_key"'\'' >> ~/.bashrc'
echo '   echo '\''export XAI_API_KEY="your_key"'\'' >> ~/.bashrc'
echo '   source ~/.bashrc'
echo ""
echo "🎉 安裝完成！重啟 clawdbot gateway 後即可使用"
echo "   clawdbot gateway restart"
