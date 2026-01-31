---
name: hybrid-search
description: 多來源協作搜尋技能，整合 Google Search (Serper.dev) 和 Grok (Web + X/Twitter) 進行交叉驗證搜尋。觸發詞：搜尋, 查一下, 最新, 新聞, $BTC, $ETH
---

# Hybrid Search 多來源協作搜尋

整合 Google + Grok 進行智慧搜尋，提供交叉驗證的可靠結果。

## 使用方式

```bash
# Google 搜尋
python3 ~/.clawdbot/skills/hybrid-search/scripts/google_search.py "關鍵字"

# Grok Web 搜尋
python3 ~/.clawdbot/skills/hybrid-search/scripts/grok_search.py "關鍵字" --mode web

# Grok X/Twitter 搜尋
python3 ~/.clawdbot/skills/hybrid-search/scripts/grok_search.py "關鍵字" --mode x

# 完整混合搜尋（推薦）
python3 ~/.clawdbot/skills/hybrid-search/scripts/hybrid_search.py "關鍵字"
```

## 環境變數

需要設定 SERPER_API_KEY 和 XAI_API_KEY
