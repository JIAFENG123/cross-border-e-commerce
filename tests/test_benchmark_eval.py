import json
from pathlib import Path
from deep_research.tools.scraper import ECommerceScraper


BENCHMARK_FILE = Path(__file__).parent / "data" / "golden_benchmark.json"


def test_golden_benchmark_dataset_integrity():
    """Verify that the golden benchmark file exists and conforms to standard evaluation schema."""
    assert BENCHMARK_FILE.exists(), f"Benchmark file {BENCHMARK_FILE} does not exist"
    
    with open(BENCHMARK_FILE, "r", encoding="utf-8") as f:
        cases = json.load(f)
        
    assert isinstance(cases, list)
    assert len(cases) >= 3, "Golden benchmark should have at least 3 curated benchmark cases"
    
    for case in cases:
        assert "id" in case
        assert "query" in case
        assert "target_market" in case
        assert "ground_truth" in case
        gt = case["ground_truth"]
        assert "expected_competitor_keywords" in gt
        assert "critical_voc_defects" in gt
        assert "factory_actionable_solutions" in gt
        assert "financial_thresholds" in gt


def test_benchmark_case_audio_headphone():
    """Evaluate Case 1: Audio ANC Headphone (B0BS1QCFHX) against Golden Ground Truth."""
    with open(BENCHMARK_FILE, "r", encoding="utf-8") as f:
        cases = json.load(f)
    case = next(c for c in cases if c["id"] == "case_audio_anc_headphone")
    gt = case["ground_truth"]

    # 1. Scrape / Resolve
    info = ECommerceScraper.resolve_asin(case["query"])
    assert info["is_asin"] is True
    assert "Sony" in info["brand"] or "Sony" in info["title"]

    # 2. Competitor matching against keyword ground truth
    competitors = ECommerceScraper.search_competitors(case["query"], resolved=info)
    assert len(competitors) >= 3
    for comp in competitors:
        title_lower = comp["title"].lower()
        assert any(k in title_lower for k in gt["expected_competitor_keywords"]), (
            f"Competitor '{comp['title']}' drifted from golden keywords: {gt['expected_competitor_keywords']}"
        )

    # 3. VOC Defect matching
    voc = ECommerceScraper.mine_voc_defects(case["query"], resolved=info)
    assert len(voc) >= 3
    components_text = " ".join([v["component"].lower() + " " + v["defect_description"].lower() for v in voc])
    assert any(w in components_text for w in ["noise", "anc", "sound", "headband", "hinge", "earpad"])
