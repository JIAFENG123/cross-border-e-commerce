from __future__ import annotations

from typing import Annotated, Any, Dict, List, Optional
from typing_extensions import TypedDict
import operator
from pydantic import BaseModel, Field


class SubTask(BaseModel):
    task_id: str = Field(description="Unique task id e.g. task_competitor_scan")
    title: str = Field(description="Short title of the task")
    description: str = Field(description="Detailed objective")
    dimension: str = Field(
        description="Target dimension: competitor_analysis | voc_mining | cost_modeling | trend_synthesis"
    )
    status: str = Field(default="pending", description="pending | in_progress | completed | failed")
    queries: List[str] = Field(default_factory=list, description="Target search queries or ASINs")
    findings: Optional[str] = Field(default=None, description="Extracted findings")


class CompetitorItem(BaseModel):
    asin: str = Field(description="Amazon ASIN or product ID")
    title: str = Field(description="Product title")
    brand: str = Field(default="Unknown", description="Brand name")
    price_usd: float = Field(default=0.0, description="Retail price in USD")
    rating: float = Field(default=0.0, description="Average review rating (0.0 - 5.0)")
    reviews_count: int = Field(default=0, description="Total review count")
    bsr_rank: Optional[int] = Field(default=None, description="Best Sellers Rank")
    bsr_category: Optional[str] = Field(default=None, description="BSR category name")
    key_selling_points: List[str] = Field(default_factory=list, description="Bullet points / strengths")
    estimated_monthly_sales: Optional[int] = Field(default=None, description="Estimated monthly units sold")


class VOCDefect(BaseModel):
    component: str = Field(description="Component or feature involved e.g. 'Seal Ring', 'Battery', 'Lid'")
    defect_description: str = Field(description="What went wrong or broke")
    customer_quote: str = Field(description="Representative customer feedback or review excerpt")
    severity: str = Field(default="Medium", description="High | Medium | Low")
    frequency_percent: float = Field(default=0.0, description="Estimated percentage of negative reviews")
    factory_countermeasure: str = Field(description="How to improve in 1688 / OEM production")


class ResearchState(TypedDict):
    # Input parameters
    niche_query: str
    target_market: str
    resolved_product: Optional[Dict[str, Any]]  # Real product metadata if query is ASIN or URL
    llm_provider: Optional[str]  # e.g. "groq" or "nvidia"
    llm_model: Optional[str]     # e.g. "qwen/qwen3.8-27b"
    
    # Strategic Plan
    plan_overview: str
    subtasks: List[SubTask]
    current_step: str
    
    # Collected Domain Knowledge (Using additive reducer where appropriate)
    competitors: Annotated[List[Dict[str, Any]], operator.add]
    voc_defects: Annotated[List[Dict[str, Any]], operator.add]
    market_trends: Annotated[List[str], operator.add]
    financial_model: Optional[Dict[str, Any]]
    
    # Reflection & Critique Loop
    critic_notes: Annotated[List[str], operator.add]
    iteration_count: int
    max_iterations: int
    is_sufficient: bool
    
    # Final Output
    final_report: Optional[str]
