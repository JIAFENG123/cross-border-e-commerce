"""Golden Benchmark Dataset for Cross-Border E-Commerce AI Agent Evaluation.

Defines ground-truth benchmarks, physical specifications, FBA classification rules,
and known real-world buyer VOC defect profiles for regression testing.
"""

from __future__ import annotations

from typing import Dict, Any, List, Tuple
from pydantic import BaseModel, Field


class GoldenCase(BaseModel):
    case_id: str
    name: str
    query: str
    market: str = "US"
    category: str
    
    # Ground truth physical & logistics specs
    ground_truth_weight_lbs: float
    ground_truth_dimensions_inches: Tuple[float, float, float]  # (L, W, H)
    expected_fba_tier: str  # e.g., "Large Standard", "Small Standard", "Small Oversize / Bulky"
    expected_retail_range_usd: Tuple[float, float]
    
    # Key VOC defects that a competent researcher MUST uncover
    ground_truth_voc_clusters: List[Dict[str, Any]]
    required_voc_keywords: List[List[str]]  # Each sub-list represents an essential defect theme (OR logic within, AND across)
    
    # Structural expectations
    expected_min_competitors: int = 3
    expected_min_voc: int = 3

    # Financial redlines
    expected_min_net_margin_pct: float
    expected_max_net_margin_pct: float
    expected_sourcing_range_usd: Tuple[float, float]
    
    # Pre-cached state for instant deterministic testing
    sample_state: Dict[str, Any] = Field(default_factory=dict)


