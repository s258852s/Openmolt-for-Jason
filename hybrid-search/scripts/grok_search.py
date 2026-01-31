#!/usr/bin/env python3
"""
Grok Search via xAI API (Web + X/Twitter)
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
    Perform search via xAI Grok API using Responses endpoint with tools
    
    Args:
        query: Search query string
        mode: "web" for web search, "x" for X/Twitter search, "both" for both
    
    Returns:
        dict with search results
    """
    api_key = os.environ.get("XAI_API_KEY")
    
    if not api_key:
        return {"error": "XAI_API_KEY not set. Export it or add to clawdbot.json"}
    
    # Use Responses API endpoint
    url = "https://api.x.ai/v1/responses"
    
    # Build tools based on mode
    tools = []
    if mode in ["web", "both"]:
        tools.append({"type": "web_search"})
    if mode in ["x", "both"]:
        tools.append({"type": "x_search"})
    
    # Build prompt based on mode
    if mode == "x":
        user_prompt = f"搜尋 X/Twitter 上關於「{query}」的最新討論和推文，整理重點並用繁體中文回答"
    elif mode == "both":
        user_prompt = f"同時搜尋網路和 X/Twitter 上關於「{query}」的最新資訊，整理重點並用繁體中文回答"
    else:  # web
        user_prompt = f"搜尋網路上關於「{query}」的最新資訊，整理重點並用繁體中文回答"
    
    payload = json.dumps({
        "model": "grok-4-1-fast-reasoning",
        "tools": tools,
        "input": user_prompt
    }).encode('utf-8')
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
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
    
    mode_name = "X/Twitter" if mode == "x" else ("Web + X" if mode == "both" else "Web")
    
    formatted = {
        "source": f"Grok {mode_name}",
        "query": query,
        "mode": mode,
        "content": "",
        "citations": []
    }
    
    # Extract content from Responses API format
    if "output" in raw:
        for item in raw["output"]:
            if item.get("type") == "message":
                for content in item.get("content", []):
                    if content.get("type") == "output_text":
                        formatted["content"] += content.get("text", "")
    
    # Fallback: check for direct text field
    if not formatted["content"] and "text" in raw:
        formatted["content"] = raw["text"]
    
    # Extract citations if available
    if "citations" in raw:
        formatted["citations"] = raw["citations"]
    
    return formatted

def main():
    parser = argparse.ArgumentParser(description="Grok Search via xAI API")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--mode", choices=["web", "x", "both"], default="web", 
                        help="Search mode: 'web' for web search, 'x' for X/Twitter, 'both' for both (default: web)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    
    args = parser.parse_args()
    
    result = grok_search(args.query, args.mode)
    
    if args.json or "error" in result:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # Pretty print
        mode_emoji = "🐦" if args.mode == "x" else ("🌐🐦" if args.mode == "both" else "🤖")
        
        print(f"\n{mode_emoji} Grok {result['source'].split(' ', 1)[-1]} 搜尋：{result['query']}\n")
        print("=" * 50)
        print(f"\n{result['content']}\n")
        
        if result.get("citations"):
            print("\n📚 引用來源：")
            for i, cite in enumerate(result["citations"], 1):
                if isinstance(cite, dict):
                    print(f"  {i}. {cite.get('title', '')} - {cite.get('url', '')}")
                else:
                    print(f"  {i}. {cite}")

if __name__ == "__main__":
    main()
