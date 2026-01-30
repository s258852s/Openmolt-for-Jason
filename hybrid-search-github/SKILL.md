---
name: hybrid-search
description: 多來源混合搜尋 - 整合 Google (Serper.dev) + Grok Web + Grok X/Twitter，交叉驗證資訊
metadata: {"moltbot":{"emoji":"🔍","requires":{"bins":["python3"],"env":["SERPER_API_KEY","XAI_API_KEY"]},"primaryEnv":"SERPER_API_KEY"}}
---

# Hybrid Search Skill

多來源混合搜尋技能，整合三個搜尋來源並交叉驗證結果。

## 功能

| 來源 | API | 用途 |
|------|-----|------|
| Google | Serper.dev | 綜合網路搜尋、新聞 |
| Grok Web | xAI Agent Tools API | 深度分析、即時資訊 |
| Grok X | xAI Agent Tools API | Twitter/X 社群討論 |

## 使用時機

當用戶使用以下關鍵字時觸發：
- `/search`, `/研究`, `搜尋`, `查一下`
- `最新`, `新聞`, `現在`, `目前`
- `$BTC`, `$ETH`, `黃金`, `股票`
- `川普`, `政治`, `選舉`

## 執行方式

### 混合搜尋（推薦）
```bash
python3 ~/.clawdbot/skills/hybrid-search/scripts/hybrid_search.py "搜尋關鍵字"
```

### 單獨 Google 搜尋
```bash
python3 ~/.clawdbot/skills/hybrid-search/scripts/google_search.py "搜尋關鍵字"
```

### 單獨 Grok 搜尋
```bash
# Web 搜尋
python3 ~/.clawdbot/skills/hybrid-search/scripts/grok_search.py "關鍵字" --mode web

# X/Twitter 搜尋
python3 ~/.clawdbot/skills/hybrid-search/scripts/grok_search.py "關鍵字" --mode x

# 兩者都搜
python3 ~/.clawdbot/skills/hybrid-search/scripts/grok_search.py "關鍵字" --mode both
```

## 搜尋策略建議

| 查詢類型 | 推薦來源 | 範例 |
|----------|----------|------|
| 一般新聞 | Google + Grok Web | "台灣今日新聞" |
| 即時事件 | Grok X 優先 | "地震 現在" |
| 金融資訊 | 全部 + 交叉驗證 | "$BTC 價格" |
| 技術問題 | Google 優先 | "Python error fix" |
| 社群輿論 | Grok X | "川普 推特反應" |

## 輸出格式

整合報告包含：
- 📊 綜合摘要（整合所有來源）
- 🌐 Google 結果
- 🔍 Grok Web 分析
- 🐦 Grok X 社群聲音
- ⚠️ 來源衝突警告（如果有）

## 環境變數

需要在 `~/.bashrc` 設定：
```bash
export SERPER_API_KEY="你的_serper_key"
export XAI_API_KEY="你的_xai_key"
```

## API 申請

- Serper.dev: https://serper.dev (免費 2500 次/月)
- xAI: https://console.x.ai (Agent Tools API 免費)