# Benchmark Case 1: Standard Consumer Electronics (Sony WH-CH720N Noise-Canceling Headphones)
CASE_SONY_HEADPHONE = GoldenCase(
    case_id="headphone_sony_wh_ch720n",
    name="Sony WH-CH720N 无线主动降噪头戴耳机 (标杆标品)",
    query="B0BS1QCFHX",
    market="US",
    category="Consumer Electronics",
    ground_truth_weight_lbs=0.85,
    ground_truth_dimensions_inches=(8.2, 8.2, 2.1),
    expected_fba_tier="Large Standard",
    expected_retail_range_usd=(49.99, 79.99),
    ground_truth_voc_clusters=[
        {
            "component": "头梁伸缩转轴 (Hinge)",
            "defect": "正常使用数月后塑料卡扣疲劳脆断",
            "keywords": ["hinge", "snap", "break", "headband", "断", "卡扣", "塑料"]
        },
        {
            "component": "前馈降噪麦克风 (ANC Mic)",
            "defect": "户外大风时风噪啸叫严重",
            "keywords": ["wind", "whistling", "mic", "noise", "啸叫", "风噪", "底噪"]
        },
        {
            "component": "蛋白皮耳罩 (Earpads)",
            "defect": "长时间佩戴闷热出汗、表面涂层水解脱落",
            "keywords": ["earpad", "sweat", "hot", "peel", "flaking", "耳罩", "出汗", "脱皮", "闷热"]
        }
    ],
    required_voc_keywords=[
        ["hinge", "snap", "break", "headband", "转轴", "断裂", "头梁"],
        ["wind", "mic", "whistling", "啸叫", "风噪", "底噪", "降噪"],
        ["earpad", "sweat", "peel", "耳罩", "闷热", "脱皮", "出汗"]
    ],
    expected_min_net_margin_pct=15.0,
    expected_max_net_margin_pct=35.0,
    expected_sourcing_range_usd=(8.0, 16.0),
    sample_state={
        "niche_query": "B0BS1QCFHX",
        "target_market": "US",
        "resolved_product": {
            "is_asin": True,
            "asin": "B0BS1QCFHX",
            "title": "Sony WH-CH720N Wireless Noise Canceling Headphones",
            "brand": "Sony"
        },
        "competitors": [
            {"brand": "Sony", "title": "WH-CH720N Wireless Noise Canceling", "price_usd": 59.99, "rating": 4.4, "reviews_count": 8920, "bsr_rank": 142, "estimated_monthly_sales": 8500},
            {"brand": "Soundcore", "title": "Anker Life Q30 Hybrid ANC", "price_usd": 79.99, "rating": 4.5, "reviews_count": 18400, "bsr_rank": 88, "estimated_monthly_sales": 12000},
            {"brand": "JBL", "title": "Tune 760NC Foldable", "price_usd": 64.95, "rating": 4.3, "reviews_count": 5210, "bsr_rank": 215, "estimated_monthly_sales": 5300},
            {"brand": "1MORE", "title": "SonoFlow Active Noise Cancelling", "price_usd": 49.99, "rating": 4.4, "reviews_count": 3410, "bsr_rank": 380, "estimated_monthly_sales": 3800}
        ],
        "voc_defects": [
            {
                "component": "头梁转轴伸缩处 (Hinge)",
                "defect_description": "正常佩戴 3-6 个月折痕处塑料疲劳脆断",
                "customer_quote": "The plastic around the headband snapped after just 4 months of normal office use.",
                "severity": "High",
                "frequency_percent": 42.0,
                "factory_countermeasure": "工厂模具改良：内部注塑骨架必须嵌入 0.8mm 65Mn 弹簧钢补强片，卡扣处改用锌合金冲压。"
            },
            {
                "component": "前馈麦克风腔体 (ANC Mic)",
                "defect_description": "户外刮风或跑步时底噪啸叫严重",
                "customer_quote": "ANC works fine indoors, but outside any gust of wind creates a loud screeching wind noise.",
                "severity": "Medium",
                "frequency_percent": 28.0,
                "factory_countermeasure": "声学腔体改良：在开孔前馈麦克风外部增设高密度防风透气阻尼网与硅胶减震密封圈。"
            },
            {
                "component": "蛋白皮耳罩 (Earpads)",
                "defect_description": "夏天闷热不透气，且 1 年后表层人造革水解脱落",
                "customer_quote": "Sweaty after 45 minutes, and fake leather started peeling all over my ears.",
                "severity": "Low",
                "frequency_percent": 18.0,
                "factory_countermeasure": "材料改良：接触皮肤面升级为蜂窝状冰丝凉感网布，侧边保留隔音皮，并设计可快速卡扣拆卸清洗。"
            }
        ],
        "financial_model": {
            "fba_tier": "Large Standard",
            "cubic_meters_per_unit": 0.0023,
            "dimensional_weight_lbs": 1.02,
            "billable_weight_lbs": 1.02,
            "sourcing_cost_usd": 10.42,
            "first_leg_shipping_usd": 0.52,
            "customs_and_tariff_usd": 2.61,
            "fba_fulfillment_fee_usd": 4.75,
            "amazon_referral_fee_usd": 9.00,
            "ad_spend_usd": 9.00,
            "return_allowance_usd": 1.80,
            "total_landed_cost_usd": 13.55,
            "total_operating_cost_usd": 38.10,
            "net_profit_usd": 21.89,
            "gross_margin_percentage": 77.4,
            "net_margin_percentage": 36.5,
            "roi_percentage": 161.5,
            "viability_rating": "Excellent (极佳蓝海品)"
        },
        "final_report": """# 《Sony WH-CH720N 同类标杆出海商业可行性深度决策报告》

## 一、 执行摘要与立项裁决 (Executive Summary & Verdict)
标杆品索尼 WH-CH720N 零售价稳定在 $59.99，BSR 稳居耳机大类 Top 150，月出货量约 8,500 件。赛道核心竞争矛盾在于“买家对佩戴舒适与降噪的高期待”与“低价位易断裂塑料件”的撕裂。全口径测算显示全链路净利率为 36.5%，单台纯利 $21.89，达到投决门槛，建议立项。

| 决策维度 | 核心量化指标 | 战略指导结论 |
|:---|:---|:---|
| **目标售价区间** | $59.99 (USD) | 卡位 $50-$80 放量黄金带，避开 $150+ 高端红海 |
| **单件落地总成本** | $13.55 (USD) | 采购 $10.42 + 头程海运拼箱 $0.52 + 关税 $2.61 |
| **FBA 配送与尺寸分段** | Large Standard ($4.75) | 计费重 1.02 lbs，包装外箱严控 18"x14"x8" 避免溢出 |
| **平台佣金与获客支出** | 佣金 $9.00 / 广告 $9.00 | 设定 ACOS ≤ 15%，退货损耗拨备 3% ($1.80) |
| **单件净利润与净利率** | **$21.89 (36.5%)** | ROI 达到 161.5%，财务安全垫充裕 |
| **投资裁决建议** | **批准立项 (Greenlight)** | 针对断梁与耳罩痛点实施结构开模改良后投入首批量产 |

> Verdict: ✅ 批准立项。优先攻关“65Mn 弹簧钢内嵌头梁模具”与“凉感耳罩面料”，锁定 Q3 旺季入仓。

## 二、 市场竞争格局与标杆竞品透视 (Competitor Matrix)
| 排名 | 品牌 / 型号 | 售价 (USD) | 评分 / 评价数 | BSR 排名 | 预估月销 | 核心卖点 | 致命短板 |
|:---|:---|:---|:---|:---|:---|:---|:---|
| **#1** | Sony WH-CH720N | $59.99 | 4.4 (8,920) | #142 | 8,500 件 | V1 降噪芯片、超轻 192g | 转轴易断、无收纳盒 |
| **#2** | Soundcore Life Q30 | $79.99 | 4.5 (18,400) | #88 | 12,000 件 | 三模主动降噪、APP 调音 | 耳罩夏天发闷脱皮 |
| **#3** | JBL Tune 760NC | $64.95 | 4.3 (5,210) | #215 | 5,300 件 | PureBass 纯正低音 | 夹头感强、头顶压痛 |
| **#4** | 1MORE SonoFlow | $49.99 | 4.4 (3,410) | #380 | 3,800 件 | Hi-Res 双金标、长续航 | 塑料质感廉价、通话杂音 |

## 三、 买家真实声音 (VOC) 逆向工程与工厂开模建议
1. **头梁伸缩转轴 (Hinge)**: 42% 差评集中在“正常佩戴 3-6 个月折痕处塑料疲劳脆断”。
   - **工厂开模对策**: 杜绝纯 ABS 注塑，模具内部必须预埋 0.8mm 65Mn 高回弹弹簧钢补强片，卡扣折叠处升级为锌合金冲压转轴，通过 10,000 次拉伸疲劳测试。
2. **前馈麦克风腔体 (ANC Mic)**: 28% 差评集中在“户外跑步或刮风时底噪风噪剧烈啸叫”。
   - **声学改模对策**: 在前馈麦克风拾音孔外部开模加装高密度防风透气阻尼网与硅胶减震密封圈，并微调 DSP 前馈降噪滤波器的高频截止点。
3. **蛋白皮耳罩 (Earpads)**: 18% 差评集中在“佩戴 45 分钟耳朵出汗发闷，1 年后表层人造革水解脱皮”。
   - **材料升级对策**: 皮肤接触面升级为蜂窝状冰丝凉感网布，侧边保留隔音皮，设计快拆卡扣结构便于买家自行拆卸清洗。

## 四、 风险雷达与出海合规避坑指南
1. **退货率陷阱**: 耳机属于高退货品类（行业平均退货率 8-12%），模型中已按 3% 单台计提损耗拨备，首批大货必须随箱赠送绒布收纳袋以降低运输擦伤。
2. **美国知识产权与蓝牙合规**: 必须获取 Bluetooth SIG BQB 认证、FCC-ID 无线电认证，严格避开索尼降噪天线外观专利。
3. **FBA 季节性仓储费**: Q4 (10-12月) FBA 仓储费由每立方英尺 $0.87 飙升至 $2.40，必须严控单台备货周转天数在 45 天以内。"""
    }
)

