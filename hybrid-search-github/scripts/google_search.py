#!/usr/bin/env python3
"""
Google Search via Serper.dev API
多語言搜尋，台灣地區優化

Usage: python3 google_search.py "搜尋關鍵字"
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
        return {"error": "SERPER_API_KEY not set. Export it in ~/.bashrc"}
    
    url = "https://google.serper.dev/search"
    
    payload = json.dumps({
        "q": query,
        "gl": "tw",
        "hl": "zh-TW",
        "num": num_results
    }).encode('utf-8')
    
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return format_google_results(result, query)
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP Error {e.code}: {e.reason}"}
    except urllib.error.URLError as e:
        return {"error": f"URL Error: {e.reason}"}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}

def format_google_results(raw: dict, query: str) -> dict:
    """Format raw Serper API response into clean structure"""
    formatted = {
        "source": "Google (Serper)",
        "query": query,
        "organic": [],
        "answer_box": None,
        "knowledge_graph": None
    }
    
    # Extract organic results
    if "organic" in raw:
        for item in raw["organic"][:10]:
            formatted["organic"].append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", ""),
                "position": item.get("position", 0)
            })
    
    # Extract answer box if present
    if "answerBox" in raw:
        ab = raw["answerBox"]
        formatted["answer_box"] = {
            "title": ab.get("title", ""),
            "answer": ab.get("answer", ab.get("snippet", "")),
            "source": ab.get("link", "")
        }
    
    # Extract knowledge graph if present
    if "knowledgeGraph" in raw:
        kg = raw["knowledgeGraph"]
        formatted["knowledge_graph"] = {
            "title": kg.get("title", ""),
            "type": kg.get("type", ""),
            "description": kg.get("description", ""),
            "source": kg.get("website", "")
        }
    
    return formatted

def main():
    parser = argparse.ArgumentParser(description="Google Search via Serper.dev")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--num", type=int, default=10, help="Number of results")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    
    args = parser.parse_args()
    
    result = google_search(args.query, args.num)
    
    if args.json or "error" in result:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # Pretty print
        print(f"\n🌐 Google 搜尋：{result['query']}\n")
        print("=" * 50)
        
        if result.get("answer_box"):
            ab = result["answer_box"]
            print(f"\n📦 精選摘要：")
            print(f"   {ab['answer'][:200]}...")
            if ab.get("source"):
                print(f"   來源: {ab['source']}")
        
        if result.get("knowledge_graph"):
            kg = result["knowledge_graph"]
            print(f"\n📚 知識圖譜：{kg['title']}")
            if kg.get("description"):
                print(f"   {kg['description'][:150]}...")
        
        print(f"\n🔗 搜尋結果：")
        for item in result["organic"][:5]:
            print(f"\n{item['position']}. {item['title']}")
            print(f"   {item['link']}")
            if item.get("snippet"):
                print(f"   {item['snippet'][:100]}...")

if __name__ == "__main__":
    main()
