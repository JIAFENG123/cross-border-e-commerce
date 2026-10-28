from __future__ import annotations

import json
from deep_research.utils.console import console
from deep_research.state import ResearchState, SubTask
from deep_research.llm import get_llm
from deep_research.tools.scraper import ECommerceScraper

PLANNER_SYSTEM_PROMPT = """你是一名拥有10年经验的顶级跨境电商选品与商业战略总监。
用户会给你一个拟出海的细分品类（如“便携式户外意式浓缩咖啡机”）或目标市场。
你的任务是将宏观调研目标拆解为4个具有专业深度、互不重叠的子任务清单（SubTasks）：
1. competitor_analysis：头部竞品排查（BSR排名、价格带分布、月销预估、核心卖点矩阵）
2. voc_mining：买家声音与差评逆向挖掘（退货痛点、1-3星差评部件故障、失效场景）
3. cost_modeling：供应链出厂价与落地总成本测算（FBA尺寸分段、抛重、海运关税、毛利率门槛）
4. trend_synthesis：海外社媒口碑与趋势（Reddit/TikTok使用场景、送礼属性、季节性）

请输出一段对该品类的战略预判综述（plan_overview），并确保子任务涵盖上述4个维度。
"""


def planner_node(state: ResearchState) -> dict:
    """Planner Node: Breaks the research query into structured subtasks."""
    niche = state["niche_query"]
    market = state.get("target_market", "US")
    
    # 1. Resolve ASIN or URL if provided
    resolved = ECommerceScraper.resolve_asin(niche)
    target_display = f"{resolved['title']} (ASIN: {resolved['asin']})" if resolved.get("is_asin") else niche
    
    console.print(f"\n[bold magenta]═══════════════════════════════════════════════════════[/bold magenta]")
    console.print(f"[bold magenta]>> [1. PLANNER] 启动多维度调研规划: {target_display} (站点: {market})[/bold magenta]")
    console.print(f"[bold magenta]═══════════════════════════════════════════════════════[/bold magenta]\n")
    
    llm = get_llm(provider=state.get("llm_provider"), model_name=state.get("llm_model"))
    prompt = f"""品类/标杆产品: {target_display}
目标站点: {market}

请以跨境电商操盘手的专业视角，给出对该赛道的规划预判综述（3句话以内），提炼最核心的竞争矛盾点。"""

    try:
        response = llm.invoke([
            {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])
        plan_overview = response.content.strip()
    except Exception as e:
        console.print(f"[yellow]Planner 调用大模型降级兜底: {e}[/yellow]")
        plan_overview = f"针对 {target_display} 赛道，核心矛盾在于买家对功能体验与做工品质的高预期，需重点把控关键零部件品控并优化头程物流抛重比。"

    # Standardized 4-dimensional subtasks
    subtasks = [
        SubTask(
            task_id="task_competitor_scan",
            title="头部竞品与价格带扫描",
            description=f"检索 {market} 亚马逊同类目直接对标竞品 Listing、BSR 分布与月销量",
            dimension="competitor_analysis",
            queries=[f"{target_display} competitors", f"{target_display} best sellers"]
        ),
        SubTask(
            task_id="task_voc_mining",
            title="买家差评与核心缺陷逆向工程",
            description="抓取同类目 1-3 星差评，聚类零部件故障与买家抱怨场景",
            dimension="voc_mining",
            queries=[f"{target_display} negative reviews", f"{target_display} complaints"]
        ),
        SubTask(
            task_id="task_landed_cost",
            title="头程海运/FBA配送费/落地毛利测算",
            description="核算体积重（抛重）、关税及净利率是否满足20%安全红线",
            dimension="cost_modeling",
            queries=[f"{target_display} package dimensions", f"{target_display} shipping weight"]
        ),
        SubTask(
            task_id="task_social_trends",
            title="海外社媒真实口碑与长尾趋势",
            description="洞察 Reddit 与 Google Trends 中的场景痛点与送礼属性",
            dimension="trend_synthesis",
            queries=[f"{target_display} reddit discussion", f"{target_display} tiktok trend"]
        ),
    ]

    console.print(f"[green][OK] 规划生成完毕：已建立 4 项专业子任务队列[/green]")
    console.print(f"[dim]战略综述: {plan_overview[:100]}...[/dim]\n")

    return {
        "plan_overview": plan_overview,
        "subtasks": subtasks,
        "resolved_product": resolved,
        "current_step": "planned"
    }
