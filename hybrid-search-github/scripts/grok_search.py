#!/usr/bin/env python3
"""
Grok Search via xAI Agent Tools API (Web + X/Twitter)
使用新的 Responses API 進行即時搜尋

Usage: 
  python3 grok_search.py "query" --mode web
  python3 grok_search.py "query" --mode x
  python3 grok_search.py "query" --mode both
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

def grok_search(query: str, mode: str = "web") -> dict:
    """
    Perform search via xAI Agent Tools API
    
    Args:
        query: Search query string
        mode: "web" for web search, "x" for X/Twitter search, "both" for both
    
    Returns:
        dict with search results
    """
    api_key = os.environ.get("XAI_API_KEY")
    
    if not api_key:
        return {"error": "XAI_API_KEY not set. Export it in ~/.bashrc"}
    
    # 使用 Responses API endpoint
    url = "https://api.x.ai/v1/responses"
    
    # 根據 mode 設定 tools
    tools = []
    if mode in ["web", "both"]:
        tools.append({"type": "web_search"})
    if mode in ["x", "both"]:
        tools.append({"type": "x_search"})
    
    # 構建搜尋 prompt
    if mode == "x":
        user_prompt = f"搜尋 X/Twitter 上關於「{query}」的最新討論、推文和趨勢。請用繁體中文回答，包含推文來源。"
    elif mode == "both":
        user_prompt = f"同時搜尋網路和 X/Twitter 上關於「{query}」的最新資訊。請用繁體中文回答，標註資訊來源。"
    else:
        user_prompt = f"搜尋關於「{query}」的最新網路資訊。請用繁體中文回答，標註資訊來源。"
    
    payload = json.dumps({
        "model": "grok-4-1-fast-reasoning",
        "input": user_prompt,
        "tools": tools,
        "temperature": 0.7
    }).encode('utf-8')
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            return format_grok_results(result, mode, query)
    except urllib.error.HTTPError as e:
        error_body = ""
        try:
            error_body = e.read().decode('utf-8')
        except:
            pass
        return {"error": f"HTTP Error {e.code}: {e.reason}", "details": error_body}
    except urllib.error.URLError as e:
        return {"error": f"URL Error: {e.reason}"}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}

def format_grok_results(raw: dict, mode: str, query: str) -> dict:
    """Format raw API response into clean structure"""
    
    mode_names = {"web": "Web", "x": "X/Twitter", "both": "Web + X"}
    
    formatted = {
        "source": f"Grok {mode_names.get(mode, 'Search')}",
        "query": query,
        "mode": mode,
        "content": "",
        "citations": [],
        "tool_calls": []
    }
    
    # 從 Responses API 格式提取內容
    # 新版 API 使用 output_text
    if "output_text" in raw:
        formatted["content"] = raw["output_text"]
    elif "output" in raw:
        for item in raw["output"]:
            if item.get("type") == "message":
                content = item.get("content", [])
                for c in content:
                    if c.get("type") == "text":
                        formatted["content"] += c.get("text", "")
            elif item.get("type") == "tool_call":
                formatted["tool_calls"].append({
                    "name": item.get("name", ""),
                    "arguments": item.get("arguments", {})
                })
    
    # 備用：舊格式相容
    if not formatted["content"] and "choices" in raw:
        if len(raw["choices"]) > 0:
            message = raw["choices"][0].get("message", {})
            formatted["content"] = message.get("content", "")
    
    # 提取 citations
    if "citations" in raw:
        formatted["citations"] = raw["citations"]
    
    return formatted

def main():
    parser = argparse.ArgumentParser(description="Grok Search via xAI Agent Tools API")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--mode", choices=["web", "x", "both"], default="web", 
                        help="Search mode: 'web', 'x' (Twitter), or 'both' (default: web)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    
    args = parser.parse_args()
    
    result = grok_search(args.query, args.mode)
    
    if args.json or "error" in result:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # Pretty print
        mode_emoji = {"web": "🌐", "x": "🐦", "both": "🔍"}
        
        print(f"\n{mode_emoji.get(args.mode, '🔍')} Grok {result['source']} 搜尋：{result['query']}\n")
        print("=" * 50)
        
        if result.get("tool_calls"):
            print("\n📡 工具呼叫：")
            for tc in result["tool_calls"]:
                print(f"  • {tc['name']}")
        
        print(f"\n{result['content']}\n")
        
        if result.get("citations"):
            print("\n📚 引用來源：")
            for i, cite in enumerate(result["citations"][:10], 1):
                if isinstance(cite, dict):
                    print(f"  {i}. {cite.get('title', '')} - {cite.get('url', '')}")
                elif isinstance(cite, str):
                    print(f"  {i}. {cite}")

if __name__ == "__main__":
    main()
