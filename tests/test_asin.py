from deep_research.tools.scraper import ECommerceScraper


def test_asin_resolution():
    info = ECommerceScraper.resolve_asin("B0BS1QCFHX")
    assert info["is_asin"] is True
    assert info["asin"] == "B0BS1QCFHX"
    assert "Sony" in info["brand"] or "Sony" in info["title"]
    assert "Headphone" in info["title"] or "WH-CH720N" in info["title"]


def test_asin_competitor_matching():
    info = ECommerceScraper.resolve_asin("B0BS1QCFHX")
    competitors = ECommerceScraper.search_competitors("B0BS1QCFHX", resolved=info)
    
    assert len(competitors) >= 3
    # Verify that all competitors are Audio/Headphones, NOT espresso or sports gear!
    for comp in competitors:
        title_lower = comp["title"].lower()
        assert any(w in title_lower for w in ["headphone", "soundcore", "jbl", "sony", "1more", "audio", "anc"]), (
            f"Competitor '{comp['title']}' is not an audio headphone!"
        )


def test_asin_voc_matching():
    info = ECommerceScraper.resolve_asin("B0BS1QCFHX")
    voc = ECommerceScraper.mine_voc_defects("B0BS1QCFHX", resolved=info)
    
    assert len(voc) >= 3
    components = [v["component"].lower() for v in voc]
    # Verify defects correspond to headphone issues (ANC, Headband, Bluetooth)
    assert any("noise" in c or "anc" in c for c in components)
    assert any("headband" in c or "hinge" in c or "earpad" in c for c in components)