# Benchmark Case 2: Outdoor Small Appliance (Portable Camping Espresso Maker)
CASE_ESPRESSO_MAKER = GoldenCase(
    case_id="outdoor_portable_espresso_maker",
    name="便携式露营意式浓缩咖啡机 (高压加热小家电)",
    query="Portable Camping Espresso Maker",
    market="US",
    category="Outdoor Small Appliance",
    ground_truth_weight_lbs=1.65,
    ground_truth_dimensions_inches=(9.5, 3.5, 3.5),
    expected_fba_tier="Large Standard",
    expected_retail_range_usd=(69.99, 129.99),
    ground_truth_voc_clusters=[
        {
            "component": "高压密封圈 (O-ring Seal)",
            "defect": "多次加压冲煮后硅胶圈高温硬化导致侧漏/泄压",
            "keywords": ["leak", "seal", "o-ring", "pressure", "crema", "泄压", "漏水", "密封圈"]
        },
        {
            "component": "锂电池与自加热模块 (Battery & Heater)",
            "defect": "户外低温下加热速度极慢，满电仅能冲煮 2-3 杯",
            "keywords": ["battery", "charge", "heat", "slow", "dead", "电池", "续航", "加热慢"]
        },
        {
            "component": "手柄按压机械结构 (Piston Pump)",
            "defect": "手动按压阻力过大，女性单手难以持续施力",
            "keywords": ["pump", "stiff", "hand", "push", "hard", "按压", "费力", "卡死"]
        }
    ],
    required_voc_keywords=[
        ["leak", "seal", "pressure", "o-ring", "漏水", "泄压", "密封"],
        ["battery", "charge", "heat", "power", "电池", "续航", "加热"],
        ["pump", "stiff", "push", "hard", "按压", "费力", "阻力"]
    ],
    expected_min_net_margin_pct=20.0,
    expected_max_net_margin_pct=45.0,
    expected_sourcing_range_usd=(18.0, 32.0),
    sample_state={
        "niche_query": "Portable Camping Espresso Maker",
        "target_market": "US",
        "resolved_product": {
            "is_asin": False,
            "title": "Portable Camping Espresso Maker",
            "brand": "Generic"
        },
        "competitors": [
            {"brand": "Outin", "title": "Nano Portable Espresso Machine", "price_usd": 129.99, "rating": 4.4, "reviews_count": 3200, "bsr_rank": 820, "estimated_monthly_sales": 2500},
            {"brand": "Wacaco", "title": "Nanopresso Portable Espresso Maker", "price_usd": 64.90, "rating": 4.3, "reviews_count": 5100, "bsr_rank": 640, "estimated_monthly_sales": 4200},
            {"brand": "Conqueco", "title": "Portable Espresso Maker Heated", "price_usd": 99.98, "rating": 4.1, "reviews_count": 1890, "bsr_rank": 1450, "estimated_monthly_sales": 1200}
        ],
        "voc_defects": [
            {
                "component": "高压密封圈 (Gasket O-Ring)",
                "defect_description": "使用 15 次后硅胶密封圈出现微裂纹，萃取时 18bar 压力导致热水从螺纹边缘爆喷",
                "customer_quote": "Hot coffee sprayed all over my camp table because the gasket failed under pressure.",
                "severity": "High",
                "frequency_percent": 38.0,
                "factory_countermeasure": "升级为食品级氟橡胶 (FKM/Viton) 材质耐温 200°C，且开模增加双阶梯自锁倒角。"
            },
            {
                "component": "动力电池组 (Lithium Battery)",
                "defect_description": "户外 10°C 低温环境下电芯电压骤降，冷水自加热 3 杯后即报低电量",
                "customer_quote": "Battery dies after heating only 2 cups in chilly mountain mornings.",
                "severity": "High",
                "frequency_percent": 34.0,
                "factory_countermeasure": "换装 3 串 18650 汽车级动力电芯 (7500mAh)，配合 BMS 低温自保温电路算法。"
            },
            {
                "component": "注压活塞杆 (Hand Pump)",
                "defect_description": "活塞轴承缺油阻力过大，需 20kg 持续按压力度",
                "customer_quote": "Pumping 18 bars of pressure manually requires too much hand strength for my wife.",
                "severity": "Medium",
                "frequency_percent": 19.0,
                "factory_countermeasure": "增加杠杆微动省力弹簧与食品级聚四氟乙烯 (PTFE) 润滑导向套。"
            }
        ],
        "financial_model": {
            "fba_tier": "Large Standard",
            "cubic_meters_per_unit": 0.0019,
            "dimensional_weight_lbs": 0.84,
            "billable_weight_lbs": 1.65,
            "sourcing_cost_usd": 24.50,
            "first_leg_shipping_usd": 0.43,
            "customs_and_tariff_usd": 6.13,
            "fba_fulfillment_fee_usd": 5.40,
            "amazon_referral_fee_usd": 13.50,
            "ad_spend_usd": 13.50,
            "return_allowance_usd": 2.70,
            "total_landed_cost_usd": 31.06,
            "total_operating_cost_usd": 66.16,
            "net_profit_usd": 23.83,
            "gross_margin_percentage": 65.5,
            "net_margin_percentage": 26.5,
            "roi_percentage": 76.7,
            "viability_rating": "Excellent (极佳蓝海品)"
        },
        "final_report": """# 《便携露营高压加热咖啡机出海商业可行性深度决策报告》

## 一、 执行摘要与立项裁决 (Executive Summary & Verdict)
便携露营意式浓缩咖啡机是当前欧美户外轻奢生活方式的爆发性蓝海细分。标杆品零售价位于 $69.99-$129.99 区间。测算显示全口径净利率为 26.5%，单台纯利 $23.83，ROI 达 76.7%，各项指标均符合海外中高客单价精品立项红线，建议批准立项。

| 决策维度 | 核心量化指标 | 战略指导结论 |
|:---|:---|:---|
| **目标零售定价** | $89.99 (USD) | 避开 Outin ($129+) 高端品牌溢价，以极致性价比抢占大众露营市场 |
| **单台落地总成本** | $31.06 (USD) | 采购 $24.50 + 头程海运拼箱 $0.43 + 关税 $6.13 |
| **FBA 配送与尺寸分段** | Large Standard ($5.40) | 计费重 1.65 lbs，包装体积仅 0.0019 CBM，物流履约极其经济 |
| **全口径运营总成本** | $66.16 (USD) | 含佣金 $13.50、广告获客 $13.50 (ACOS 15%)、退换货拨备 $2.70 |
| **单台净利润与净利率** | **$23.83 (26.5%)** | 净利率显著高于行业 15% 安全垫，具备强抗风险能力 |
| **投资裁决建议** | **批准立项 (Greenlight)** | 针对高压密封与低温电池进行开模改款后，Q3 进入批量备货 |

> Verdict: ✅ 批准立项。重点攻关“食品级氟橡胶自锁密封圈”与“BMS 低温自保温电芯”，快速切入欧美 Prime Day 黄金档。

## 二、 市场竞争格局与标杆竞品透视 (Competitor Matrix)
| 排名 | 品牌 / 型号 | 售价 (USD) | 评分 / 评价数 | BSR 排名 | 预估月销 | 关键卖点 | 致命短板 |
|:---|:---|:---|:---|:---|:---|:---|:---|
| **#1** | Outin Nano Heated | $129.99 | 4.4 (3,200) | #820 | 2,500 件 | 3分钟冷水速热、20bar泵 | 机身较重、充电口防水差 |
| **#2** | Wacaco Nanopresso | $64.90 | 4.3 (5,100) | #640 | 4,200 件 | 机械便携、仅336克 | 无加热功能、纯手动按压费力 |
| **#3** | Conqueco Portable | $99.98 | 4.1 (1,890) | #1450 | 1,200 件 | 经济型自加热一体机 | 电池衰减快、密封圈易漏水 |

## 三、 买家真实声音 (VOC) 逆向工程与工厂开模建议
1. **高压密封圈 (Gasket O-Ring)**: 38% 差评集中在“冲煮 15 次后硅胶圈高温硬化导致高压泄压与漏水”。
   - **工厂开模对策**: 淘汰普通食品级硅胶，全线换装耐温 200°C 的食品级氟橡胶 (FKM/Viton)，开模在螺纹咬合处增加双阶梯自锁倒角，耐压上限提升至 25bar。
2. **动力电池组 (Lithium Battery)**: 34% 差评集中在“户外 10°C 低温环境下加热极慢，满电仅冲煮 2 杯”。
   - **硬件升级对策**: 采用 3 串 18650 汽车级动力电芯 (7500mAh / 30A 放电)，配合智能 BMS 低温自保温电路算法，确保冷水加热杯数提升至 4-5 杯。
3. **注压活塞与注水腔体 (Pump Mechanism)**: 19% 差评集中在“按压力度大，长时间使用卡死”。
   - **工程对策**: 增设杠杆省力微动结构与食品级聚四氟乙烯 (PTFE) 润滑导向套，阻力降低 40%。

## 四、 风险雷达与出海合规避坑指南
1. **电池空海运合规与认证**: 必须通过 UN38.3、MSDS、海运安全鉴定书及美国 UL 2054 电池安全认证，并取得 FDA 食品接触级认证。
2. **高压防爆与泄压保护**: 腔体内部增设弹簧机械超压自泄阀（设定阈值 22bar），避免买家咖啡粉填压过紧导致物理爆裂风险。
3. **退货与质保预备**: 提供 1 年换新保修，备件箱随赠 3 套原厂备用密封圈与专用拆装棒。"""
    }
)

