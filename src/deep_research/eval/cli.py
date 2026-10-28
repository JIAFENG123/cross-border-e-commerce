"""Command-Line Interface for Cross-Border E-Commerce AI Agent Eval Pipeline.

Usage:
    # Run deterministic + golden benchmark checks on cached sample states (instant < 1s)
    uv run python -m deep_research.eval.cli

    # Run with live LangGraph execution end-to-end
    uv run python -m deep_research.eval.cli --mode live

    # Run single case without LLM judge for instant CI/CD
    uv run python -m deep_research.eval.cli --case headphone_sony_wh_ch720n --no-judge
"""

from __future__ import annotations

import sys
if sys.platform == "win32":
    try:
        if sys.stdout and hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if sys.stderr and hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import argparse
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from deep_research.eval.golden_dataset import ALL_GOLDEN_CASES, get_golden_case
from deep_research.eval.evaluator import AgentEvaluator

console = Console()


def main():
    parser = argparse.ArgumentParser(description="AI Agent Industrial Evaluation Pipeline (Benchmark & Eval)")
    parser.add_argument(
        "--mode",
        choices=["state", "live"],
        default="state",
        help="Evaluation mode: 'state' (test against benchmark states) or 'live' (run LangGraph end-to-end)"
    )
    parser.add_argument(
        "--case",
        type=str,
        default=None,
        help="Specific case ID to evaluate (e.g., 'headphone_sony_wh_ch720n')"
    )
    parser.add_argument(
        "--no-judge",
        action="store_true",
        help="Disable LLM-as-a-Judge semantic scoring for ultra-fast local CI/CD"
    )
    parser.add_argument(
        "--provider",
        type=str,
        default="groq",
        help="LLM provider for live mode and LLM judge (default: groq)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="artifacts/eval",
        help="Output directory for generated evaluation reports"
    )

    args = parser.parse_args()

    # Determine cases
    if args.case:
        try:
            cases = [get_golden_case(args.case)]
        except ValueError as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            sys.exit(1)
    else:
        cases = ALL_GOLDEN_CASES

    console.print()
    console.print(Panel(
        f"[bold cyan]Cross-Border E-Commerce AI Agent Systemic Eval Pipeline[/bold cyan]\n"
        f"[dim]Mode: [bold]{args.mode.upper()}[/bold] | Cases: [bold]{len(cases)}[/bold] | "
        f"LLM Judge: [bold]{'Disabled' if args.no_judge else 'Enabled (Groq GPT-OSS 120B)'}[/bold][/dim]",
        border_style="cyan"
    ))
    console.print()

    evaluator = AgentEvaluator(run_judge=not args.no_judge, provider=args.provider)

    with console.status("[bold green]Executing multi-tiered evaluation checks...[/bold green]"):
        report = evaluator.run_suite(
            cases=cases,
            mode=args.mode,
            save_report=True,
            output_dir=args.output
        )

    # 1. Per-Case Results Table
    table = Table(title="[bold]>> Golden Benchmark Evaluation Matrix (By Case)[/bold]", header_style="bold magenta")
    table.add_column("Case ID", style="dim", width=26)
    table.add_column("Product Name", style="bold")
    table.add_column("Math Eq", justify="center")
    table.add_column("FBA Tier", justify="center")
    table.add_column("VOC Recall", justify="right")
    table.add_column("LLM Judge", justify="right")
    table.add_column("Total Score", justify="right", style="bold")
    table.add_column("Verdict", justify="center")

    for r in report.results:
        math_badge = "[green]✓ 100%[/green]" if r.math_metric.passed else "[red]✕ FAIL[/red]"
        fba_badge = f"[green]✓ {r.fba_metric.metadata.get('assigned', 'Match')}[/green]" if r.fba_metric.passed else f"[red]✕ {r.fba_metric.metadata.get('assigned')}[/red]"
        voc_badge = f"{r.voc_metric.score * 100:.0f}%"
        judge_badge = f"{r.judge_result.composite_score_pct:.1f}" if r.judge_result else "N/A"
        verdict = "[bold green]PASS[/bold green]" if r.passed else "[bold red]FAIL[/bold red]"

        table.add_row(
            r.case_id,
            r.case_name[:24],
            math_badge,
            fba_badge,
            voc_badge,
            judge_badge,
            f"{r.overall_score:.1f}",
            verdict
        )

    console.print(table)
    console.print()

    # 2. Macro KPI Summary Table
    kpi_table = Table(title="[bold]>> Macro Quality & Reliability Redlines[/bold]", header_style="bold green")
    kpi_table.add_column("Dimension", style="bold")
    kpi_table.add_column("Observed Value", justify="center", style="bold cyan")
    kpi_table.add_column("Industry Standard Threshold", justify="center", style="dim")
    kpi_table.add_column("Status", justify="center")

    kpi_table.add_row(
        "Overall Benchmark Pass Rate",
        f"{report.pass_rate_pct}% ({report.passed_cases}/{report.total_cases})",
        "≥ 90.0%",
        "[green]PASSED[/green]" if report.pass_rate_pct >= 90.0 else "[yellow]ATTENTION[/yellow]"
    )
    kpi_table.add_row(
        "Financial Math & Accounting Balance",
        f"{report.math_integrity_rate_pct}%",
        "100.0% (Zero-Tolerance)",
        "[green]PASSED[/green]" if report.math_integrity_rate_pct == 100.0 else "[red]FAILED[/red]"
    )
    kpi_table.add_row(
        "FBA Size Tier Classification Accuracy",
        f"{report.fba_accuracy_rate_pct}%",
        "≥ 95.0%",
        "[green]PASSED[/green]" if report.fba_accuracy_rate_pct >= 95.0 else "[red]FAILED[/red]"
    )
    kpi_table.add_row(
        "VOC Failure Mode Semantic Recall",
        f"{report.avg_voc_recall_pct}%",
        "≥ 75.0%",
        "[green]PASSED[/green]" if report.avg_voc_recall_pct >= 75.0 else "[yellow]ATTENTION[/yellow]"
    )
    if report.avg_judge_score_pct > 0:
        kpi_table.add_row(
            "LLM-as-a-Judge Feasibility Rating",
            f"{report.avg_judge_score_pct} / 100",
            "≥ 80.0",
            "[green]PASSED[/green]" if report.avg_judge_score_pct >= 80.0 else "[yellow]FAIR[/yellow]"
        )

    console.print(kpi_table)
    console.print()

    console.print(f"[bold green]✓[/bold green] Eval report artifacts successfully exported to: [underline]{args.output}[/underline]")
    console.print(f"[dim]Timestamp: {report.timestamp} | Latency: {report.avg_latency_seconds}s per case[/dim]\n")


if __name__ == "__main__":
    main()
