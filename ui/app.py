import os
import sys

# Ensure project root and src/ are in sys.path for cloud deployment
_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SRC_DIR = os.path.join(_ROOT_DIR, "src")
for _p in [_SRC_DIR, _ROOT_DIR]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        if sys.stdout and hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if sys.stderr and hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import streamlit as st
import json
import pandas as pd

# Sync Streamlit cloud secrets to os.environ if running on Streamlit Cloud
try:
    if hasattr(st, "secrets"):
        for _k, _v in st.secrets.items():
            if isinstance(_v, str) and _k not in os.environ:
                os.environ[_k] = _v
except Exception:
    pass

# Page Configuration - Must be the very first Streamlit command
st.set_page_config(
    page_title="Deep Research · 跨境电商出海商业决策智能体",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── World-Class Minimalist & Zero-Latency Typography CSS ──────────────────────
# Note: System fonts only — NO blocking external @import to guarantee instant 0ms white-screen-free load!
MINIMAL_DESIGN_CSS = """
<style>
:root {
    --bg-paper: #FAF8F5;
    --bg-card: #FFFFFF;
    --bg-subtle: #F4F1EA;
    --border-color: #E8E5DD;
    --border-light: #F0EDE5;
    --text-primary: #232220;
    --text-secondary: #5C5851;
    --text-muted: #8C877D;
    --accent-terracotta: #C25E3E;
    --accent-terracotta-hover: #AA4E31;
    --accent-terracotta-subtle: #FDF4F0;
    --accent-sage: #2F634E;
    --accent-sage-subtle: #EEF4F1;
}

/* Base Body & Zero-Flicker Layout */
.stApp {
    background-color: var(--bg-paper) !important;
    color: var(--text-primary) !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Inter", sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

/* Hide default streamlit clutter */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3.5rem !important;
    max-width: 1140px !important;
}

/* Editorial Serif Headings */
h1, h2, h3, .serif-heading {
    font-family: "Charter", "Bitstream Charter", "Sitka Text", "Cambria", "Georgia", "Source Serif Pro", serif !important;
    font-weight: 500 !important;
    letter-spacing: -0.02em !important;
    color: var(--text-primary) !important;
}

/* Terracotta Primary Action Button */
.stButton > button[kind="primary"] {
    background-color: var(--accent-terracotta) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 9px !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    padding: 0.6rem 1.6rem !important;
    box-shadow: 0 1px 3px rgba(194, 94, 62, 0.18) !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

.stButton > button[kind="primary"]:hover {
    background-color: var(--accent-terracotta-hover) !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(194, 94, 62, 0.25) !important;
}

/* Secondary & Preset Buttons */
.stButton > button[kind="secondary"] {
    background-color: #FFFFFF !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    font-size: 12px !important;
    padding: 0.35rem 0.8rem !important;
    transition: all 0.15s ease !important;
}

.stButton > button[kind="secondary"]:hover {
    border-color: var(--accent-terracotta) !important;
    color: var(--accent-terracotta) !important;
    background-color: var(--accent-terracotta-subtle) !important;
}

/* Search Input Card Styling */
.search-card-container {
    background: #FFFFFF;
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 1.5rem 1.75rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.03), 0 6px 20px rgba(0,0,0,0.015);
    margin-bottom: 1.75rem;
}

/* Inputs */
.stTextInput > div > div > input {
    border-radius: 10px !important;
    border: 1px solid var(--border-color) !important;
    background-color: #FAF8F5 !important;
    font-size: 14px !important;
    padding: 0.65rem 0.9rem !important;
    color: var(--text-primary) !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--accent-terracotta) !important;
    background-color: #FFFFFF !important;
    box-shadow: 0 0 0 2px var(--accent-terracotta-subtle) !important;
}

.stSelectbox > div > div {
    border-radius: 8px !important;
    border: 1px solid var(--border-color) !important;
    background-color: #FAF8F5 !important;
    font-size: 13px !important;
}

/* Stepper Card */
.minimal-step-card {
    background: #FFFFFF;
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 1rem 1.15rem;
    min-height: 94px;
    transition: all 0.25s ease;
}

.minimal-step-card.active {
    border-color: var(--accent-terracotta) !important;
    background-color: var(--accent-terracotta-subtle) !important;
}

.minimal-step-card.completed {
    border-color: #C8DBD1 !important;
    background-color: var(--accent-sage-subtle) !important;
}

.minimal-step-card.waiting {
    opacity: 0.65;
    background-color: #FCFBF9;
}

.status-pill {
    font-size: 11px;
    font-weight: 600;
    padding: 2px 7px;
    border-radius: 10px;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

.status-pill.active {
    background: #F8E2D8;
    color: var(--accent-terracotta);
}

.status-pill.completed {
    background: #DDEBE3;
    color: var(--accent-sage);
}

.status-pill.waiting {
    background: #EDEAE3;
    color: var(--text-muted);
}

.pulse-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background-color: var(--accent-terracotta);
    animation: pulseAnim 1.4s infinite;
}

@keyframes pulseAnim {
    0% { opacity: 0.3; transform: scale(0.9); }
    50% { opacity: 1; transform: scale(1.2); }
    100% { opacity: 0.3; transform: scale(0.9); }
}

/* Metric Display Cards */
[data-testid="stMetric"] {
    background-color: #FFFFFF !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 14px !important;
    padding: 1.25rem 1.4rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02) !important;
}

[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
    font-size: 0.76rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    font-family: "Charter", "Bitstream Charter", "Georgia", serif !important;
    color: var(--text-primary) !important;
    font-size: 2.1rem !important;
    font-weight: 500 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 1px solid var(--border-color);
    background: transparent;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0;
    padding: 10px 18px;
    color: var(--text-muted) !important;
    font-size: 13.5px;
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    color: var(--accent-terracotta) !important;
    border-bottom: 2px solid var(--accent-terracotta) !important;
    font-weight: 600 !important;
}

/* Progress */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, var(--accent-terracotta), #DE8A36) !important;
    border-radius: 999px;
}

/* Feature Pillars Grid */
.feature-pillar-card {
    background: #FFFFFF;
    border: 1px solid var(--border-color);
    border-radius: 14px;
    padding: 1.5rem 1.6rem;
    height: 100%;
}
</style>
"""
st.markdown(MINIMAL_DESIGN_CSS, unsafe_allow_html=True)


# ─── Lazy-Loaded Agent Engine (Instant 0ms Page Startup) ───────────────────────
@st.cache_resource(show_spinner="⚡ 正在连接 LangGraph 智能体状态引擎...")
def get_compiled_graph():
    from deep_research.graph import build_research_graph
    return build_research_graph()


def get_app_settings():
    from deep_research.config import get_settings
    return get_settings()


# ─── Step Card Component Renderer ─────────────────────────────────────────────
def render_stepper_card(num: int, title: str, status: str, detail: str) -> str:
    if status == "active":
        badge = '<span class="status-pill active"><span class="pulse-dot"></span> 执行中</span>'
        cls = "minimal-step-card active"
    elif status == "completed":
        badge = '<span class="status-pill completed">✓ 完成</span>'
        cls = "minimal-step-card completed"
    else:
        badge = '<span class="status-pill waiting">○ 待机</span>'
        cls = "minimal-step-card waiting"

    return f"""
    <div class="{cls}">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
        <span style="font-weight:600; font-size:13px; color:#232220;">{num}. {title}</span>
        {badge}
      </div>
      <div style="font-size:12px; color:#706B62; line-height:1.45;">{detail}</div>
    </div>
    """


# ─── Header: Serene & Minimalist Editorial ────────────────────────────────────
st.markdown("""
<div style="margin-bottom: 1.8rem;">
  <div style="display:inline-flex; align-items:center; gap:8px; background:#FBF3EE; border:1px solid #F0DFD5; border-radius:6px; padding:3px 9px; margin-bottom:10px;">
    <span style="font-size:10px; font-weight:700; color:#C25E3E; text-transform:uppercase; letter-spacing:0.06em;">Deep Research · AI Agent</span>
    <span style="color:#B88E7D; font-size:11px;">|</span>
    <span style="font-size:11px; color:#7A5546;">LangGraph 状态图与跨模型热备</span>
  </div>
  <h1 class="serif-heading" style="font-size: 2.35rem; margin: 0 0 8px 0; color: #232220;">出海商业可行性深度调研</h1>
  <p style="color: #6E695F; font-size: 14.5px; line-height: 1.6; margin: 0; max-width: 780px;">
    面向跨境操盘手与供应链投资人。输入目标细分品类或亚马逊 ASIN，自主完成多维路径规划、标杆竞品透视、买家 VOC 逆向缺陷挖掘与 FBA 履约全成本测算。
  </p>
</div>
""", unsafe_allow_html=True)


# ─── Model Choices ────────────────────────────────────────────────────────────
settings = get_app_settings()
MODEL_CHOICES = {
    "⚡ Groq · Qwen 3.8 27B (极速 ~500ms · 推荐)": {
        "provider": "groq", "model": "qwen/qwen3.8-27b",
        "badge": "Groq LPU 极速响应", "desc": "毫秒级响应，跨境电商多语言/中文分析极度流畅。"
    },
    "⚡ Groq · GPT-OSS 120B (高推理长文)": {
        "provider": "groq", "model": "openai/gpt-oss-120b",
        "badge": "Groq LPU 深度推理", "desc": "120B 强逻辑大模型，擅长复杂商业逻辑推演。"
    },
    "🧠 NVIDIA NIM · Nemotron 550B (旗舰大底座)": {
        "provider": "nvidia", "model": settings.nvidia_model,
        "badge": "NVIDIA 550B", "desc": "550B 超大规模模型，商业报告文风成熟厚重。"
    }
}


# ─── Hero Command & Input Panel (Centerpiece) ─────────────────────────────────
# Session state management for query presets
if "niche_query_input" not in st.session_state:
    st.session_state["niche_query_input"] = "B0BS1QCFHX"

st.markdown('<div class="search-card-container">', unsafe_allow_html=True)

# Main Query Input Bar
col_input, col_action = st.columns([4, 1])
with col_input:
    query_text = st.text_input(
        "调研输入",
        value=st.session_state["niche_query_input"],
        placeholder="输入品类关键词 (如 Portable Camping Espresso Maker) 或亚马逊 ASIN (如 B0BS1QCFHX)...",
        label_visibility="collapsed"
    )
with col_action:
    start_btn = st.button("🚀 启动深度调研", type="primary", use_container_width=True)

# Quick Preset Chips Row
chip_col1, chip_col2, chip_col3, _ = st.columns([1.3, 1.4, 1.7, 3])
with chip_col1:
    if st.button("🎧 索尼降噪耳机", type="secondary", use_container_width=True):
        st.session_state["niche_query_input"] = "B0BS1QCFHX"
        st.rerun()
with chip_col2:
    if st.button("☕ 便携浓缩咖啡机", type="secondary", use_container_width=True):
        st.session_state["niche_query_input"] = "Portable Camping Espresso Maker"
        st.rerun()
with chip_col3:
    if st.button("🪑 人体工学网椅 (抛货)", type="secondary", use_container_width=True):
        st.session_state["niche_query_input"] = "Ergonomic Mesh Office Chair"
        st.rerun()

# Advanced Parameters Expander (Clean & Uncluttered)
with st.expander("⚙️ 引擎配置与调研参数 (站点 / 模型 / 反思轮数)", expanded=False):
    param_col1, param_col2, param_col3 = st.columns(3)
    with param_col1:
        chosen_market = st.selectbox("目标站点", ["US (美国站)", "UK (英国站)", "DE (德国站)", "JP (日本站)"], index=0)
    with param_col2:
        chosen_model_label = st.selectbox("驱动大模型底座", options=list(MODEL_CHOICES.keys()), index=0)
    with param_col3:
        max_iter = st.slider("最大反思质检轮数", min_value=1, max_value=3, value=1)

    selected_engine = MODEL_CHOICES[chosen_model_label]
    st.caption(f"**当前策略**：主引擎 `{selected_engine['provider'].upper()}` (`{selected_engine['model']}`)，若网络波动自动跨服务无缝降级兜底。")

st.markdown('</div>', unsafe_allow_html=True)


# ─── Execution Logic ──────────────────────────────────────────────────────────
if start_btn:
    market_code = chosen_market.split()[0]
    graph = get_compiled_graph()

    initial_state = {
        "niche_query": query_text.strip(),
        "target_market": market_code,
        "resolved_product": None,
        "llm_provider": selected_engine["provider"],
        "llm_model": selected_engine["model"],
        "max_iterations": max_iter,
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

    st.markdown("<h3 class='serif-heading' style='font-size:1.35rem; margin:1.5rem 0 0.75rem 0;'>状态机流转监视器 (Live StateGraph Stepper)</h3>", unsafe_allow_html=True)
    progress_bar = st.progress(5, text="正在启动 LangGraph 状态图工作流...")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        s1_box = st.empty()
        s1_box.markdown(render_stepper_card(1, "Planner", "active", "正在拆解调研路径与意图..."), unsafe_allow_html=True)
    with col2:
        s2_box = st.empty()
        s2_box.markdown(render_stepper_card(2, "Researcher", "waiting", "等待调度出海工具链..."), unsafe_allow_html=True)
    with col3:
        s3_box = st.empty()
        s3_box.markdown(render_stepper_card(3, "Critic", "waiting", "等待质检反思审查..."), unsafe_allow_html=True)
    with col4:
        s4_box = st.empty()
        s4_box.markdown(render_stepper_card(4, "Synthesizer", "waiting", "等待综合生成立项报告..."), unsafe_allow_html=True)

    stream_log_box = st.expander("🔍 实时执行细节流 (Live Agent Updates)", expanded=True)
    current_state = dict(initial_state)

    for event in graph.stream(current_state, stream_mode="updates"):
        node_name = list(event.keys())[0]
        node_data = event[node_name]
        current_state.update(node_data)

        if node_name == "planner":
            resolved = current_state.get("resolved_product") or {}
            prod_name = resolved.get("title", query_text)[:28]
            s1_box.markdown(render_stepper_card(1, "Planner", "completed", f"拆解完成 · {prod_name}"), unsafe_allow_html=True)
            s2_box.markdown(render_stepper_card(2, "Researcher", "active", "正在采集同类竞品与 VOC..."), unsafe_allow_html=True)
            progress_bar.progress(35, text="2/4 正在采集同类对标竞品与买家差评...")

            with stream_log_box:
                st.write(f"📋 **战略规划概览**：{current_state.get('plan_overview', '')}")
                subtasks = current_state.get("subtasks", [])
                st.write(f"已创建 **{len(subtasks)}** 个多维度子任务：`{[t.title for t in subtasks]}`")

        elif node_name == "researcher":
            competitors = current_state.get("competitors", [])
            voc_defects = current_state.get("voc_defects", [])
            fin = current_state.get("financial_model", {}) or {}
            margin = fin.get("net_margin_percentage", 0)

            s2_box.markdown(render_stepper_card(2, "Researcher", "completed", f"{len(competitors)}款竞品 · {len(voc_defects)}大痛点 · 净利{margin}%"), unsafe_allow_html=True)
            s3_box.markdown(render_stepper_card(3, "Critic", "active", "正在质检数据置信度与毛利..."), unsafe_allow_html=True)
            progress_bar.progress(68, text="3/4 质检专家正在审查数据与毛利红线...")

            with stream_log_box:
                st.write(f"📊 **已抓取标杆与竞品 ({len(competitors)}款)**：`{[c.get('brand') + ': ' + c.get('title')[:30] for c in competitors]}`")
                st.write(f"⚠️ **已提炼 VOC 缺陷 ({len(voc_defects)}项)**：`{[v.get('component') for v in voc_defects]}`")
                st.write(f"💰 **全口径销售净利率**：`{margin}%` (评级: `{fin.get('viability_rating')}`)")

        elif node_name == "critic":
            notes = current_state.get("critic_notes", [])
            critique_summary = notes[-1] if notes else "数据置信度达标"

            s3_box.markdown(render_stepper_card(3, "Critic", "completed", "质检通过 · 数据与毛利指标达标"), unsafe_allow_html=True)
            s4_box.markdown(render_stepper_card(4, "Synthesizer", "active", "正在综合撰写万字立项报告..."), unsafe_allow_html=True)
            progress_bar.progress(85, text="4/4 正在综合撰写万字级商业可行性报告...")

            with stream_log_box:
                st.write(f"⚖️ **质检专家审查意见**：{critique_summary}")

        elif node_name == "synthesizer":
            report_len = len(current_state.get("final_report", ""))
            s4_box.markdown(render_stepper_card(4, "Synthesizer", "completed", f"立项报告合成就绪 ({report_len}字)"), unsafe_allow_html=True)
            progress_bar.progress(100, text="🎉 深度调研全流程闭环完成！")

            with stream_log_box:
                st.write("📝 **最终报告撰写就绪**，下方仪表盘已同步解锁！")

    st.session_state["final_state"] = current_state
    st.rerun()


# ─── Results Dashboard View ───────────────────────────────────────────────────
if "final_state" in st.session_state:
    state = st.session_state["final_state"]
    resolved = state.get("resolved_product")
    fin = state.get("financial_model") or {}
    competitors = state.get("competitors") or []
    voc = state.get("voc_defects") or []
    report = state.get("final_report") or ""

    st.markdown("<hr style='border:none; border-top:1px solid #E8E5DD; margin:2rem 0;'>", unsafe_allow_html=True)

    # Recognition banner if ASIN
    if resolved and resolved.get("is_asin"):
        st.markdown(f"""
        <div style="background:#FDF5F1; border:1px solid #F0D9CE; border-radius:12px; padding:14px 18px; margin-bottom:1.5rem; display:flex; align-items:center; gap:12px;">
          <span style="font-size:20px;">🎯</span>
          <div>
            <div style="font-size:14px; font-weight:600; color:#232220;">标杆竞品锚定成功：{resolved.get('title')}</div>
            <div style="font-size:12px; color:#6E695F; margin-top:2px;">品牌: <b>{resolved.get('brand')}</b> &nbsp;|&nbsp; ASIN: <b>{resolved.get('asin')}</b> &nbsp;|&nbsp; 站点: <b>{state.get('target_market')}</b></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # 4 Key Metrics Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("商业可行性评级", fin.get("viability_rating", "Healthy"))
    with col2:
        st.metric("预估销售净利率", f"{fin.get('net_margin_percentage', 0)}%")
    with col3:
        st.metric("单台预估纯利润", f"${fin.get('net_profit_usd', 0)}")
    with col4:
        st.metric("FBA 尺寸分段", fin.get("fba_tier", "Standard"))

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    # 4 Structured Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📑 决策立项报告", "🏆 标杆竞品透视", "⚠️ 买家差评缺陷(VOC)", "💰 FBA抛重利润模型"
    ])

    with tab1:
        down_col, _ = st.columns([1, 4])
        with down_col:
            st.download_button(
                label="📥 下载 Markdown 决策报告",
                data=report,
                file_name=f"{state['niche_query'].replace(' ', '_')}_feasibility_report.md",
                mime="text/markdown",
                use_container_width=True
            )
        st.markdown(report)

    with tab2:
        if competitors:
            df_comp = pd.DataFrame(competitors)[[
                "brand", "title", "price_usd", "rating", "reviews_count", "bsr_rank", "estimated_monthly_sales"
            ]]
            df_comp.columns = ["品牌", "商品标题", "售价($)", "评分", "评价总数", "BSR排名", "预估月销量"]
            st.dataframe(df_comp, use_container_width=True)

    with tab3:
        if voc:
            df_voc = pd.DataFrame(voc)[[
                "component", "defect_description", "customer_quote", "severity", "frequency_percent", "factory_countermeasure"
            ]]
            df_voc.columns = ["涉事部件", "故障描述", "买家原声抱怨", "严重等级", "发生频率(%)", "工厂模具改良方案"]
            st.dataframe(df_voc, use_container_width=True)

    with tab4:
        if fin:
            fc1, fc2 = st.columns(2)
            with fc1:
                st.markdown("<h4 class='serif-heading' style='font-size:1.15rem; margin-bottom:0.75rem;'>📦 物理与包装分段</h4>", unsafe_allow_html=True)
                st.write(f"- **FBA 计费重 (Billable Weight)**: `{fin.get('billable_weight_lbs')} lbs`")
                st.write(f"- **包装体积重 (Dimensional Weight)**: `{fin.get('dimensional_weight_lbs')} lbs`")
                st.write(f"- **单件海运体积 (CBM)**: `{fin.get('cubic_meters_per_unit')} m³`")
                st.write(f"- **单件全口径落地成本 (Landed Cost)**: `${fin.get('total_landed_cost_usd')}`")
            with fc2:
                st.markdown("<h4 class='serif-heading' style='font-size:1.15rem; margin-bottom:0.75rem;'>💵 全口径成本分解 (单件)</h4>", unsafe_allow_html=True)
                st.write(f"- 工厂采购价: `${fin.get('sourcing_cost_usd')}`")
                st.write(f"- 头程海运拼箱: `${fin.get('first_leg_shipping_usd')}`")
                st.write(f"- 美国进口关税 (25%): `${fin.get('customs_and_tariff_usd')}`")
                st.write(f"- 亚马逊 FBA 配送费: `${fin.get('fba_fulfillment_fee_usd')}`")
                st.write(f"- 平台销售佣金 (15%): `${fin.get('amazon_referral_fee_usd')}`")
                st.write(f"- 预估广告获客支出 (ACOS 16%): `${fin.get('ad_spend_usd')}`")

else:
    # ─── Initial Welcome Showcase: 3 Value Pillars ────────────────────────────
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    fcol1, fcol2, fcol3 = st.columns(3)
    with fcol1:
        st.markdown("""
        <div class="feature-pillar-card">
          <div style="font-size: 24px; margin-bottom: 8px;">🎯</div>
          <h3 class="serif-heading" style="font-size: 1.15rem; margin: 0 0 6px 0;">精准标杆锚定</h3>
          <p style="font-size: 13px; color: #706B62; line-height: 1.5; margin: 0;">
            支持直接输入 ASIN 逆向解析真实类目、品牌与价格带，杜绝跨品类漂移，精准挖掘 Top 标杆竞品。
          </p>
        </div>
        """, unsafe_allow_html=True)
    with fcol2:
        st.markdown("""
        <div class="feature-pillar-card">
          <div style="font-size: 24px; margin-bottom: 8px;">⚠️</div>
          <h3 class="serif-heading" style="font-size: 1.15rem; margin: 0 0 6px 0;">VOC 差评逆向工程</h3>
          <p style="font-size: 13px; color: #706B62; line-height: 1.5; margin: 0;">
            聚焦 1~3 星高频质量与体验故障，直接提炼可落地交付给 1688 / 模具工厂的结构与材料改良对策。
          </p>
        </div>
        """, unsafe_allow_html=True)
    with fcol3:
        st.markdown("""
        <div class="feature-pillar-card">
          <div style="font-size: 24px; margin-bottom: 8px;">💰</div>
          <h3 class="serif-heading" style="font-size: 1.15rem; margin: 0 0 6px 0;">全链路 FBA 履约测算</h3>
          <p style="font-size: 13px; color: #706B62; line-height: 1.5; margin: 0;">
            严谨计算长宽高体积重（抛重比）、海运 CBM、25% 关税与平台抽佣，得出真实的净利润率与安全红线。
          </p>
        </div>
        """, unsafe_allow_html=True)
