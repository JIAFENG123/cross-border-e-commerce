from deep_research.tools.cost_calculator import CostCalculator, ProductCostSpec


def test_fba_tier_classification():
    # Small Standard
    tier, fee = CostCalculator.classify_fba_tier(length=10, width=8, height=0.5, weight=0.4)
    assert tier == "Small Standard"
    assert fee == 3.22

    # Large Standard
    tier, fee = CostCalculator.classify_fba_tier(length=8.5, width=4.0, height=4.0, weight=1.2)
    assert tier == "Large Standard"
    assert fee > 4.0


def test_cost_and_profit_analysis():
    spec = ProductCostSpec(
        weight_lbs=1.2,
        length_inches=8.5,
        width_inches=4.0,
        height_inches=4.0,
        sourcing_cost_cny=60.0,
        retail_price_usd=49.99,
        exchange_rate_usd_cny=7.20,
        ocean_freight_per_cbm_usd=180.0,
        last_mile_trucking_per_cbm_usd=45.0,
        us_tariff_rate=0.25,
        ad_spend_percentage=0.15,
        return_loss_rate=0.03
    )

    analysis = CostCalculator.analyze(spec)

    assert analysis.sourcing_cost_usd == round(60.0 / 7.20, 2)
    assert analysis.fba_tier == "Large Standard"
    assert analysis.net_profit_usd > 0
    assert analysis.net_margin_percentage > 10.0
    assert "Healthy" in analysis.viability_rating or "Excellent" in analysis.viability_rating
