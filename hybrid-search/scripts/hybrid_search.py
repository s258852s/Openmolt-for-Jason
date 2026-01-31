#!/usr/bin/env python3
"""
Hybrid Search - 多來源協作搜尋
整合 Google (Serper.dev) + Grok (Web + X) 進行交叉驗證

Usage: python3 hybrid_search.py "search query" [options]
"""

import argparse
import json
import os
import sys
import concurrent.futures
from datetime import datetime

# Import local search modules
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from google_search import google_search
from grok_search import grok_search

def hybrid_search(query: str, sources: list = None, timeout: int = 60) -> dict:
    """
    Perform hybrid search across multiple sources
    
    Args:
        query: Search query string
        sources: List of sources to use ["google", "grok_web", "grok_x"]
                 Default: all sources
        timeout: Timeout in seconds for each source
    
    Returns:
        dict with combined search results
    """
    if sources is None:
        sources = ["google", "grok_web", "grok_x"]
    
    results = {
        "query": query,
        "timestamp": datetime.now().isoformat(),
        "sources_requested": sources,
        "sources_succeeded": [],
        "sources_failed": [],
        "google": None,
        "grok_web": None,
        "grok_x": None,
        "summary": ""
    }
    
    # Define search tasks
    tasks = {}
    if "google" in sources:
        tasks["google"] = lambda: google_search(query)
    if "grok_web" in sources:
        tasks["grok_web"] = lambda: grok_search(query, mode="web")
    if "grok_x" in sources:
        tasks["grok_x"] = lambda: grok_search(query, mode="x")
    
    # Execute searches concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_source = {
            executor.submit(task): source 
            for source, task in tasks.items()
        }
        
        for future in concurrent.futures.as_completed(future_to_source, timeout=timeout):
            source = future_to_source[future]
            try:
                result = future.result()
                if "error" not in result:
                    results[source] = result
                    results["sources_succeeded"].append(source)
                else:
                    results["sources_failed"].append({
                        "source": source,
                        "error": result["error"]
                    })
            except Exception as e:
                results["sources_failed"].append({
                    "source": source,
                    "error": str(e)
                })
    
    # Generate summary
    results["summary"] = generate_summary(results)
    
    return results

def generate_summary(results: dict) -> str:
    """Generate a combined summary from all sources"""
    
    summary_parts = []
    
    # Google results summary
    if results.get("google") and results["google"].get("results"):
        google_res = results["google"]
        summary_parts.append("【Google 搜尋】")
        
        if google_res.get("answer_box"):
            summary_parts.append(f"精選答案：{google_res['answer_box'].get('answer', '')}")
        
        top_results = google_res["results"][:3]
        for r in top_results:
            summary_parts.append(f"• {r['title']}")
            if r.get('snippet'):
                summary_parts.append(f"  {r['snippet'][:100]}...")
    
    # Grok Web summary
    if results.get("grok_web") and results["grok_web"].get("content"):
        summary_parts.append("\n【Grok Web 分析】")
        content = results["grok_web"]["content"]
        # Take first 500 chars of Grok response
        summary_parts.append(content[:500] + "..." if len(content) > 500 else content)
    
    # Grok X summary
    if results.get("grok_x") and results["grok_x"].get("content"):
        summary_parts.append("\n【X/Twitter 即時】")
        content = results["grok_x"]["content"]
        summary_parts.append(content[:500] + "..." if len(content) > 500 else content)
    
    if not summary_parts:
        return "無法取得任何搜尋結果"
    
    return "\n".join(summary_parts)

def print_results(results: dict):
    """Pretty print search results"""
    
    print(f"\n{'='*60}")
    print(f"🔍 混合搜尋結果：{results['query']}")
    print(f"⏰ 時間：{results['timestamp']}")
    print(f"✅ 成功來源：{', '.join(results['sources_succeeded']) or '無'}")
    if results['sources_failed']:
        failed = [f"{f['source']}" for f in results['sources_failed']]
        print(f"❌ 失敗來源：{', '.join(failed)}")
    print(f"{'='*60}\n")
    
    # Print summary
    print("📋 綜合摘要：")
    print("-" * 40)
    print(results['summary'])
    print()
    
    # Print detailed Google results
    if results.get("google"):
        google = results["google"]
        print("\n🌐 Google 詳細結果：")
        print("-" * 40)
        for i, r in enumerate(google.get("results", [])[:5], 1):
            print(f"{i}. {r['title']}")
            print(f"   🔗 {r['url']}")
            if r.get('date'):
                print(f"   📅 {r['date']}")
            print()
    
    # Print Grok citations if available
    if results.get("grok_web") and results["grok_web"].get("citations"):
        print("\n📚 Grok Web 引用來源：")
        print("-" * 40)
        for cite in results["grok_web"]["citations"][:5]:
            if isinstance(cite, dict):
                print(f"• {cite.get('title', '')} - {cite.get('url', '')}")
            else:
                print(f"• {cite}")
    
    # Print errors if any
    if results['sources_failed']:
        print("\n⚠️ 錯誤訊息：")
        print("-" * 40)
        for fail in results['sources_failed']:
            print(f"• {fail['source']}: {fail['error']}")

def main():
    parser = argparse.ArgumentParser(
        description="Hybrid Search - 多來源協作搜尋",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例：
  python3 hybrid_search.py "台灣今日新聞"
  python3 hybrid_search.py "BTC 價格" --sources google grok_web
  python3 hybrid_search.py "川普" --sources grok_x --json
        """
    )
    parser.add_argument("query", help="搜尋關鍵字")
    parser.add_argument("--sources", nargs="+", 
                        choices=["google", "grok_web", "grok_x"],
                        default=["google", "grok_web", "grok_x"],
                        help="選擇搜尋來源 (預設: 全部)")
    parser.add_argument("--timeout", type=int, default=60,
                        help="每個來源的超時秒數 (預設: 60)")
    parser.add_argument("--json", action="store_true", 
                        help="輸出 JSON 格式")
    
    args = parser.parse_args()
    
    # Check for API keys
    missing_keys = []
    if "google" in args.sources and not os.environ.get("SERPER_API_KEY"):
        missing_keys.append("SERPER_API_KEY")
    if ("grok_web" in args.sources or "grok_x" in args.sources) and not os.environ.get("XAI_API_KEY"):
        missing_keys.append("XAI_API_KEY")
    
    if missing_keys:
        print(f"⚠️ 缺少 API Key: {', '.join(missing_keys)}")
        print("請設定環境變數或加入 ~/.clawdbot/clawdbot.json")
        print("\n範例：")
        print('  export SERPER_API_KEY="your_key"')
        print('  export XAI_API_KEY="your_key"')
        sys.exit(1)
    
    # Perform search
    results = hybrid_search(args.query, args.sources, args.timeout)
    
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print_results(results)

if __name__ == "__main__":
    main()
