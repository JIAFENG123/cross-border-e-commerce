from __future__ import annotations

from typing import Dict, Any, Tuple
from pydantic import BaseModel, Field


class ProductCostSpec(BaseModel):
    # Dimensions in inches and weight in lbs
    weight_lbs: float = Field(default=1.2, description="Actual product weight in lbs (including package)")
    length_inches: float = Field(default=8.5, description="Package length in inches")
    width_inches: float = Field(default=4.0, description="Package width in inches")
    height_inches: float = Field(default=4.0, description="Package height in inches")

    # Financial parameters
    sourcing_cost_cny: float = Field(default=65.0, description="Factory wholesale cost in RMB (ex-factory)")
    retail_price_usd: float = Field(default=49.99, description="Target Amazon retail price in USD")
    exchange_rate_usd_cny: float = Field(default=7.20, description="USD/CNY exchange rate")

    # Logistics & Tariff assumptions
    ocean_freight_per_cbm_usd: float = Field(default=180.0, description="Ocean freight per CBM (cubic meter) to US port")
    last_mile_trucking_per_cbm_usd: float = Field(default=45.0, description="US customs clearance + drayage to FBA warehouse")
    us_tariff_rate: float = Field(default=0.25, description="Tariff rate including Section 301 (e.g. 25%)")
    ad_spend_percentage: float = Field(default=0.15, description="Target ACOS (Advertising Cost of Sales, e.g. 15%)")
    return_loss_rate: float = Field(default=0.03, description="Estimated return & damage loss rate (e.g. 3%)")


class LandedCostAnalysis(BaseModel):
    # Tier classification
    fba_tier: str
    cubic_meters_per_unit: float
    dimensional_weight_lbs: float
    billable_weight_lbs: float

    # Cost breakdown per unit in USD
    sourcing_cost_usd: float
    first_leg_shipping_usd: float
    customs_and_tariff_usd: float
    fba_fulfillment_fee_usd: float
    amazon_referral_fee_usd: float
    ad_spend_usd: float
    return_allowance_usd: float

    # Totals & Margins
    total_landed_cost_usd: float  # Ex-factory + shipping + tariffs
    total_operating_cost_usd: float  # All-in cost before tax
    net_profit_usd: float
    gross_margin_percentage: float
    net_margin_percentage: float
    roi_percentage: float  # Net profit / (Sourcing + Shipping + Tariff)
    viability_rating: str  # Excellent | Healthy | High Risk | Unviable


class CostCalculator:
    """Calculates Amazon FBA, Ocean Freight, Customs Duty and Net Profit Margin."""

    @staticmethod
    def classify_fba_tier(length: float, width: float, height: float, weight: float) -> Tuple[str, float]:
        """Classify Amazon FBA size tier and calculate fulfillment fee (US marketplace)."""
        dims = sorted([length, width, height], reverse=True)
        longest, median, shortest = dims[0], dims[1], dims[2]

        # Calculate dimensional weight: (L x W x H) / 139
        dim_weight = (longest * median * shortest) / 139.0

        # Small Standard: max 15" x 12" x 0.75", max 16 oz (1 lb)
        if longest <= 15.0 and median <= 12.0 and shortest <= 0.75 and weight <= 1.0:
            tier = "Small Standard"
            billable_weight = weight
            fee = 3.22 if billable_weight <= 0.5 else 3.40

        # Large Standard: max 18" x 14" x 8", max 20 lbs
        elif longest <= 18.0 and median <= 14.0 and shortest <= 8.0 and weight <= 20.0:
            tier = "Large Standard"
            billable_weight = max(weight, dim_weight)
            if billable_weight <= 0.5:
                fee = 3.86
            elif billable_weight <= 1.0:
                fee = 4.15
            elif billable_weight <= 1.5:
                fee = 4.75
            elif billable_weight <= 2.0:
                fee = 5.40
            elif billable_weight <= 3.0:
                fee = 6.10
            else:
                fee = 6.10 + 0.38 * (billable_weight - 3.0)

        # Oversize / Bulky
        else:
            tier = "Small Oversize / Bulky"
            billable_weight = max(weight, dim_weight)
            fee = 9.73 + 0.42 * max(0.0, billable_weight - 1.0)

        return tier, round(fee, 2)

    @classmethod
    def analyze(cls, spec: ProductCostSpec) -> LandedCostAnalysis:
        # 1. Volume in cubic meters (1 inch = 0.0254 m)
        cbm = (spec.length_inches * 0.0254) * (spec.width_inches * 0.0254) * (spec.height_inches * 0.0254)

        # 2. FBA Tier & fee
        fba_tier, fba_fee = cls.classify_fba_tier(
            spec.length_inches, spec.width_inches, spec.height_inches, spec.weight_lbs
        )
        dim_weight = (spec.length_inches * spec.width_inches * spec.height_inches) / 139.0
        billable_weight = max(spec.weight_lbs, dim_weight)

        # 3. Unit Costs in USD
        sourcing_usd = spec.sourcing_cost_cny / spec.exchange_rate_usd_cny
        shipping_usd = cbm * (spec.ocean_freight_per_cbm_usd + spec.last_mile_trucking_per_cbm_usd)
        tariff_usd = sourcing_usd * spec.us_tariff_rate

        # 4. Amazon fees
        referral_fee = spec.retail_price_usd * 0.15  # 15% standard category referral fee
        ad_spend = spec.retail_price_usd * spec.ad_spend_percentage
        return_allowance = spec.retail_price_usd * spec.return_loss_rate

        # 5. Summaries
        landed_cost = sourcing_usd + shipping_usd + tariff_usd
        total_operating_cost = landed_cost + fba_fee + referral_fee + ad_spend + return_allowance
        net_profit = spec.retail_price_usd - total_operating_cost

        gross_margin = ((spec.retail_price_usd - landed_cost) / spec.retail_price_usd) * 100.0
        net_margin = (net_profit / spec.retail_price_usd) * 100.0
        roi = (net_profit / max(0.01, landed_cost)) * 100.0

        if net_margin >= 25.0:
            viability = "Excellent (极佳蓝海品)"
        elif net_margin >= 15.0:
            viability = "Healthy (健康常规品)"
        elif net_margin >= 5.0:
            viability = "High Risk (薄利/对投流敏感)"
        else:
            viability = "Unviable (亏损或极高破产风险)"

        return LandedCostAnalysis(
            fba_tier=fba_tier,
            cubic_meters_per_unit=round(cbm, 4),
            dimensional_weight_lbs=round(dim_weight, 2),
            billable_weight_lbs=round(billable_weight, 2),
            sourcing_cost_usd=round(sourcing_usd, 2),
            first_leg_shipping_usd=round(shipping_usd, 2),
            customs_and_tariff_usd=round(tariff_usd, 2),
            fba_fulfillment_fee_usd=round(fba_fee, 2),
            amazon_referral_fee_usd=round(referral_fee, 2),
            ad_spend_usd=round(ad_spend, 2),
            return_allowance_usd=round(return_allowance, 2),
            total_landed_cost_usd=round(landed_cost, 2),
            total_operating_cost_usd=round(total_operating_cost, 2),
            net_profit_usd=round(net_profit, 2),
            gross_margin_percentage=round(gross_margin, 1),
            net_margin_percentage=round(net_margin, 1),
            roi_percentage=round(roi, 1),
            viability_rating=viability,
        )
