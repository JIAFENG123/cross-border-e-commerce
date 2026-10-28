from __future__ import annotations

import sys
import argparse
from pathlib import Path
from rich.markdown import Markdown
from rich.panel import Panel

from deep_research.utils.console import console
from deep_research.graph import build_research_graph


def main():
    parser = argparse.ArgumentParser(description="Cross-Border E-Commerce Deep Research AI Agent")
    parser.add_argument("niche", type=str, help="Product niche keyword or competitor ASIN (e.g. 'Portable Camping Espresso Maker')")
    parser.add_argument("--market", type=str, default="US", help="Target Amazon marketplace (default: US)")
    parser.add_argument("--max-iter", type=int, default=2, help="Maximum research & reflection iterations")
    parser.add_argument("--output", type=str, default="deep_research_report.md", help="Output report filepath")
    
    args = parser.parse_args()

    console.print(Panel.fit(
        f"[bold cyan]跨境电商垂直版 Deep Research AI Agent[/bold cyan]\n"
        f"[dim]调研品类: [white]{args.niche}[/white] | 站点: [white]{args.market}[/white] | 最大反思轮数: [white]{args.max_iter}[/white][/dim]",
        border_style="cyan"
    ))

    graph = build_research_graph()

    initial_state = {
        "niche_query": args.niche,
        "target_market": args.market,
        "resolved_product": None,
        "max_iterations": args.max_iter,
        "iteration_count": 0,
        "competitors": [],
        "voc_defects": [],
        "market_trends": [],
        "critic_notes": [],
        "is_sufficient": False,
        "plan_overview": "",
        "subtasks": [],
        "current_step": "init",
        "financial_model": None,
        "final_report": None,
    }

    try:
        final_state = graph.invoke(initial_state)
        report = final_state.get("final_report", "未生成报告")

        # Output to file
        out_path = Path(args.output)
        out_path.write_text(report, encoding="utf-8")
        console.print(f"\n[bold green][OK] 调研已完成！完整报告已保存至: [underline]{out_path.resolve()}[/underline][/bold green]\n")

        # Render preview in terminal
        console.print(Panel(Markdown(report), title=f"[bold green]《{args.niche}》商业可行性决策报告[/bold green]", border_style="green"))

    except KeyboardInterrupt:
        console.print("\n[yellow]用户手动终止调研[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red][ERROR] 运行异常: {e}[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
