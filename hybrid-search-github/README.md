# 🔍 Hybrid Search Skill for Moltbot

多來源混合搜尋技能，整合 Google + Grok Web + Grok X/Twitter。

## 功能特色

- ✅ **Google Search** (Serper.dev API) - 綜合網路搜尋
- ✅ **Grok Web Search** (xAI Agent Tools API) - AI 深度分析
- ✅ **Grok X Search** (xAI Agent Tools API) - Twitter/X 即時討論
- ✅ **交叉驗證** - 自動比對多來源結果
- ✅ **繁體中文** - 台灣用戶優化

## 安裝

### 方法 1：Git Clone（推薦）

```bash
cd ~/.clawdbot/skills
git clone https://github.com/你的帳號/hybrid-search.git
clawdbot gateway restart
```

### 方法 2：手動安裝

```bash
# 下載並解壓
# 複製整個 hybrid-search 目錄到 ~/.clawdbot/skills/
```

## 設定 API Keys

在 `~/.bashrc` 加入：

```bash
export SERPER_API_KEY="你的_serper_key"
export XAI_API_KEY="你的_xai_key"
```

然後執行：

```bash
source ~/.bashrc
clawdbot gateway restart
```

### 取得 API Keys

| 服務 | 網址 | 免費額度 |
|------|------|----------|
| Serper.dev | https://serper.dev | 2,500 次/月 |
| xAI | https://console.x.ai | Agent Tools 免費 |

## 使用方式

直接跟 Moltbot 說：

- "搜尋一下 BTC 最新價格"
- "查一下黃金暴跌原因"
- "最新的川普新聞"
- "/search AI 發展趨勢"

## 檔案結構

```
hybrid-search/
├── SKILL.md          # Moltbot skill 定義
├── README.md         # 本文件
├── install.sh        # 自動安裝腳本
├── .env.example      # 環境變數範例
└── scripts/
    ├── google_search.py   # Google/Serper 搜尋
    ├── grok_search.py     # Grok Web/X 搜尋 (Agent Tools API)
    └── hybrid_search.py   # 混合搜尋整合器
```

## 手動測試

```bash
# 測試 Google
python3 ~/.clawdbot/skills/hybrid-search/scripts/google_search.py "test"

# 測試 Grok Web
python3 ~/.clawdbot/skills/hybrid-search/scripts/grok_search.py "test" --mode web

# 測試 Grok X
python3 ~/.clawdbot/skills/hybrid-search/scripts/grok_search.py "test" --mode x

# 測試混合搜尋
python3 ~/.clawdbot/skills/hybrid-search/scripts/hybrid_search.py "test"
```

## 授權

MIT License

## 作者

Jason (yurou)
