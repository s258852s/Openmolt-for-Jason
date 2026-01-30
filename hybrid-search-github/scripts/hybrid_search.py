#!/usr/bin/env python3
"""
Hybrid Search - 多來源混合搜尋
整合 Google (Serper) + Grok Web + Grok X/Twitter

Usage: python3 hybrid_search.py "搜尋關鍵字"
"""

import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# 加入當前目錄到 path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from google_search import google_search
from grok_search import grok_search

def hybrid_search(query: str, timeout: int = 60) -> dict:
    """
    Perform hybrid search across multiple sources
    
    Args:
        query: Search query string
        timeout: Timeout in seconds for each source
    
    Returns:
        dict with combined results from all sources
    """
    results = {
        "query": query,
        "timestamp": datetime.now().isoformat(),
        "sources": {},
        "errors": [],
        "summary": ""
    }
    
    # 定義搜尋任務
    search_tasks = {
        "google": lambda: google_search(query),
        "grok_web": lambda: grok_search(query, mode="web"),
        "grok_x": lambda: grok_search(query, mode="x")
    }
    
    # 並行執行搜尋
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(task): name 
            for name, task in search_tasks.items()
        }
        
        for future in as_completed(futures, timeout=timeout):
            name = futures[future]
            try:
                result = future.result(timeout=timeout)
                if "error" in result:
                    results["errors"].append({
                        "source": name,
                        "error": result["error"]
                    })
                else:
                    results["sources"][name] = result
            except Exception as e:
                results["errors"].append({
                    "source": name,
                    "error": str(e)
                })
    
    # 生成整合摘要
    results["summary"] = generate_summary(results)
    
    return results

def generate_summary(results: dict) -> str:
    """Generate integrated summary from all sources"""
    
    parts = []
    sources_found = list(results["sources"].keys())
    
    parts.append(f"🔍 混合搜尋結果：{results['query']}")
    parts.append(f"📊 成功來源：{', '.join(sources_found)} ({len(sources_found)}/3)")
    parts.append("")
    
    # Google 結果
    if "google" in results["sources"]:
        g = results["sources"]["google"]
        parts.append("═══ 🌐 Google 搜尋 ═══")
        
        if g.get("answer_box"):
            parts.append(f"📦 精選答案：{g['answer_box'].get('answer', '')[:200]}")
        
        if g.get("organic"):
            parts.append("🔗 前 3 筆結果：")
            for item in g["organic"][:3]:
                parts.append(f"  • {item['title']}")
                if item.get("snippet"):
                    parts.append(f"    {item['snippet'][:80]}...")
        parts.append("")
    
    # Grok Web 結果
    if "grok_web" in results["sources"]:
        gw = results["sources"]["grok_web"]
        parts.append("═══ 🔍 Grok Web 分析 ═══")
        content = gw.get("content", "")
        if content:
            # 截取前 500 字
            parts.append(content[:500] + ("..." if len(content) > 500 else ""))
        parts.append("")
    
    # Grok X 結果
    if "grok_x" in results["sources"]:
        gx = results["sources"]["grok_x"]
        parts.append("═══ 🐦 Grok X/Twitter ═══")
        content = gx.get("content", "")
        if content:
            parts.append(content[:500] + ("..." if len(content) > 500 else ""))
        parts.append("")
    
    # 錯誤報告
    if results["errors"]:
        parts.append("⚠️ 部分來源失敗：")
        for err in results["errors"]:
            parts.append(f"  • {err['source']}: {err['error'][:50]}")
    
    return "\n".join(parts)

def main():
    parser = argparse.ArgumentParser(description="Hybrid Search - 多來源混合搜尋")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--timeout", type=int, default=60, help="Timeout per source (seconds)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    
    args = parser.parse_args()
    
    print(f"\n🔍 正在搜尋：{args.query}")
    print("⏳ 同時查詢 Google + Grok Web + Grok X...\n")
    
    result = hybrid_search(args.query, args.timeout)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["summary"])
        print(f"\n⏱️ 完成時間：{result['timestamp']}")

if __name__ == "__main__":
    main()
