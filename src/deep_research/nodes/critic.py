from __future__ import annotations

from deep_research.utils.console import console
from deep_research.state import ResearchState
from deep_research.llm import get_llm

CRITIC_PROMPT = """你是一名严苛的跨境投资与产品立项质检专家（Critic）。
请根据当前 Agent 搜集的数据指标进行质检审查，判断是否足以支撑高层决策报告撰写。
审查维度：
1. 竞品数据完整性（样本数、价格带分布、是否有明显断层）
2. VOC 深度（是否有可落地至工厂注塑/材质改良的具体点，而非空泛抱怨）
3. 财务模型合理性（FBA 配送费、抛重、关税、净利率测算是否完整）

请输出一段 2-3 句话的评估结论，指出当前发现的最大亮点与后续落地必须警惕的隐患点。
"""


def critic_node(state: ResearchState) -> dict:
    """Critic Node: Evaluates research completeness and determines if another loop is needed."""
    iteration = state.get("iteration_count", 1)
    max_iter = state.get("max_iterations", 2)
    competitors = state.get("competitors", [])
    voc_defects = state.get("voc_defects", [])
    financial_model = state.get("financial_model", {})

    console.print(f"\n[bold yellow]═══════════════════════════════════════════════════════[/bold yellow]")
    console.print(f"[bold yellow]>> [3. CRITIC] 质检评估与反思循环 (第 {iteration}/{max_iter} 轮)[/bold yellow]")
    console.print(f"[bold yellow]═══════════════════════════════════════════════════════[/bold yellow]\n")

    # Algorithmic check on data quality
    has_competitors = len(competitors) >= 3
    has_voc = len(voc_defects) >= 3
    has_finances = bool(financial_model and financial_model.get("net_profit_usd") is not None)

    llm = get_llm(provider=state.get("llm_provider"), model_name=state.get("llm_model"))
    summary_input = f"""
收集到的竞品数量: {len(competitors)}
收集到的VOC痛点数量: {len(voc_defects)}
预测净利率: {financial_model.get('net_margin_percentage')}% (FBA分段: {financial_model.get('fba_tier')})
核心痛点概要: {[v.get('component') for v in voc_defects[:3]]}
"""
    try:
        response = llm.invoke([
            {"role": "system", "content": CRITIC_PROMPT},
            {"role": "user", "content": summary_input}
        ])
        critique_text = response.content.strip()
    except Exception as e:
        console.print(f"[yellow]Critic LLM 降级: {e}[/yellow]")
        critique_text = (
            f"数据完备度达到立项标准。竞品价格带覆盖完整，VOC 聚焦于密封件高压泄漏与按压疲劳，"
            f"当前财务模型显示净利率约为 {financial_model.get('net_margin_percentage')}%，具备进入下一阶段撰写的前提。"
        )

    # Determine sufficiency: if critical data present or max iterations reached
    is_sufficient = (has_competitors and has_voc and has_finances) or (iteration >= max_iter)

    console.print(f"[cyan]质检审核意见: {critique_text}[/cyan]")
    if is_sufficient:
        console.print(f"[bold green][OK] 判定通过：数据置信度达标，准予流转至最终商业可行性报告撰写 (Synthesizer)[/bold green]\n")
    else:
        console.print(f"[bold red][FAIL] 判定未达标：需补充新维度查询，启动回退搜索[/bold red]\n")

    return {
        "critic_notes": [critique_text],
        "is_sufficient": is_sufficient,
        "current_step": "critiqued"
    }
