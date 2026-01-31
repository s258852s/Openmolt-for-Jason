#!/usr/bin/env python3
"""
Google Search via Serper.dev API
Usage: python3 google_search.py "search query" [--num 10]
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

def google_search(query: str, num_results: int = 10) -> dict:
    """
    Perform Google search via Serper.dev API
    
    Args:
        query: Search query string
        num_results: Number of results to return (default 10)
    
    Returns:
        dict with search results
    """
    api_key = os.environ.get("SERPER_API_KEY")
    
    if not api_key:
        return {"error": "SERPER_API_KEY not set. Export it or add to clawdbot.json"}
    
    url = "https://google.serper.dev/search"
    
    payload = json.dumps({
        "q": query,
        "num": num_results,
        "gl": "tw",  # Taiwan
        "hl": "zh-TW"  # Traditional Chinese
    }).encode('utf-8')
    
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return format_results(result)
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP Error {e.code}: {e.reason}"}
    except urllib.error.URLError as e:
        return {"error": f"URL Error: {e.reason}"}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}

def format_results(raw: dict) -> dict:
    """Format raw API response into clean structure"""
    
    formatted = {
        "source": "Google (Serper.dev)",
        "query": raw.get("searchParameters", {}).get("q", ""),
        "results": [],
        "knowledge_graph": None,
        "answer_box": None
    }
    
    # Extract organic results
    for item in raw.get("organic", []):
        formatted["results"].append({
            "title": item.get("title", ""),
            "url": item.get("link", ""),
            "snippet": item.get("snippet", ""),
            "date": item.get("date", "")
        })
    
    # Extract knowledge graph if present
    if "knowledgeGraph" in raw:
        kg = raw["knowledgeGraph"]
        formatted["knowledge_graph"] = {
            "title": kg.get("title", ""),
            "type": kg.get("type", ""),
            "description": kg.get("description", "")
        }
    
    # Extract answer box if present
    if "answerBox" in raw:
        ab = raw["answerBox"]
        formatted["answer_box"] = {
            "title": ab.get("title", ""),
            "answer": ab.get("answer", "") or ab.get("snippet", "")
        }
    
    return formatted

def main():
    parser = argparse.ArgumentParser(description="Google Search via Serper.dev")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--num", type=int, default=10, help="Number of results (default: 10)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    
    args = parser.parse_args()
    
    result = google_search(args.query, args.num)
    
    if args.json or "error" in result:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # Pretty print
        print(f"\n🔍 Google 搜尋：{result['query']}\n")
        print("=" * 50)
        
        if result.get("answer_box"):
            ab = result["answer_box"]
            print(f"\n📦 精選摘要：")
            print(f"   {ab.get('answer', '')}\n")
        
        if result.get("knowledge_graph"):
            kg = result["knowledge_graph"]
            print(f"\n📚 知識圖譜：{kg.get('title', '')}")
            print(f"   {kg.get('description', '')}\n")
        
        print(f"\n📰 搜尋結果：\n")
        for i, r in enumerate(result["results"], 1):
            print(f"{i}. {r['title']}")
            print(f"   🔗 {r['url']}")
            if r.get('snippet'):
                print(f"   {r['snippet'][:150]}...")
            if r.get('date'):
                print(f"   📅 {r['date']}")
            print()

if __name__ == "__main__":
    main()
