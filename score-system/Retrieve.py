"""
Retrieve.py - 使用 Apify 抓取百度首页信息

功能：
1. 通过 Apify 的 Web Scraper 抓取百度首页内容
2. 提取页面标题、描述、热门搜索、导航链接等信息
3. 支持多种输出格式（JSON / 文本）
4. 支持自定义 Apify API Token 和 Actor

使用方法：
    python Retrieve.py
    python Retrieve.py --output json
    python Retrieve.py --actor apify/web-scraper
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import Optional, Dict, Any

try:
    from apify_client import ApifyClient
except ImportError:
    print("正在安装 apify-client...")
    os.system(f"{sys.executable} -m pip install apify-client -q")
    from apify_client import ApifyClient


# ============================================================
# 配置区 - 请在此填写你的 Apify API Token
# ============================================================
APIFY_API_TOKEN = os.environ.get("APIFY_API_TOKEN", "")

# 默认使用的 Apify Actor
DEFAULT_ACTOR = "apify/web-scraper"

# 要抓取的目标 URL
TARGET_URL = "https://www.baidu.com"


class BaiduScraper:
    """百度首页抓取器"""

    def __init__(self, api_token: str = APIFY_API_TOKEN):
        if not api_token:
            raise ValueError(
                "❌ 未设置 Apify API Token！\n"
                "请通过以下方式之一设置：\n"
                "  1. 设置环境变量: set APIFY_API_TOKEN=your_token_here\n"
                "  2. 修改本文件中的 APIFY_API_TOKEN 变量"
            )
        self.client = ApifyClient(api_token)

    def scrape(self, actor_name: str = DEFAULT_ACTOR) -> Dict[str, Any]:
        """
        使用指定的 Actor 抓取百度首页

        Args:
            actor_name: Apify Actor 名称

        Returns:
            包含抓取结果的字典
        """
        print(f"🚀 正在使用 Actor [{actor_name}] 抓取 {TARGET_URL} ...")

        # 准备运行输入
        run_input = {
            "startUrls": [{"url": TARGET_URL}],
            "pageFunction": """
                async function pageFunction(context) {
                    const { $, request, log } = context;
                    const pageTitle = $('title').text().trim();
                    const metaDescription = $('meta[name="description"]').attr('content') || '';

                    // 提取导航链接
                    const navLinks = [];
                    $('#s-top-left a').each((i, el) => {
                        navLinks.push({
                            text: $(el).text().trim(),
                            href: $(el).attr('href')
                        });
                    });

                    // 提取热门搜索词（百度首页的热搜区域）
                    const hotSearches = [];
                    $('.hot-title, .title-content, .s-hot-search-content').each((i, el) => {
                        const text = $(el).text().trim();
                        if (text) hotSearches.push(text);
                    });

                    // 提取所有可见链接
                    const allLinks = [];
                    $('a[href]').each((i, el) => {
                        const href = $(el).attr('href');
                        const text = $(el).text().trim();
                        if (text && href && !href.startsWith('javascript')) {
                            allLinks.push({ text, href });
                        }
                    });

                    // 提取页面正文文本片段
                    const bodyText = $('body').text()
                        .replace(/\\s+/g, ' ')
                        .substring(0, 2000);

                    return {
                        url: request.url,
                        title: pageTitle,
                        metaDescription: metaDescription,
                        navLinks: navLinks.slice(0, 20),
                        hotSearches: hotSearches.slice(0, 30),
                        allLinksCount: allLinks.length,
                        allLinks: allLinks.slice(0, 50),
                        bodyPreview: bodyText,
                        scrapedAt: new Date().toISOString()
                    };
                }
            """,
            "proxyConfiguration": {
                "useApifyProxy": True
            },
            "maxCrawlingDepth": 1,
            "maxPagesPerCrawl": 1,
        }

        # 运行 Actor 并等待结果
        try:
            run = self.client.actor(actor_name).call(run_input=run_input)
            print(f"✅ Actor 运行完成！Run ID: {run['id']}")
        except Exception as e:
            print(f"❌ Actor 运行失败: {e}")
            print("💡 提示：请检查 API Token 是否正确，或网络是否可访问 Apify")
            sys.exit(1)

        # 获取结果
        results = []
        try:
            dataset = self.client.dataset(run["defaultDatasetId"]).list_items().items
            results = list(dataset)
            print(f"📦 获取到 {len(results)} 条结果")
        except Exception as e:
            print(f"⚠️  获取结果时出错: {e}")

        return {
            "success": len(results) > 0,
            "targetUrl": TARGET_URL,
            "actorUsed": actor_name,
            "runId": run["id"],
            "results": results,
            "resultCount": len(results),
            "scrapedAt": datetime.now().isoformat(),
        }

    def scrape_simple(self) -> Dict[str, Any]:
        """
        简化版抓取 - 使用 Apify 的 Website Content Crawler
        更适合提取文本内容
        """
        actor_name = "apify/website-content-crawler"
        print(f"🚀 正在使用 Actor [{actor_name}] 抓取 {TARGET_URL} ...")

        run_input = {
            "startUrls": [{"url": TARGET_URL}],
            "maxCrawlPages": 1,
            "maxCrawlDepth": 1,
            "extendOutputFunction": """
                async function extendOutputFunction({ $, request, response, html }) {
                    return {
                        title: $('title').text().trim(),
                        metaDescription: $('meta[name="description"]').attr('content') || '',
                        metaKeywords: $('meta[name="keywords"]').attr('content') || '',
                    };
                }
            """,
        }

        try:
            run = self.client.actor(actor_name).call(run_input=run_input)
            dataset = self.client.dataset(run["defaultDatasetId"]).list_items().items
            results = list(dataset)
            print(f"✅ 抓取完成，获取到 {len(results)} 条结果")
            return {
                "success": len(results) > 0,
                "targetUrl": TARGET_URL,
                "actorUsed": actor_name,
                "results": results,
                "resultCount": len(results),
                "scrapedAt": datetime.now().isoformat(),
            }
        except Exception as e:
            print(f"❌ 抓取失败: {e}")
            return {"success": False, "error": str(e)}


def format_text_output(data: Dict[str, Any]) -> str:
    """将结果格式化为可读的文本"""
    lines = []
    lines.append("=" * 60)
    lines.append("  🌐 百度首页抓取结果")
    lines.append("=" * 60)
    lines.append(f"  抓取时间: {data.get('scrapedAt', 'N/A')}")
    lines.append(f"  目标网址: {data.get('targetUrl', 'N/A')}")
    lines.append(f"  使用 Actor: {data.get('actorUsed', 'N/A')}")
    lines.append(f"  结果数量: {data.get('resultCount', 0)}")
    lines.append("-" * 60)

    for i, result in enumerate(data.get("results", [])):
        lines.append(f"\n  📄 页面 {i + 1}:")
        lines.append(f"     标题: {result.get('title', 'N/A')}")
        lines.append(f"     网址: {result.get('url', 'N/A')}")

        if result.get("metaDescription"):
            lines.append(f"     描述: {result['metaDescription']}")

        # 导航链接
        nav_links = result.get("navLinks", [])
        if nav_links:
            lines.append(f"\n  🔗 导航链接 ({len(nav_links)} 条):")
            for link in nav_links[:10]:
                lines.append(f"     - {link.get('text', 'N/A')}: {link.get('href', 'N/A')}")

        # 热门搜索
        hot = result.get("hotSearches", [])
        if hot:
            lines.append(f"\n  🔥 热门搜索 ({len(hot)} 条):")
            for j, item in enumerate(hot[:15], 1):
                lines.append(f"     {j}. {item}")

        # 页面预览
        preview = result.get("bodyPreview", "")
        if preview:
            lines.append(f"\n  📝 页面内容预览:")
            lines.append(f"     {preview[:500]}...")

        lines.append("-" * 40)

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Retrieve.py - 使用 Apify 抓取百度首页信息",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python Retrieve.py                    # 默认抓取并输出文本
  python Retrieve.py --output json      # 输出 JSON 格式
  python Retrieve.py --simple           # 使用简化版抓取器
  python Retrieve.py --actor apify/web-scraper  # 指定 Actor
  python Retrieve.py --save result.json # 保存到文件
        """,
    )
    parser.add_argument(
        "--output", "-o",
        choices=["text", "json"],
        default="text",
        help="输出格式 (默认: text)",
    )
    parser.add_argument(
        "--actor", "-a",
        default=DEFAULT_ACTOR,
        help=f"Apify Actor 名称 (默认: {DEFAULT_ACTOR})",
    )
    parser.add_argument(
        "--simple", "-s",
        action="store_true",
        help="使用简化版 Website Content Crawler 抓取",
    )
    parser.add_argument(
        "--save", "-f",
        type=str,
        help="将结果保存到文件",
    )
    parser.add_argument(
        "--token", "-t",
        type=str,
        help="Apify API Token (优先级高于环境变量)",
    )

    args = parser.parse_args()

    # 获取 API Token
    api_token = args.token or APIFY_API_TOKEN

    try:
        scraper = BaiduScraper(api_token)
    except ValueError as e:
        print(e)
        sys.exit(1)

    # 执行抓取
    if args.simple:
        data = scraper.scrape_simple()
    else:
        data = scraper.scrape(actor_name=args.actor)

    # 输出结果
    if args.output == "json":
        output = json.dumps(data, ensure_ascii=False, indent=2)
    else:
        output = format_text_output(data)

    print(output)

    # 保存到文件
    if args.save:
        save_path = args.save
        with open(save_path, "w", encoding="utf-8") as f:
            if save_path.endswith(".json"):
                json.dump(data, f, ensure_ascii=False, indent=2)
            else:
                f.write(format_text_output(data))
        print(f"\n💾 结果已保存到: {save_path}")

    # 返回状态码
    if not data.get("success"):
        sys.exit(1)


if __name__ == "__main__":
    main()
