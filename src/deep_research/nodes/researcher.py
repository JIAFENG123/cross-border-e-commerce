from __future__ import annotations

from typing import Dict, Any, List
from deep_research.utils.console import console
from deep_research.state import ResearchState
from deep_research.tools.scraper import ECommerceScraper
from deep_research.tools.search import MarketTrendSearcher
from deep_research.tools.cost_calculator import CostCalculator, ProductCostSpec


def researcher_node(state: ResearchState) -> dict:
    """Researcher Node: Concurrently executes domain tools to collect e-commerce metrics."""
    niche = state["niche_query"]
    resolved = state.get("resolved_product")
    iteration = state.get("iteration_count", 0) + 1
    target_display = f"{resolved['title']} (ASIN: {resolved['asin']})" if resolved and resolved.get("is_asin") else niche
    
    console.print(f"\n[bold blue]═══════════════════════════════════════════════════════[/bold blue]")
    console.print(f"[bold blue]>> [2. RESEARCHER] 第 {iteration} 轮数据采集与实体提取: {target_display[:60]}[/bold blue]")
    console.print(f"[bold blue]═══════════════════════════════════════════════════════[/bold blue]\n")

    # 1. Competitor Scraping
    competitors = ECommerceScraper.search_competitors(niche, resolved=resolved, limit=4)
    console.print(f"[green][OK] 获取到 {len(competitors)} 款高参考性同类对标竞品数据[/green]")

    # 2. VOC Defect Mining
    voc_defects = ECommerceScraper.mine_voc_defects(niche, resolved=resolved)
    console.print(f"[green][OK] 挖掘出 {len(voc_defects)} 大核心买家差评聚集缺陷[/green]")

    # 3. Market Trends
    trends = MarketTrendSearcher.fetch_market_trends(target_display)
    console.print(f"[green][OK] 汇总 {len(trends)} 条社媒真实场景诉求与趋势[/green]")

    # 4. Financial Modeling based on real category physical specs
    spec = ECommerceScraper.get_product_spec(niche, resolved=resolved, competitors=competitors)
    financial_analysis = CostCalculator.analyze(spec).model_dump()
    console.print(f"[green][OK] 完成落地总成本与 FBA 尺寸分段测算 (预测净利率: {financial_analysis['net_margin_percentage']}%, 评级: {financial_analysis['viability_rating']})[/green]\n")

    return {
        "competitors": competitors,
        "voc_defects": voc_defects,
        "market_trends": trends,
        "financial_model": financial_analysis,
        "iteration_count": iteration,
        "current_step": "researched"
    }