# Benchmark Case 3: Bulky Oversize (Ergonomic Mesh Office Chair)
CASE_OFFICE_CHAIR = GoldenCase(
    case_id="furniture_mesh_office_chair",
    name="人体工学网布办公椅 (抛重型大件家具)",
    query="Ergonomic Mesh Office Chair",
    market="US",
    category="Home & Office Furniture",
    ground_truth_weight_lbs=34.0,
    ground_truth_dimensions_inches=(26.0, 26.0, 14.5),
    expected_fba_tier="Small Oversize / Bulky",
    expected_retail_range_usd=(119.99, 199.99),
    ground_truth_voc_clusters=[
        {
            "component": "瓦楞包装箱 (Outer Carton)",
            "defect": "单层纸箱运输中破损严重，导致五星脚和滚轮掉落刮花",
            "keywords": ["box", "damaged", "torn", "missing", "scratched", "纸箱", "破损", "少件", "刮花"]
        },
        {
            "component": "气压升降棒 (Gas Lift Cylinder)",
            "defect": "使用 2-3 个月后缓慢漏气下沉并发出金属异响",
            "keywords": ["gas", "cylinder", "sink", "drop", "squeak", "气压杆", "下沉", "异响", "漏气"]
        },
        {
            "component": "坐垫网布与前沿骨架 (Seat Mesh Frame)",
            "defect": "网布张力衰退松垮，大腿前端压迫硬塑料横梁导致下肢发麻",
            "keywords": ["mesh", "sag", "numb", "plastic", "thigh", "网布", "塌陷", "大腿", "硌腿", "发麻"]
        }
    ],
    required_voc_keywords=[
        ["box", "damaged", "torn", "package", "破损", "纸箱", "包装"],
        ["gas", "cylinder", "sink", "drop", "气压杆", "下沉", "气棒"],
        ["mesh", "sag", "frame", "thigh", "网布", "塌陷", "压腿", "发麻"]
    ],
    expected_min_net_margin_pct=10.0,
    expected_max_net_margin_pct=28.0,
    expected_sourcing_range_usd=(25.0, 45.0),
    sample_state={
        "niche_query": "Ergonomic Mesh Office Chair",
        "target_market": "US",
        "resolved_product": {
            "is_asin": False,
            "title": "Ergonomic Mesh Office Chair",
            "brand": "Generic"
        },
        "competitors": [
            {"brand": "Hbada", "title": "Ergonomic Office Chair Flip-up Armrests", "price_usd": 129.99, "rating": 4.2, "reviews_count": 14200, "bsr_rank": 35, "estimated_monthly_sales": 9500},
            {"brand": "Mimoglad", "title": "Ergonomic Mesh High Back Chair", "price_usd": 159.99, "rating": 4.4, "reviews_count": 6800, "bsr_rank": 78, "estimated_monthly_sales": 5100},
            {"brand": "SIHOO", "title": "M18 Ergonomic Office Chair", "price_usd": 179.99, "rating": 4.3, "reviews_count": 9400, "bsr_rank": 52, "estimated_monthly_sales": 7200}
        ],
        "voc_defects": [
            {
                "component": "瓦楞纸箱与内部缓冲 (Carton Packaging)",
                "defect_description": "海运颠簸及最后一公里派送中外箱穿孔，五星脚塑料边缘破损严重，配件散落丢失",
                "customer_quote": "Box was severely mangled, wheel casters fell out during transit.",
                "severity": "High",
                "frequency_percent": 46.0,
                "factory_countermeasure": "外箱升级为美卡双坑五层加厚瓦楞纸箱 (250磅耐破)，关键边角加装 15mm 珍珠棉护角封套。"
            },
            {
                "component": "防爆气压棒 (Gas Lift Cylinder)",
                "defect_description": "低成本 2 级气压杆密封圈漏气，久坐 30 分钟自动回落至最低档",
                "customer_quote": "The gas cylinder sinks down every time I sit on it after 3 months.",
                "severity": "High",
                "frequency_percent": 31.0,
                "factory_countermeasure": "淘汰普通 2 级气棒，全线标配 SGS 及 TUV 认证 4 级加厚防爆气压棒。"
            },
            {
                "component": "坐框前沿 (Waterfall Seat Rim)",
                "defect_description": "透气网布久坐松弛后，大腿根部直接紧压前沿硬质塑料横梁，阻断血液循环",
                "customer_quote": "The mesh loosened, and now the hard plastic front edge cuts off leg circulation.",
                "severity": "Medium",
                "frequency_percent": 21.0,
                "factory_countermeasure": "前沿坐框内衬 45D 高回弹定型切绵斜坡过渡，网布采用杜邦高抗拉聚酯纤维。"
            }
        ],
        "financial_model": {
            "fba_tier": "Small Oversize / Bulky",
            "cubic_meters_per_unit": 0.1606,
            "dimensional_weight_lbs": 70.52,
            "billable_weight_lbs": 70.52,
            "sourcing_cost_usd": 32.00,
            "first_leg_shipping_usd": 36.14,
            "customs_and_tariff_usd": 8.00,
            "fba_fulfillment_fee_usd": 22.40,
            "amazon_referral_fee_usd": 22.50,
            "ad_spend_usd": 22.50,
            "return_allowance_usd": 4.50,
            "total_landed_cost_usd": 76.14,
            "total_operating_cost_usd": 148.04,
            "net_profit_usd": 1.95,
            "gross_margin_percentage": 49.2,
            "net_margin_percentage": 1.3,
            "roi_percentage": 2.6,
            "viability_rating": "High Risk (薄利/对投流敏感)"
        },
        "final_report": """# 《人体工学网布办公椅出海可行性与大件抛货风控报告》

## 一、 执行摘要与立项裁决 (Executive Summary & Verdict)
人体工学办公椅属于典型的高客单价、极高物流敏感型大件抛货（Bulky / Oversize）。测算显示当前零售价 $149.99 下，净利率仅 1.3%，单件纯利 $1.95，处于微利亏损边缘。其根本痛点在于单件体积重高达 70.5 lbs，导致尾程 FBA 配送费 ($22.40) 与头程海运费 ($36.14) 吞噬了 40% 的销售额。裁决意见为：**暂缓立项 / 极高风险 (Conditional Reject)**，除非对包装实行“K/D 全拆装扁平化开模”，将体积压缩 30% 以上。

| 决策维度 | 核心量化指标 | 战略指导结论 |
|:---|:---|:---|
| **目标零售售价** | $149.99 (USD) | 处于 $120-$180 主流红海带，价格天花板被头部品牌压制 |
| **单件落地总成本** | $76.14 (USD) | 工厂采购 $32.00 + 头程海运拼箱 $36.14 + 关税 $8.00 |
| **FBA 配送与尺寸分段** | Small Oversize / Bulky | 单件 FBA 配送费高达 $22.40，且体积重高达 70.5 lbs |
| **全口径运营总成本** | $148.04 (USD) | 含平台佣金 $22.50 (15%)、ACOS 广告 $22.50、退换货拨备 $4.50 |
| **预估净利润与净利率** | **$1.95 (1.3%)** | ROI 仅 2.6%，极易因汇率或海运费上涨陷入负利润 |
| **投资裁决建议** | **⚠️ 极高风险 / 暂缓立项** | 必须完成外包装 K/D 紧凑型扁平改模，否则不予放行大货投入 |

> Verdict: ⚠️ 审慎立项 / 风险警示。当前供应链包装体积过大，必须重新设计扁平拆装纸箱并改用 4 级气压棒，方可考虑二次投决。

## 二、 市场竞争格局与标杆竞品透视 (Competitor Matrix)
| 排名 | 品牌 / 型号 | 售价 (USD) | 评分 / 评价数 | BSR 排名 | 预估月销 | 关键卖点 | 致命短板 |
|:---|:---|:---|:---|:---|:---|:---|:---|
| **#1** | Hbada Flip-up Arms | $129.99 | 4.2 (14,200) | #35 | 9,500 件 | 可翻转扶手、空间收纳 | 气压棒异响、腰托硬 |
| **#2** | Mimoglad High Back | $159.99 | 4.4 (6,800) | #78 | 5,100 件 | 自适应腰靠、大角度后仰 | 纸箱破损率高、少螺丝 |
| **#3** | SIHOO M18 Ergonomic | $179.99 | 4.3 (9,400) | #52 | 7,200 件 | 经典爆款、全金属底座 | 坐垫前沿压大腿下肢发麻 |

## 三、 买家真实声音 (VOC) 逆向工程与工厂改模建议
1. **外箱包装破损与配件散落 (Carton Packaging)**: 46% 差评集中在“外箱海运受潮穿孔，五星脚塑料磕碰破裂，螺丝包滑出丢失”。
   - **包装工程对策**: 升级为 250 磅耐破度五层加厚 BC 坑美卡瓦楞箱，外箱四周嵌入 15mm 硬质珍珠棉边角防护，螺丝配件包采用吸塑封装卡在坐垫底部。
2. **气压升降棒漏气 (Gas Lift Cylinder)**: 31% 差评集中在“正常使用 2-3 个月后坐下自动慢沉下坠”。
   - **核心部件对策**: 严禁采购廉价 2 级气压杆，全线换装经 SGS、BIFMA、TUV 认证的标准 4 级加厚防爆气压棒（管壁厚度 ≥ 2.5mm）。
3. **坐框前沿压迫血管 (Waterfall Seat Rim)**: 21% 差评集中在“久坐大腿发麻”。
   - **模具改良对策**: 开模前沿向下弧度扩大 15°，增加瀑布型高密度回弹切绵缓冲垫，网布升级为杜邦高抗拉耐磨复合丝。

## 四、 风险雷达与大件出海合规避坑指南
1. **退货死局**: 大件家具逆向退货物流成本超过 $40/单，若退货率达 6% 则全盘必亏，必须随机附赠备用轮与内六角扳手以降低“因组装困难而退货”。
2. **BIFMA X5.1 结构安全测试**: 必须通过美国办公家具 ANSI/BIFMA X5.1 静压（136kg）与跌落测试，避免因断裂引发人身伤害诉讼。
3. **FBA 旺季超大件附加费**: 规避 Q4 仓储峰值费率，建议结合美西海外仓（第三方 3PL）分流一件代发。"""
    }
)

ALL_GOLDEN_CASES = [
    CASE_SONY_HEADPHONE,
    CASE_ESPRESSO_MAKER,
    CASE_OFFICE_CHAIR
]


def get_golden_case(case_id: str) -> GoldenCase:
    for c in ALL_GOLDEN_CASES:
        if c.case_id == case_id or c.query.lower() == case_id.lower():
            return c
    raise ValueError(f"GoldenCase with id '{case_id}' not found in benchmark.")
