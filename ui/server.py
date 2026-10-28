from __future__ import annotations

import sys
import os
import json
import asyncio
import threading
from typing import Dict, Any, Optional

# Ensure project root and src/ are in sys.path
_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SRC_DIR = os.path.join(_ROOT_DIR, "src")
for _p in [_SRC_DIR, _ROOT_DIR]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

# Ensure UTF-8 on Windows
if sys.platform == "win32":
    try:
        if sys.stdout and hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if sys.stderr and hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse, StreamingResponse
from starlette.routing import Route

# Ensure local marked.min.js is loaded
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
MARKED_JS_FILE = os.path.join(STATIC_DIR, "marked.min.js")
MARKED_JS_SOURCE = ""
if os.path.exists(MARKED_JS_FILE):
    try:
        with open(MARKED_JS_FILE, "r", encoding="utf-8") as f:
            MARKED_JS_SOURCE = f.read()
    except Exception as e:
        print(f"Warning: could not read marked.min.js: {e}")

# Pre-compiled HTML with embedded Zero-Latency Tailwind and Native CSS
HTML_PAGE = """<!DOCTYPE html>
<html lang="zh-CN" class="h-full">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Deep Research · 跨境电商出海商业决策智能体</title>
  <!-- Google allowlisted Tailwind CSS -->
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <!-- MARKED_JS_INJECTION -->
  <!-- Instant Native Zero-Latency Styles (Zero Network Font Blocking, Zero White Screen) -->
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
    html, body {
      background-color: #FAF8F5 !important;
      color: #232220;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Inter", sans-serif;
      -webkit-font-smoothing: antialiased;
    }
    .font-serif-claude {
      font-family: "Charter", "Bitstream Charter", "Sitka Text", "Cambria", "Georgia", "Source Serif Pro", serif;
      letter-spacing: -0.02em;
    }
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #E0DDD4; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #C8C5BB; }
    
    @keyframes pulseSoft {
      0%, 100% { opacity: 0.35; transform: scale(0.9); }
      50% { opacity: 1; transform: scale(1.15); }
    }
    .pulse-dot {
      animation: pulseSoft 1.4s infinite;
    }

    /* Toast Animation */
    #toast {
      transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.25s ease;
    }

    /* Markdown Decision Memo Typography & GFM Tables */
    #report-markdown-content {
      color: #383531;
    }
    #report-markdown-content h1 {
      font-family: "Charter", "Bitstream Charter", "Sitka Text", Georgia, serif;
      font-size: 1.5rem;
      font-weight: 600;
      color: #232220;
      margin-top: 1.75rem;
      margin-bottom: 0.75rem;
      padding-bottom: 0.5rem;
      border-bottom: 1px solid #E8E5DD;
    }
    #report-markdown-content h2 {
      font-family: "Charter", "Bitstream Charter", "Sitka Text", Georgia, serif;
      font-size: 1.25rem;
      font-weight: 600;
      color: #232220;
      margin-top: 1.6rem;
      margin-bottom: 0.6rem;
      padding-bottom: 0.35rem;
      border-bottom: 1px solid #F0EDE5;
    }
    #report-markdown-content h3 {
      font-family: "Charter", "Bitstream Charter", "Sitka Text", Georgia, serif;
      font-size: 1.05rem;
      font-weight: 600;
      color: #232220;
      margin-top: 1.25rem;
      margin-bottom: 0.4rem;
    }
    #report-markdown-content h4 {
      font-size: 0.95rem;
      font-weight: 600;
      color: #232220;
      margin-top: 1rem;
      margin-bottom: 0.35rem;
    }
    #report-markdown-content p {
      margin-top: 0.6rem;
      margin-bottom: 0.6rem;
      line-height: 1.75;
      color: #4A4741;
    }
    #report-markdown-content strong {
      font-weight: 600;
      color: #1F1E1D;
    }
    #report-markdown-content hr {
      border: 0;
      height: 1px;
      background-color: #E8E5DD;
      margin: 1.5rem 0;
    }
    #report-markdown-content blockquote {
      border-left: 3px solid #C25E3E;
      background-color: #FDF9F6;
      padding: 0.75rem 1.1rem;
      margin: 1.1rem 0;
      border-radius: 0 0.6rem 0.6rem 0;
      color: #383531;
      border-top: 1px solid #F7ECE4;
      border-right: 1px solid #F7ECE4;
      border-bottom: 1px solid #F7ECE4;
      font-size: 0.875rem;
    }
    #report-markdown-content blockquote p {
      margin: 0;
      font-weight: 500;
    }
    #report-markdown-content table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 0.8125rem;
    }
    #report-markdown-content thead {
      background-color: #F8F6F1;
      border-bottom: 1px solid #E8E5DD;
    }
    #report-markdown-content th {
      font-weight: 600;
      color: #232220;
      padding: 0.65rem 0.85rem;
      border-bottom: 1px solid #E8E5DD;
      border-right: 1px solid #F0EDE5;
      white-space: nowrap;
    }
    #report-markdown-content th:last-child {
      border-right: none;
    }
    #report-markdown-content td {
      padding: 0.65rem 0.85rem;
      color: #4A4741;
      border-bottom: 1px solid #F0EDE5;
      border-right: 1px solid #F0EDE5;
      vertical-align: top;
      line-height: 1.55;
    }
    #report-markdown-content td:last-child {
      border-right: none;
    }
    #report-markdown-content tbody tr:last-child td {
      border-bottom: none;
    }
    #report-markdown-content tbody tr:nth-child(even) {
      background-color: #FAFAF7;
    }
    #report-markdown-content tbody tr:hover {
      background-color: #F5F1E8;
    }
    #report-markdown-content ul {
      list-style-type: disc;
      padding-left: 1.4rem;
      margin: 0.6rem 0;
    }
    #report-markdown-content ol {
      list-style-type: decimal;
      padding-left: 1.4rem;
      margin: 0.6rem 0;
    }
    #report-markdown-content li {
      margin: 0.25rem 0;
      color: #4A4741;
      line-height: 1.6;
    }
    #report-markdown-content code {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.85em;
      background-color: #F4F1EA;
      color: #C25E3E;
      padding: 0.15rem 0.35rem;
      border-radius: 0.25rem;
      border: 1px solid #E8E5DD;
    }
  </style>
</head>
<body class="bg-[#FAF8F5] text-[#232220] min-h-full flex flex-col p-4 sm:p-6 md:p-10">

  <!-- Toast Notification -->
  <div id="toast" class="fixed top-5 right-5 z-50 transform translate-y-[-20px] opacity-0 pointer-events-none bg-[#232220] text-white text-xs font-medium px-4 py-2.5 rounded-xl shadow-lg flex items-center gap-2">
    <span>✓</span>
    <span id="toast-msg">已复制到剪贴板</span>
  </div>

  <!-- Minimalist Top Navigation & Header -->
  <header class="max-w-5xl mx-auto w-full mb-8 pb-6 border-b border-[#E8E5DD] flex flex-col md:flex-row md:items-end justify-between gap-6">
    <div>
      <div class="inline-flex items-center gap-2 px-2.5 py-1 rounded-full text-xs font-medium bg-[#FBF3EE] text-[#C25E3E] border border-[#F0DFD5] mb-3">
        <span class="w-1.5 h-1.5 rounded-full bg-[#C25E3E]"></span>
        <span>Deep Research · Zero-Latency Native Engine</span>
        <span class="text-[#D4AFA0]">/</span>
        <span class="text-[#8A5B49] text-xs">LangGraph 状态图与跨模型热备</span>
      </div>
      <h1 class="font-serif-claude text-3xl sm:text-4xl text-[#232220] font-normal leading-tight">
        出海商业可行性深度调研
      </h1>
      <p class="text-sm text-[#6E695F] mt-1.5 max-w-xl leading-relaxed">
        面向跨境操盘手与出海投资人。输入目标细分品类或亚马逊 ASIN，自主完成战略拆解、标杆竞品透视、买家 VOC 逆向与 FBA 履约全成本测算。
      </p>
    </div>

    <!-- Live Status Pill & Benchmark Quick Demo -->
    <div class="flex flex-col sm:flex-row items-start sm:items-center gap-2">
      <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-[#EEF4F1] text-[#2F634E] border border-[#C8DBD1]">
        <span class="w-2 h-2 rounded-full bg-[#2F634E]"></span>
        <span id="engine-status">系统就绪 · 毫秒级直出</span>
      </span>
      <button onclick="loadSampleDemo('headphone')" class="px-2.5 py-1 rounded-full text-xs font-medium bg-white text-[#706B62] border border-[#E8E5DD] hover:border-[#C25E3E] hover:text-[#C25E3E] transition-all">
        ⚡ 快速体验样品数据
      </button>
    </div>
  </header>

  <!-- Main Stage -->
  <main class="max-w-5xl mx-auto w-full flex-1 flex flex-col gap-7">

    <!-- 1. Hero Command Bar & Search Card -->
    <section class="bg-white rounded-2xl border border-[#E8E5DD] p-5 sm:p-7 shadow-sm">
      <form id="research-form" onsubmit="handleFormSubmit(event)" class="space-y-4">
        <!-- Input & Submit Row -->
        <div class="flex flex-col sm:flex-row gap-3">
          <div class="relative flex-1">
            <input 
              type="text" 
              id="niche-input" 
              value="B0BS1QCFHX"
              placeholder="输入细分品类 (如 Portable Camping Espresso Maker) 或亚马逊 ASIN (如 B0BS1QCFHX)..."
              class="w-full bg-[#FAF8F5] border border-[#E8E5DD] focus:border-[#C25E3E] focus:bg-white rounded-xl px-4 py-3 text-sm text-[#232220] outline-none transition-all"
              required
            />
          </div>
          <button 
            type="submit" 
            id="submit-btn"
            class="bg-[#C25E3E] hover:bg-[#AA4E31] text-white font-medium px-6 py-3 rounded-xl text-sm transition-all shadow-sm flex items-center justify-center gap-2 whitespace-nowrap active:scale-[0.99]"
          >
            <span id="btn-icon">🚀</span>
            <span id="btn-text">启动深度调研</span>
          </button>
        </div>

        <!-- Quick Presets Row -->
        <div class="flex flex-wrap items-center gap-2 pt-1 text-xs text-[#8C877D]">
          <span class="font-medium">推荐标杆案例：</span>
          <button type="button" onclick="setPreset('B0BS1QCFHX')" class="px-2.5 py-1 rounded-lg border border-[#E8E5DD] bg-[#FAF8F5] hover:border-[#C25E3E] hover:text-[#C25E3E] hover:bg-[#FBF3EE] text-[#5C5851] transition-all">
            🎧 索尼降噪耳机 (B0BS1QCFHX)
          </button>
          <button type="button" onclick="setPreset('Portable Camping Espresso Maker')" class="px-2.5 py-1 rounded-lg border border-[#E8E5DD] bg-[#FAF8F5] hover:border-[#C25E3E] hover:text-[#C25E3E] hover:bg-[#FBF3EE] text-[#5C5851] transition-all">
            ☕ 便携浓缩咖啡机
          </button>
          <button type="button" onclick="setPreset('Ergonomic Mesh Office Chair')" class="px-2.5 py-1 rounded-lg border border-[#E8E5DD] bg-[#FAF8F5] hover:border-[#C25E3E] hover:text-[#C25E3E] hover:bg-[#FBF3EE] text-[#5C5851] transition-all">
            🪑 人体工学网椅 (大件抛货)
          </button>
        </div>

        <!-- Advanced Engine Settings Toggle -->
        <div class="pt-2 border-t border-[#F2EFE8]">
          <details class="text-xs text-[#706B62] group">
            <summary class="cursor-pointer font-medium hover:text-[#232220] inline-flex items-center gap-1.5 select-none">
              <span>⚙️ 站点与模型底座设置</span>
              <span class="text-[#8C877D] text-[10px] group-open:rotate-180 transition-transform">▼</span>
            </summary>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-3 pt-3 border-t border-[#F2EFE8]">
              <div>
                <label class="block font-semibold mb-1 text-[#5C5851]">目标出海站点：</label>
                <select id="market-select" class="w-full bg-[#FAF8F5] border border-[#E8E5DD] rounded-lg px-3 py-2 text-xs text-[#232220] outline-none">
                  <option value="US" selected>🇺🇸 US (美国站)</option>
                  <option value="UK">🇬🇧 UK (英国站)</option>
                  <option value="DE">🇩🇪 DE (德国站)</option>
                  <option value="JP">🇯🇵 JP (日本站)</option>
                </select>
              </div>
              <div>
                <label class="block font-semibold mb-1 text-[#5C5851]">主驱动推理大模型：</label>
                <select id="model-select" class="w-full bg-[#FAF8F5] border border-[#E8E5DD] rounded-lg px-3 py-2 text-xs text-[#232220] outline-none">
                  <option value="groq:openai/gpt-oss-120b" selected>⚡ Groq · GPT-OSS 120B (毫秒级 · 深度推理长文 · 推荐)</option>
                  <option value="groq:openai/gpt-oss-20b">⚡ Groq · GPT-OSS 20B (极速 ~500ms · 轻量速推)</option>
                  <option value="groq:qwen/qwen3.8-27b">⚡ Groq · Qwen 3.8 27B (开源通用基座)</option>
                  <option value="nvidia:nemotron">🧠 NVIDIA NIM · Nemotron 550B (旗舰超大底座)</option>
                </select>
              </div>
            </div>
          </details>
        </div>
      </form>
    </section>

    <!-- 2. Live StateGraph Stepper Card (Appears/Updates when running) -->
    <section id="stepper-section" class="bg-white rounded-2xl border border-[#E8E5DD] p-5 sm:p-6 shadow-sm hidden">
      <div class="flex items-center justify-between mb-3 pb-3 border-b border-[#F2EFE8]">
        <div class="flex items-center gap-2">
          <span class="text-sm font-semibold text-[#232220] flex items-center gap-1.5">
            <svg class="w-4 h-4 text-[#C25E3E]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
            智能体实时状态流转监视器 (Live StateGraph Stepper)
          </span>
          <span id="stepper-model-tag" class="text-xs px-2 py-0.5 rounded bg-[#FAF8F5] border border-[#E8E5DD] text-[#706B62]">
            Groq LPU 极速流转中
          </span>
        </div>
        <div id="stepper-status-badge" class="text-xs font-medium text-[#C25E3E] flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-[#C25E3E] pulse-dot"></span>
          <span>执行中...</span>
        </div>
      </div>

      <!-- Progress Bar -->
      <div class="w-full bg-[#F2EFE8] h-1.5 rounded-full overflow-hidden mb-4">
        <div id="progress-bar-fill" class="h-full bg-gradient-to-r from-[#C25E3E] to-[#DE8A36] transition-all duration-300" style="width: 5%;"></div>
      </div>

      <!-- 4 Horizontal Stepper Nodes -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5">
        <!-- Node 1: Planner -->
        <div id="step-1" class="rounded-xl border p-3.5 bg-white border-[#E8E5DD] opacity-60 transition-all">
          <div class="flex items-center justify-between mb-1.5">
            <span class="text-xs font-semibold text-[#232220]">1. Planner 规划</span>
            <span id="step-1-badge" class="text-xs px-1.5 py-0.5 rounded-full bg-[#EDEAE3] text-[#706B62] font-semibold">待机</span>
          </div>
          <div id="step-1-desc" class="text-xs text-[#6E695F] leading-relaxed">
            等待拆解调研路径与意图...
          </div>
        </div>

        <!-- Node 2: Researcher -->
        <div id="step-2" class="rounded-xl border p-3.5 bg-white border-[#E8E5DD] opacity-60 transition-all">
          <div class="flex items-center justify-between mb-1.5">
            <span class="text-xs font-semibold text-[#232220]">2. Researcher 采集</span>
            <span id="step-2-badge" class="text-xs px-1.5 py-0.5 rounded-full bg-[#EDEAE3] text-[#706B62] font-semibold">待机</span>
          </div>
          <div id="step-2-desc" class="text-xs text-[#6E695F] leading-relaxed">
            等待调度出海工具链...
          </div>
        </div>

        <!-- Node 3: Critic -->
        <div id="step-3" class="rounded-xl border p-3.5 bg-white border-[#E8E5DD] opacity-60 transition-all">
          <div class="flex items-center justify-between mb-1.5">
            <span class="text-xs font-semibold text-[#232220]">3. Critic 质检反思</span>
            <span id="step-3-badge" class="text-xs px-1.5 py-0.5 rounded-full bg-[#EDEAE3] text-[#706B62] font-semibold">待机</span>
          </div>
          <div id="step-3-desc" class="text-xs text-[#6E695F] leading-relaxed">
            等待审查数据与毛利红线...
          </div>
        </div>

        <!-- Node 4: Synthesizer -->
        <div id="step-4" class="rounded-xl border p-3.5 bg-white border-[#E8E5DD] opacity-60 transition-all">
          <div class="flex items-center justify-between mb-1.5">
            <span class="text-xs font-semibold text-[#232220]">4. Synthesizer 合成</span>
            <span id="step-4-badge" class="text-xs px-1.5 py-0.5 rounded-full bg-[#EDEAE3] text-[#706B62] font-semibold">待机</span>
          </div>
          <div id="step-4-desc" class="text-xs text-[#6E695F] leading-relaxed">
            等待综合生成立项报告...
          </div>
        </div>
      </div>

      <!-- Real-time Agent Log Expander -->
      <div class="mt-4 pt-3 border-t border-[#F2EFE8]">
        <details class="text-xs text-[#706B62]">
          <summary class="cursor-pointer font-medium hover:text-[#232220]">
            🔍 查看实时执行细节流 (Live Agent Updates)
          </summary>
          <div id="agent-log-container" class="mt-2.5 p-3 rounded-lg bg-[#FAF8F5] border border-[#E8E5DD] font-mono text-[11px] leading-relaxed max-h-48 overflow-y-auto space-y-1 text-[#4A4741]">
            <div class="text-[#8C877D]">[Init] 正在准备 LangGraph 状态图工作流...</div>
          </div>
        </details>
      </div>
    </section>

    <!-- 3. Pre-Search Showcase: 3 Value Pillars (Visible before running) -->
    <section id="showcase-section" class="grid grid-cols-1 md:grid-cols-3 gap-5">
      <div class="bg-white rounded-2xl border border-[#E8E5DD] p-6 shadow-sm">
        <div class="w-10 h-10 rounded-xl bg-[#FBF3EE] text-[#C25E3E] flex items-center justify-center text-xl mb-3.5">
          🎯
        </div>
        <h3 class="font-serif-claude text-lg text-[#232220] font-medium mb-1.5">精准标杆锚定</h3>
        <p class="text-xs text-[#6E695F] leading-relaxed">
          支持输入 ASIN 逆向解析真实类目、品牌与价格带，杜绝跨品类漂移，精准挖掘 Top 标杆竞品。
        </p>
      </div>

      <div class="bg-white rounded-2xl border border-[#E8E5DD] p-6 shadow-sm">
        <div class="w-10 h-10 rounded-xl bg-[#FBF3EE] text-[#C25E3E] flex items-center justify-center text-xl mb-3.5">
          ⚠️
        </div>
        <h3 class="font-serif-claude text-lg text-[#232220] font-medium mb-1.5">VOC 差评逆向工程</h3>
        <p class="text-xs text-[#6E695F] leading-relaxed">
          聚焦 1~3 星高频质量与体验故障，直接提炼可落地交付给 1688 / 模具工厂的结构与材料改良对策。
        </p>
      </div>

      <div class="bg-white rounded-2xl border border-[#E8E5DD] p-6 shadow-sm">
        <div class="w-10 h-10 rounded-xl bg-[#FBF3EE] text-[#C25E3E] flex items-center justify-center text-xl mb-3.5">
          💰
        </div>
        <h3 class="font-serif-claude text-lg text-[#232220] font-medium mb-1.5">全链路 FBA 履约测算</h3>
        <p class="text-xs text-[#6E695F] leading-relaxed">
          严谨计算长宽高体积重（抛重比）、海运 CBM、25% 关税与平台抽佣，得出真实的净利润率与安全红线。
        </p>
      </div>
    </section>

    <!-- 4. Results Dossier Container (Revealed upon completion) -->
    <div id="results-container" class="space-y-6 hidden">
      <!-- Recognition Banner -->
      <div id="asin-banner" class="bg-[#FDF5F1] border border-[#F0D9CE] rounded-xl p-4 flex items-center gap-3">
        <span class="text-2xl">🎯</span>
        <div>
          <div id="asin-banner-title" class="text-sm font-semibold text-[#232220]">标杆竞品锚定成功</div>
          <div id="asin-banner-sub" class="text-xs text-[#6E695F]">正在匹配同类竞争矩阵...</div>
        </div>
      </div>

      <!-- 4 Key Metrics KPI Row -->
      <section class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="bg-white rounded-2xl border border-[#E8E5DD] p-5 shadow-sm">
          <span class="text-xs uppercase tracking-wider font-semibold text-[#8C877D] block mb-1">商业可行性评级</span>
          <div id="metric-rating" class="font-serif-claude text-3xl text-[#232220]">Healthy</div>
          <span id="metric-rating-sub" class="text-xs text-[#2F634E] mt-1 inline-block">● 推荐谨慎立项打样</span>
        </div>

        <div class="bg-white rounded-2xl border border-[#E8E5DD] p-5 shadow-sm">
          <span class="text-xs uppercase tracking-wider font-semibold text-[#8C877D] block mb-1">预估销售净利率</span>
          <div id="metric-margin" class="font-serif-claude text-3xl text-[#C25E3E]">24.6%</div>
          <span class="text-xs text-[#706B62] mt-1 inline-block">全口径扣除 (含关税/ACOS)</span>
        </div>

        <div class="bg-white rounded-2xl border border-[#E8E5DD] p-5 shadow-sm">
          <span class="text-xs uppercase tracking-wider font-semibold text-[#8C877D] block mb-1">单台预估纯利润</span>
          <div id="metric-profit" class="font-serif-claude text-3xl text-[#232220]">$14.76</div>
          <span class="text-xs text-[#706B62] mt-1 inline-block">单台纯利净额</span>
        </div>

        <div class="bg-white rounded-2xl border border-[#E8E5DD] p-5 shadow-sm">
          <span class="text-xs uppercase tracking-wider font-semibold text-[#8C877D] block mb-1">FBA 尺寸分段</span>
          <div id="metric-fba" class="font-serif-claude text-2xl text-[#232220]">Large standard</div>
          <span id="metric-fba-fee" class="text-xs text-[#706B62] mt-1 inline-block">配送费: $5.26 /件</span>
        </div>
      </section>

      <!-- 4 Tabs Dossier -->
      <section class="bg-white rounded-2xl border border-[#E8E5DD] shadow-sm overflow-hidden flex flex-col">
        <!-- Tabs Header -->
        <div class="flex items-center px-6 pt-4 border-b border-[#E8E5DD] gap-6 overflow-x-auto bg-[#FCFBF8]">
          <button onclick="switchTab('report')" id="tab-btn-report" class="tab-btn pb-3 text-sm font-medium border-b-2 border-[#C25E3E] text-[#C25E3E] transition-all whitespace-nowrap">
            📑 决策立项执行备忘录
          </button>
          <button onclick="switchTab('competitors')" id="tab-btn-competitors" class="tab-btn pb-3 text-sm font-medium border-b-2 border-transparent text-[#706B62] hover:text-[#232220] transition-all whitespace-nowrap">
            🏆 同类标杆竞品透视矩阵
          </button>
          <button onclick="switchTab('voc')" id="tab-btn-voc" class="tab-btn pb-3 text-sm font-medium border-b-2 border-transparent text-[#706B62] hover:text-[#232220] transition-all whitespace-nowrap">
            ⚠️ 买家负评 VOC 逆向工程 (模具方案)
          </button>
          <button onclick="switchTab('calculator')" id="tab-btn-calculator" class="tab-btn pb-3 text-sm font-medium border-b-2 border-transparent text-[#706B62] hover:text-[#232220] transition-all whitespace-nowrap">
            💰 动态 FBA 抛重与毛利模拟器
          </button>
        </div>

        <!-- Tab 1: Executive Report -->
        <div id="tab-pane-report" class="p-6 md:p-8 flex flex-col gap-6">
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 pb-4 border-b border-[#F2EFE8]">
            <div>
              <h2 id="report-title" class="font-serif-claude text-2xl text-[#232220]">
                《出海商业可行性深度决策报告》
              </h2>
              <p class="text-xs text-[#706B62] mt-1">立项裁决：根据财务模型与买家差评深度综合判定。</p>
            </div>
            <div class="flex items-center gap-2">
              <button onclick="copyMarkdownReport()" class="px-3 py-1.5 rounded-lg text-xs font-medium border border-[#E8E5DD] bg-[#FAF8F5] hover:bg-[#F2EFE8] text-[#232220] transition-all flex items-center gap-1.5">
                <svg class="w-3.5 h-3.5 text-[#706B62]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/></svg>
                复制 Markdown
              </button>
              <button onclick="downloadMarkdownReport()" class="px-3 py-1.5 rounded-lg text-xs font-medium bg-[#C25E3E] hover:bg-[#AA4E31] text-white transition-all flex items-center gap-1.5">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
                下载报告 (.md)
              </button>
            </div>
          </div>

          <div id="report-markdown-content" class="text-sm text-[#4A4741] space-y-4 leading-relaxed font-sans">
            <!-- Dynamically populated via renderMarkdown() -->
          </div>
        </div>

        <!-- Tab 2: Competitors Table -->
        <div id="tab-pane-competitors" class="p-6 md:p-8 hidden">
          <h3 class="font-serif-claude text-xl text-[#232220] mb-4">核心对标竞品透视矩阵</h3>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs border-collapse">
              <thead>
                <tr class="border-b border-[#E8E5DD] bg-[#FCFBF8] text-[#706B62]">
                  <th class="py-3 px-4 font-semibold">品牌</th>
                  <th class="py-3 px-4 font-semibold">对标产品标题</th>
                  <th class="py-3 px-4 font-semibold">售价</th>
                  <th class="py-3 px-4 font-semibold">评分 / 评论数</th>
                  <th class="py-3 px-4 font-semibold">BSR 排名</th>
                  <th class="py-3 px-4 font-semibold">预估月销</th>
                </tr>
              </thead>
              <tbody id="competitors-tbody" class="divide-y divide-[#F2EFE8]"></tbody>
            </table>
          </div>
        </div>

        <!-- Tab 3: VOC Defects -->
        <div id="tab-pane-voc" class="p-6 md:p-8 hidden">
          <h3 class="font-serif-claude text-xl text-[#232220] mb-1">买家声音 (VOC) 差评聚类与模具改造方案</h3>
          <p class="text-xs text-[#706B62] mb-5">针对 1~3 星差评高频失效场景逆向提炼，可直接交付给 OEM / 模具工厂开模改良。</p>
          <div id="voc-cards-container" class="grid grid-cols-1 md:grid-cols-3 gap-4"></div>
        </div>

        <!-- Tab 4: Landed Cost & Profit Simulator -->
        <div id="tab-pane-calculator" class="p-6 md:p-8 hidden">
          <div class="flex flex-col md:flex-row gap-8">
            <!-- Left Sliders -->
            <div class="w-full md:w-1/2 space-y-5 bg-[#FCFBF8] p-5 rounded-xl border border-[#E8E5DD]">
              <h4 class="font-serif-claude text-lg text-[#232220] border-b border-[#E8E5DD] pb-2">
                参数交互式模拟微调
              </h4>

              <div>
                <div class="flex justify-between text-xs mb-1 font-medium">
                  <span>亚马逊目标零售售价 (USD):</span>
                  <span id="slider-retail-val" class="text-[#C25E3E] font-semibold">$59.99</span>
                </div>
                <input type="range" id="slider-retail" min="15" max="200" step="1" value="59.99" oninput="recalcCost()" class="w-full accent-[#C25E3E]">
              </div>

              <div>
                <div class="flex justify-between text-xs mb-1 font-medium">
                  <span>工厂出厂采购价 (RMB 1688):</span>
                  <span id="slider-sourcing-val" class="text-[#C25E3E] font-semibold">¥75.0</span>
                </div>
                <input type="range" id="slider-sourcing" min="15" max="350" step="1" value="75" oninput="recalcCost()" class="w-full accent-[#C25E3E]">
              </div>

              <div>
                <div class="flex justify-between text-xs mb-1 font-medium">
                  <span>预估广告 ACOS (%):</span>
                  <span id="slider-acos-val" class="text-[#C25E3E] font-semibold">16%</span>
                </div>
                <input type="range" id="slider-acos" min="5" max="35" step="1" value="16" oninput="recalcCost()" class="w-full accent-[#C25E3E]">
              </div>

              <div>
                <div class="flex justify-between text-xs mb-1 font-medium">
                  <span>海运每立方运费 (USD / CBM):</span>
                  <span id="slider-cbm-val" class="text-[#C25E3E] font-semibold">$180</span>
                </div>
                <input type="range" id="slider-cbm" min="80" max="350" step="10" value="180" oninput="recalcCost()" class="w-full accent-[#C25E3E]">
              </div>
            </div>

            <!-- Right Live Output Breakdown -->
            <div class="w-full md:w-1/2 flex flex-col justify-between">
              <div>
                <h4 class="font-serif-claude text-lg text-[#232220] mb-4">实时测算全口径单件利润拆解</h4>
                
                <div class="space-y-2.5 text-xs">
                  <div class="flex justify-between py-1.5 border-b border-[#F2EFE8]">
                    <span class="text-[#706B62]">单件出厂采购成本 (USD):</span>
                    <span id="calc-sourcing" class="font-medium text-[#232220]">$10.42</span>
                  </div>
                  <div class="flex justify-between py-1.5 border-b border-[#F2EFE8]">
                    <span class="text-[#706B62]">头程海运拼箱运费:</span>
                    <span id="calc-freight" class="font-medium text-[#232220]">$0.78</span>
                  </div>
                  <div class="flex justify-between py-1.5 border-b border-[#F2EFE8]">
                    <span class="text-[#706B62]">美国 Section 301 关税 (25%):</span>
                    <span id="calc-tariff" class="font-medium text-[#232220]">$2.60</span>
                  </div>
                  <div class="flex justify-between py-1.5 border-b border-[#F2EFE8]">
                    <span class="text-[#706B62]">亚马逊 FBA 配送费:</span>
                    <span id="calc-fba" class="font-medium text-[#232220]">$5.26</span>
                  </div>
                  <div class="flex justify-between py-1.5 border-b border-[#F2EFE8]">
                    <span class="text-[#706B62]">平台销售佣金 (15%):</span>
                    <span id="calc-commission" class="font-medium text-[#232220]">$9.00</span>
                  </div>
                  <div class="flex justify-between py-1.5 border-b border-[#F2EFE8]">
                    <span class="text-[#706B62]">广告与退货损耗津贴:</span>
                    <span id="calc-ad" class="font-medium text-[#232220]">$11.40</span>
                  </div>
                </div>
              </div>

              <!-- Total Bottom Bar -->
              <div class="mt-6 pt-4 border-t-2 border-[#E8E5DD] flex justify-between items-center bg-[#FAF8F5] p-4 rounded-xl">
                <div>
                  <span class="text-xs uppercase tracking-wide text-[#706B62] font-semibold">预测纯净利润率</span>
                  <div id="calc-margin-big" class="font-serif-claude text-3xl font-medium text-[#C25E3E]">24.6%</div>
                </div>
                <div class="text-right">
                  <span class="text-xs uppercase tracking-wide text-[#706B62] font-semibold">单件纯净利</span>
                  <div id="calc-profit-big" class="font-serif-claude text-3xl font-medium text-[#232220]">$14.76</div>
                </div>
              </div>

            </div>
          </div>
        </div>
      </section>
    </div>

  </main>

  <footer class="max-w-5xl mx-auto w-full mt-12 pt-6 border-t border-[#E8E5DD] text-center text-xs text-[#8C877D]">
    Deep Research · 跨境电商商业决策智能体 &nbsp;|&nbsp; 纯原生零延迟响应引擎
  </footer>

  <!-- Frontend Client Logic -->
  <script>
    let currentRawReport = "";
    let currentFinalState = null;
    let activeEventSource = null;

    // Pre-curated Demo Cases for instant zero-waiting preview
    const PRESET_DEMO_DATA = {
      headphone: {
        niche_query: "B0BS1QCFHX",
        target_market: "US",
        resolved_product: { is_asin: true, asin: "B0BS1QCFHX", title: "Sony WH-CH720N Wireless Noise Canceling Headphones", brand: "Sony" },
        financial_model: { viability_rating: "Healthy", net_margin_percentage: 24.6, net_profit_usd: 14.76, fba_tier: "Large standard-size", fba_fulfillment_fee_usd: 5.26, retail_price_usd: 59.99, sourcing_cost_usd: 10.42 },
        competitors: [
          { brand: "Sony", title: "WH-CH720N Wireless Noise Canceling Headphones", price_usd: 59.99, rating: 4.4, reviews_count: 8920, bsr_rank: 142, estimated_monthly_sales: 8500 },
          { brand: "Soundcore", title: "Anker Life Q30 Hybrid Active Noise Cancelling", price_usd: 79.99, rating: 4.5, reviews_count: 18400, bsr_rank: 88, estimated_monthly_sales: 12000 },
          { brand: "JBL", title: "Tune 760NC Lightweight Foldable Over-Ear", price_usd: 64.95, rating: 4.3, reviews_count: 5210, bsr_rank: 215, estimated_monthly_sales: 5300 },
          { brand: "1MORE", title: "SonoFlow Active Noise Cancelling Headphones", price_usd: 49.99, rating: 4.4, reviews_count: 3410, bsr_rank: 380, estimated_monthly_sales: 3800 }
        ],
        voc_defects: [
          { component: "头梁转轴伸缩处 (Hinge)", defect_description: "正常佩戴 3-6 个月折痕处塑料疲劳脆断", customer_quote: "The plastic around the headband snapped after just 4 months of normal office use.", severity: "High", frequency_percent: 42.0, factory_countermeasure: "工厂模具改良：内部注塑骨架必须嵌入 0.8mm 65Mn 弹簧钢补强片，卡扣处改用锌合金冲压。" },
          { component: "前馈麦克风腔体 (ANC Mic)", defect_description: "户外刮风或跑步时底噪啸叫严重", customer_quote: "ANC works fine indoors, but outside any gust of wind creates a loud screeching wind noise.", severity: "Medium", frequency_percent: 28.0, factory_countermeasure: "声学腔体改良：在开孔前馈麦克风外部增设高密度防风透气阻尼网与硅胶减震密封圈。" },
          { component: "蛋白皮耳罩 (Earpads)", defect_description: "夏天闷热不透气，且 1 年后表层人造革水解脱落", customer_quote: "Sweaty after 45 minutes, and fake leather started peeling all over my ears.", severity: "Low", frequency_percent: 18.0, factory_countermeasure: "材料改良：接触皮肤面升级为蜂窝状冰丝凉感网布，侧边保留隔音皮，并设计可快速卡扣拆卸清洗。" }
        ],
        final_report: `# 《索尼 WH-CH720N 同类标杆出海商业可行性深度决策报告》\n\n品类: Wireless Active Noise Canceling Headphones (无线主动降噪头戴耳机) | 目标市场: 美国 (Amazon.com)\n\n---\n\n## 1️⃣ 执行摘要与立项裁决 (Executive Summary & Verdict)\n\n| 评估维度 | 核心量化结论 | 战略指导意见 |\n|:---|:---|:---|\n| **目标客群** | 远程办公白领 + 学生通勤族 | 对长时间佩戴压迫感与低频降噪敏感，极易因断梁退货 |\n| **市场体量** | 年销约 $1.8B，CAGR 14.2% | $50-$80 属于放量黄金带，头部被索尼/Anker占据 |\n| **核心矛盾** | 降噪算法 vs 塑胶用料脆断 | 索尼原装为降低机重牺牲了伸缩头梁韧性，买家怨声载道 |\n| **财务模型** | 采购 $10.42 / FBA $5.26 | 落地成本 $14.18，净利率 24.6%，单台净利 $14.76 |\n| **立项建议** | **立项通过 (Greenlight)** | 避开 $150+ 高端红海，卡位 $59.99 做结构加固升级版 |\n\n> Verdict: ✅ 批准立项。优先攻关“弹簧钢内嵌头梁模具”与“凉感耳罩面料”，Q3 前入仓锁定旺季流量。\n\n---\n\n## 2️⃣ 标杆竞品透视矩阵 (Competitor Matrix)\n\n| 排名 | 品牌 / 型号 | 价格 (USD) | 评分 / 评价数 | BSR 排名 | 预估月销 | 核心卖点 | 致命痛点 |\n|:---|:---|:---|:---|:---|:---|:---|:---|\n| **#1** | Sony WH-CH720N | $59.99 | 4.4 (8,920) | #142 | 8,500 件 | V1 降噪芯片、超轻 192g | 转轴易断、无收纳盒 |\n| **#2** | Soundcore Q30 | $79.99 | 4.5 (18,400) | #88 | 12,000 件 | 三模降噪、APP 调音 | 耳罩夏天发闷脱皮 |\n| **#3** | JBL Tune 760NC | $64.95 | 4.3 (5,210) | #215 | 5,300 件 | PureBass 纯正低音 | 夹头感强、头顶压痛 |\n\n---\n\n## 3️⃣ 买家声音 (VOC) 逆向工程与工厂改模建议\n\n- **头梁转轴伸缩处 (Hinge)**: 42% 差评集中在“正常佩戴 3-6 个月折痕处塑料疲劳脆断”。工厂模具必须在注塑骨架内嵌入 0.8mm 65Mn 弹簧钢补强片，卡扣改用锌合金冲压。\n- **前馈降噪麦克风 (ANC Mic)**: 28% 差评集中在“户外刮风时风噪剧烈啸叫”。在麦克风拾音开孔处加装高密度防风透气阻尼网与硅胶密封圈。\n- **蛋白皮耳罩 (Earpads)**: 18% 差评集中在“佩戴 45 分钟出汗发闷”。接触面升级为蜂窝状冰丝凉感网布，并采用可快拆卡扣结构。`
      }
    };

    function showToast(msg) {
      const toast = document.getElementById('toast');
      document.getElementById('toast-msg').textContent = msg;
      toast.classList.remove('opacity-0', 'translate-y-[-20px]', 'pointer-events-none');
      toast.classList.add('opacity-100', 'translate-y-0');
      setTimeout(() => {
        toast.classList.remove('opacity-100', 'translate-y-0');
        toast.classList.add('opacity-0', 'translate-y-[-20px]', 'pointer-events-none');
      }, 2200);
    }

    function setPreset(query) {
      document.getElementById('niche-input').value = query;
    }

    function loadSampleDemo(key) {
      const demo = PRESET_DEMO_DATA[key];
      if (!demo) return;
      document.getElementById('niche-input').value = demo.niche_query;
      document.getElementById('showcase-section').classList.add('hidden');
      renderResults(demo);
      showToast("已成功加载标杆案例完整数据！");
    }

    function appendAgentLog(text) {
      const logContainer = document.getElementById('agent-log-container');
      const row = document.createElement('div');
      row.textContent = text;
      logContainer.appendChild(row);
      logContainer.scrollTop = logContainer.scrollHeight;
    }

    function setNodeStatus(stepNum, status, text) {
      const nodeEl = document.getElementById(`step-${stepNum}`);
      const badgeEl = document.getElementById(`step-${stepNum}-badge`);
      const descEl = document.getElementById(`step-${stepNum}-desc`);

      if (status === 'active') {
        nodeEl.className = "rounded-xl border p-3.5 bg-[#FDF5F1] border-[#C25E3E] opacity-100 shadow-sm transition-all";
        badgeEl.className = "text-xs px-1.5 py-0.5 rounded-full bg-[#F8E2D8] text-[#C25E3E] font-semibold flex items-center gap-1";
        badgeEl.innerHTML = '<span class="w-1.5 h-1.5 rounded-full bg-[#C25E3E] pulse-dot"></span> 执行中';
      } else if (status === 'completed') {
        nodeEl.className = "rounded-xl border p-3.5 bg-[#EEF4F1] border-[#C8DBD1] opacity-100 transition-all";
        badgeEl.className = "text-xs px-1.5 py-0.5 rounded-full bg-[#DDEBE3] text-[#2F634E] font-semibold";
        badgeEl.textContent = '✓ 完成';
      } else {
        nodeEl.className = "rounded-xl border p-3.5 bg-white border-[#E8E5DD] opacity-60 transition-all";
        badgeEl.className = "text-xs px-1.5 py-0.5 rounded-full bg-[#EDEAE3] text-[#706B62] font-semibold";
        badgeEl.textContent = '待机';
      }
      if (text) descEl.textContent = text;
    }

    function fallbackMarkdownParser(md) {
      const lines = md.split('\\n');
      let result = [];
      let inTable = false;
      let tableRows = [];
      let inList = false;

      function flushList() {
        if (inList) {
          result.push('</ul>');
          inList = false;
        }
      }

      function flushTable() {
        if (inTable && tableRows.length > 0) {
          let html = '<div class="overflow-x-auto my-4 rounded-xl border border-[#E8E5DD] shadow-xs"><table class="min-w-full text-xs border-collapse">';
          if (tableRows.length >= 2 && tableRows[1].some(c => /^-+$/.test(c.trim()))) {
            html += '<thead class="bg-[#F8F6F1] border-b border-[#E8E5DD]"><tr>';
            tableRows[0].forEach(cell => {
              html += `<th class="py-3 px-3.5 font-semibold text-[#232220] border-r border-[#F0EDE5] last:border-none">${formatInline(cell)}</th>`;
            });
            html += '</tr></thead><tbody class="divide-y divide-[#F0EDE5]">';
            for (let i = 2; i < tableRows.length; i++) {
              let row = tableRows[i];
              let bg = (i % 2 === 0) ? 'bg-[#FAFAF7]' : 'bg-white';
              html += `<tr class="${bg} hover:bg-[#F5F1E8] transition-colors">`;
              row.forEach(cell => {
                html += `<td class="py-2.5 px-3.5 text-[#4A4741] border-r border-[#F0EDE5] last:border-none align-top">${formatInline(cell)}</td>`;
              });
              html += '</tr>';
            }
            html += '</tbody>';
          } else {
            html += '<tbody>';
            tableRows.forEach((row, i) => {
              let bg = (i % 2 === 0) ? 'bg-[#FAFAF7]' : 'bg-white';
              html += `<tr class="${bg}">`;
              row.forEach(cell => {
                html += `<td class="py-2.5 px-3.5 text-[#4A4741] border-r border-[#F0EDE5] last:border-none align-top">${formatInline(cell)}</td>`;
              });
              html += '</tr>';
            });
            html += '</tbody>';
          }
          html += '</table></div>';
          result.push(html);
          tableRows = [];
          inTable = false;
        }
      }

      function formatInline(text) {
        if (!text) return '';
        let s = text.trim();
        s = s.replace(/\\*\\*(.*?)\\*\\*/g, '<strong class="font-semibold text-[#232220]">$1</strong>');
        s = s.replace(/\\*(.*?)\\*/g, '<em class="italic text-[#706B62]">$1</em>');
        s = s.replace(/`([^`]+)`/g, '<code class="bg-[#F4F1EA] text-[#C25E3E] px-1 py-0.5 rounded text-xs border border-[#E8E5DD]">$1</code>');
        return s;
      }

      for (let i = 0; i < lines.length; i++) {
        let line = lines[i];
        let trimmed = line.trim();

        if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
          flushList();
          inTable = true;
          let cells = trimmed.split('|').slice(1, -1).map(c => c.trim());
          tableRows.push(cells);
          continue;
        } else if (inTable) {
          flushTable();
        }

        if (/^(\\-{3,}|\\*{3,}|_{3,})$/.test(trimmed)) {
          flushList();
          result.push('<hr class="my-6 border-0 border-t border-[#E8E5DD]" />');
          continue;
        }

        if (trimmed.startsWith('### ')) {
          flushList();
          result.push(`<h4 class="font-serif-claude text-base font-semibold text-[#232220] mt-5 mb-2">${formatInline(trimmed.slice(4))}</h4>`);
          continue;
        }
        if (trimmed.startsWith('## ')) {
          flushList();
          result.push(`<h3 class="font-serif-claude text-lg font-semibold text-[#232220] mt-6 mb-3 pb-1 border-b border-[#F0EDE5]">${formatInline(trimmed.slice(3))}</h3>`);
          continue;
        }
        if (trimmed.startsWith('# ')) {
          flushList();
          result.push(`<h2 class="font-serif-claude text-xl font-semibold text-[#232220] mt-7 mb-4 pb-2 border-b border-[#E8E5DD]">${formatInline(trimmed.slice(2))}</h2>`);
          continue;
        }

        if (trimmed.startsWith('>') || trimmed.startsWith('&gt;')) {
          flushList();
          let quoteText = trimmed.replace(/^(&gt;|>)\\s*/, '');
          result.push(`<blockquote class="border-l-4 border-[#C25E3E] bg-[#FDF9F6] px-4 py-3 my-4 rounded-r-xl text-sm font-medium text-[#232220] border-y border-r border-[#F7ECE4]">${formatInline(quoteText)}</blockquote>`);
          continue;
        }

        if (/^[-*]\\s+/.test(trimmed)) {
          if (!inList) {
            result.push('<ul class="list-disc pl-5 my-3 space-y-1 text-[#4A4741]">');
            inList = true;
          }
          result.push(`<li>${formatInline(trimmed.replace(/^[-*]\\s+/, ''))}</li>`);
          continue;
        } else {
          flushList();
        }

        if (trimmed.length > 0) {
          result.push(`<p class="my-2 leading-relaxed text-[#4A4741]">${formatInline(trimmed)}</p>`);
        }
      }

      flushList();
      flushTable();
      return result.join('\\n');
    }

    function renderMarkdownToHtml(md) {
      if (!md) return '';

      // 1. Preprocess: Elevate emoji/numbered section headers to ## headings if unheaded
      let cleanMd = md.split('\\n').map(line => {
        let trimmed = line.trim();
        // Emoji number e.g. 1️⃣ or Chinese section e.g. 一、
        if (/^[0-9]\\uFE0F?\\u20E3/.test(trimmed) || /^[一二三四五六七八九十]+[、. ]/.test(trimmed)) {
          if (!line.startsWith('#')) return '## ' + line;
        }
        return line;
      }).join('\\n');

      // 2. If marked is available, use marked with GFM table wrapping
      if (typeof marked !== 'undefined' && (marked.parse || typeof marked === 'function')) {
        try {
          const parseFn = marked.parse || marked;
          let html = parseFn(cleanMd, { gfm: true, breaks: true });
          // Wrap tables in responsive horizontal scroll wrapper
          html = html.replaceAll('<table>', '<div class="overflow-x-auto my-4 rounded-xl border border-[#E8E5DD] shadow-xs"><table class="min-w-full text-xs">');
          html = html.replaceAll('</table>', '</table></div>');
          return html;
        } catch(e) {
          console.warn("marked.parse error, using fallback parser:", e);
        }
      }

      // 3. Fallback to built-in parser
      return fallbackMarkdownParser(cleanMd);
    }

    function handleFormSubmit(e) {
      e.preventDefault();
      const query = document.getElementById('niche-input').value.trim();
      const market = document.getElementById('market-select').value;
      const modelVal = document.getElementById('model-select').value;
      const [provider, model] = modelVal.split(':');

      if (!query) return;

      // Close previous connection if any
      if (activeEventSource) {
        activeEventSource.close();
      }

      // UI Transition to Running
      document.getElementById('submit-btn').disabled = true;
      document.getElementById('btn-icon').textContent = '⏳';
      document.getElementById('btn-text').textContent = '正在调研中...';
      document.getElementById('stepper-section').classList.remove('hidden');
      document.getElementById('showcase-section').classList.add('hidden');
      document.getElementById('results-container').classList.add('hidden');
      document.getElementById('progress-bar-fill').style.width = '10%';
      document.getElementById('agent-log-container').innerHTML = '';

      setNodeStatus(1, 'active', '正在拆解调研路径与意图...');
      setNodeStatus(2, 'waiting', '等待调度出海工具链...');
      setNodeStatus(3, 'waiting', '等待审查数据与毛利红线...');
      setNodeStatus(4, 'waiting', '等待综合生成立项报告...');

      appendAgentLog(`>> [1. PLANNER] 启动多维度调研规划: ${query} (站点: ${market})`);

      // Start Server-Sent Events (SSE) Stream
      const url = `/api/stream?query=${encodeURIComponent(query)}&market=${encodeURIComponent(market)}&provider=${encodeURIComponent(provider)}&model=${encodeURIComponent(model)}`;
      activeEventSource = new EventSource(url);

      activeEventSource.onmessage = function(event) {
        let data;
        try {
          data = JSON.parse(event.data);
        } catch(e) {
          console.warn("[SSE Non-JSON or comment]:", event.data);
          return;
        }

        if (data.type === 'connected') {
          appendAgentLog("[System] 实时推流通信链路建立成功，智能体已介入执行...");
          return;
        }

        if (data.type === 'node_update') {
          const node = data.node;
          const state = data.state;

          if (node === 'planner') {
            document.getElementById('progress-bar-fill').style.width = '35%';
            setNodeStatus(1, 'completed', '规划完成 · 拆解4大维度子任务');
            setNodeStatus(2, 'active', '正在提取标杆竞品与买家VOC差评...');
            appendAgentLog(`[Planner] 战略大纲: ${state.plan_overview || '拆解完成'}`);
            if (state.subtasks) {
              appendAgentLog(`[Planner] 已创建 ${state.subtasks.length} 个多维子任务`);
            }
          } else if (node === 'researcher') {
            document.getElementById('progress-bar-fill').style.width = '70%';
            const comps = state.competitors || [];
            const voc = state.voc_defects || [];
            const fin = state.financial_model || {};
            setNodeStatus(2, 'completed', `抓取 ${comps.length} 款标杆 · ${voc.length} 项痛点 · 净利 ${fin.net_margin_percentage || 0}%`);
            setNodeStatus(3, 'active', '质检专家正在审查数据与毛利红线...');
            appendAgentLog(`[Researcher] 获取到 ${comps.length} 款同类竞品，提炼 ${voc.length} 大核心VOC`);
          } else if (node === 'critic') {
            document.getElementById('progress-bar-fill').style.width = '85%';
            setNodeStatus(3, 'completed', '质检通过 · 数据与毛利指标达标');
            setNodeStatus(4, 'active', '正在综合撰写万字立项决策报告...');
            appendAgentLog(`[Critic] 质检评估: ${(state.critic_notes && state.critic_notes[0]) || '数据完备'}`);
          } else if (node === 'synthesizer') {
            document.getElementById('progress-bar-fill').style.width = '100%';
            setNodeStatus(4, 'completed', '立项报告合成就绪');
            appendAgentLog(`[Synthesizer] 报告合成完成，正在渲染仪表盘...`);
          }
        } else if (data.type === 'done') {
          activeEventSource.close();
          renderResults(data.final_state);
          showToast("🎉 调研全流程闭环完成！");
        } else if (data.type === 'error') {
          activeEventSource.close();
          alert('调研执行异常: ' + data.message);
          document.getElementById('submit-btn').disabled = false;
          document.getElementById('btn-icon').textContent = '🚀';
          document.getElementById('btn-text').textContent = '启动深度调研';
        }
      };

      activeEventSource.onerror = function() {
        activeEventSource.close();
        document.getElementById('submit-btn').disabled = false;
        document.getElementById('btn-icon').textContent = '🚀';
        document.getElementById('btn-text').textContent = '启动深度调研';
      };
    }

    function renderResults(state) {
      currentFinalState = state;
      currentRawReport = state.final_report || "";

      document.getElementById('submit-btn').disabled = false;
      document.getElementById('btn-icon').textContent = '🚀';
      document.getElementById('btn-text').textContent = '启动深度调研';
      document.getElementById('stepper-status-badge').innerHTML = '<span class="text-[#2F634E] font-semibold">✓ 闭环完成</span>';

      const resolved = state.resolved_product;
      const fin = state.financial_model || {};
      const competitors = state.competitors || [];
      const voc = state.voc_defects || [];

      // Recognition Banner
      if (resolved && resolved.is_asin) {
        document.getElementById('asin-banner').classList.remove('hidden');
        document.getElementById('asin-banner-title').textContent = `标杆竞品锚定成功：${resolved.title || state.niche_query}`;
        document.getElementById('asin-banner-sub').textContent = `品牌: ${resolved.brand || 'N/A'} | ASIN: ${resolved.asin} | 站点: ${state.target_market || 'US'}`;
      } else {
        document.getElementById('asin-banner').classList.add('hidden');
      }

      // Metric Cards
      document.getElementById('metric-rating').textContent = fin.viability_rating || 'Healthy';
      document.getElementById('metric-margin').textContent = `${fin.net_margin_percentage || 0}%`;
      document.getElementById('metric-profit').textContent = `$${fin.net_profit_usd || 0}`;
      document.getElementById('metric-fba').textContent = fin.fba_tier || 'Standard';
      document.getElementById('metric-fba-fee').textContent = `配送费: $${fin.fba_fulfillment_fee_usd || 0} /件`;

      // Report Tab
      document.getElementById('report-title').textContent = `《${state.niche_query} 出海商业可行性深度决策报告》`;
      document.getElementById('report-markdown-content').innerHTML = renderMarkdownToHtml(currentRawReport);

      // Competitors Table
      const tbody = document.getElementById('competitors-tbody');
      tbody.innerHTML = competitors.map(c => `
        <tr class="hover:bg-[#FAF8F5] transition-colors">
          <td class="py-3 px-4 font-semibold text-[#232220]">${c.brand || 'Unknown'}</td>
          <td class="py-3 px-4 text-[#4A4741]">${c.title || 'N/A'}</td>
          <td class="py-3 px-4 font-semibold text-[#C25E3E]">$${c.price_usd || 0}</td>
          <td class="py-3 px-4 text-[#706B62]">${c.rating || 0} (${c.reviews_count || 0})</td>
          <td class="py-3 px-4 text-[#232220]">#${c.bsr_rank || 'N/A'}</td>
          <td class="py-3 px-4 text-[#232220]">${c.estimated_monthly_sales || 'N/A'} 件</td>
        </tr>
      `).join('');

      // VOC Cards
      const vocContainer = document.getElementById('voc-cards-container');
      vocContainer.innerHTML = voc.map(v => `
        <div class="rounded-xl border border-[#E8E5DD] bg-[#FCFBF8] p-4 flex flex-col justify-between">
          <div>
            <div class="flex justify-between items-start mb-2">
              <span class="font-semibold text-xs text-[#232220]">${v.component}</span>
              <span class="text-xs px-2 py-0.5 rounded-full ${v.severity.includes('High') ? 'bg-[#FBEBEB] text-[#B83232]' : 'bg-[#FDF3E7] text-[#9A6218]'} font-medium">
                ${v.severity} (${v.frequency_percent || 0}%)
              </span>
            </div>
            <p class="text-xs text-[#4A4741] mb-2 font-medium">${v.defect_description}</p>
            <p class="text-xs italic text-[#706B62] bg-white p-2.5 rounded-lg border border-[#F2EFE8] mb-3">"${v.customer_quote}"</p>
          </div>
          <div class="pt-2 border-t border-[#F2EFE8]">
            <span class="text-xs font-semibold text-[#2F634E] block mb-0.5">模具/供应链改良方案：</span>
            <p class="text-xs text-[#232220]">${v.factory_countermeasure}</p>
          </div>
        </div>
      `).join('');

      // Calculator Sliders Initialization
      if (fin.retail_price_usd) document.getElementById('slider-retail').value = fin.retail_price_usd;
      if (fin.sourcing_cost_usd) document.getElementById('slider-sourcing').value = Math.round(fin.sourcing_cost_usd * 7.2);
      recalcCost();

      // Show Results
      document.getElementById('results-container').classList.remove('hidden');
      document.getElementById('results-container').scrollIntoView({ behavior: 'smooth' });
    }

    function switchTab(tabId) {
      document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('border-[#C25E3E]', 'text-[#C25E3E]');
        btn.classList.add('border-transparent', 'text-[#706B62]');
      });
      const activeBtn = document.getElementById(`tab-btn-${tabId}`);
      if (activeBtn) {
        activeBtn.classList.remove('border-transparent', 'text-[#706B62]');
        activeBtn.classList.add('border-[#C25E3E]', 'text-[#C25E3E]');
      }

      ['report', 'competitors', 'voc', 'calculator'].forEach(p => {
        const pane = document.getElementById(`tab-pane-${p}`);
        if (p === tabId) pane.classList.remove('hidden');
        else pane.classList.add('hidden');
      });
    }

    function recalcCost() {
      const retail = parseFloat(document.getElementById('slider-retail').value);
      const sourcingRmb = parseFloat(document.getElementById('slider-sourcing').value);
      const acos = parseFloat(document.getElementById('slider-acos').value);
      const cbm = parseFloat(document.getElementById('slider-cbm').value);

      document.getElementById('slider-retail-val').textContent = `$${retail.toFixed(2)}`;
      document.getElementById('slider-sourcing-val').textContent = `¥${sourcingRmb.toFixed(1)}`;
      document.getElementById('slider-acos-val').textContent = `${acos}%`;
      document.getElementById('slider-cbm-val').textContent = `$${cbm}`;

      const sourcingUsd = sourcingRmb / 7.20;
      const freightPerUnit = 0.005 * cbm;
      const tariff = sourcingUsd * 0.25;
      const fbaFee = 5.26;
      const commission = retail * 0.15;
      const adSpend = retail * (acos / 100);
      const returnReserve = retail * 0.03;

      const totalCost = sourcingUsd + freightPerUnit + tariff + fbaFee + commission + adSpend + returnReserve;
      const netProfit = retail - totalCost;
      const netMargin = (netProfit / retail) * 100;

      document.getElementById('calc-sourcing').textContent = `$${sourcingUsd.toFixed(2)}`;
      document.getElementById('calc-freight').textContent = `$${freightPerUnit.toFixed(2)}`;
      document.getElementById('calc-tariff').textContent = `$${tariff.toFixed(2)}`;
      document.getElementById('calc-fba').textContent = `$${fbaFee.toFixed(2)}`;
      document.getElementById('calc-commission').textContent = `$${commission.toFixed(2)}`;
      document.getElementById('calc-ad').textContent = `$${(adSpend + returnReserve).toFixed(2)}`;

      document.getElementById('calc-profit-big').textContent = `$${netProfit.toFixed(2)}`;
      document.getElementById('calc-margin-big').textContent = `${netMargin.toFixed(1)}%`;

      const marginEl = document.getElementById('calc-margin-big');
      if (netMargin < 12) {
        marginEl.className = "font-serif-claude text-3xl font-medium text-[#B83232]";
      } else if (netMargin < 20) {
        marginEl.className = "font-serif-claude text-3xl font-medium text-[#9A6218]";
      } else {
        marginEl.className = "font-serif-claude text-3xl font-medium text-[#C25E3E]";
      }
    }

    function copyMarkdownReport() {
      if (!currentRawReport) {
        showToast("暂无可复制的报告内容");
        return;
      }
      navigator.clipboard.writeText(currentRawReport).then(() => {
        showToast("已成功复制决策报告 Markdown 到剪贴板！");
      });
    }

    function downloadMarkdownReport() {
      if (!currentRawReport) {
        showToast("暂无可下载的报告内容");
        return;
      }
      const blob = new Blob([currentRawReport], { type: 'text/markdown;charset=utf-8;' });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = `DeepResearch_FeasibilityReport.md`;
      link.click();
    }
  </script>
</body>
</html>
"""

SERVED_HTML_PAGE = HTML_PAGE.replace(
    "<!-- MARKED_JS_INJECTION -->",
    f"<script>\n{MARKED_JS_SOURCE}\n</script>"
)

async def homepage(request):
    """Serve pre-rendered HTML in under 3 milliseconds with zero white screen."""
    return HTMLResponse(SERVED_HTML_PAGE)


async def stream_research(request):
    """Server-Sent Events (SSE) streaming endpoint for real-time LangGraph execution."""
    query = request.query_params.get("query", "B0BS1QCFHX").strip()
    market = request.query_params.get("market", "US").strip()
    provider = request.query_params.get("provider", "groq").strip()
    model = request.query_params.get("model", "openai/gpt-oss-120b").strip()

    initial_state = {
        "niche_query": query,
        "target_market": market,
        "resolved_product": None,
        "llm_provider": provider,
        "llm_model": model,
        "max_iterations": 1,
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

    async def event_generator():
        loop = asyncio.get_running_loop()
        q = asyncio.Queue()

        def sync_worker():
            try:
                from deep_research.graph import build_research_graph
                graph = build_research_graph()
                current_state = dict(initial_state)

                for event in graph.stream(current_state, stream_mode="updates"):
                    node_name = list(event.keys())[0]
                    node_data = event[node_name]
                    current_state.update(node_data)

                    clean_data = {}
                    for k, v in node_data.items():
                        if k == "subtasks":
                            clean_data[k] = [t.model_dump() if hasattr(t, "model_dump") else t for t in v]
                        else:
                            clean_data[k] = v

                    asyncio.run_coroutine_threadsafe(
                        q.put({"type": "node_update", "node": node_name, "state": clean_data}), 
                        loop
                    )

                final_clean = {}
                for k, v in current_state.items():
                    if k == "subtasks":
                        final_clean[k] = [t.model_dump() if hasattr(t, "model_dump") else t for t in v]
                    else:
                        final_clean[k] = v

                asyncio.run_coroutine_threadsafe(
                    q.put({"type": "done", "final_state": final_clean}),
                    loop
                )
            except Exception as e:
                asyncio.run_coroutine_threadsafe(
                    q.put({"type": "error", "message": str(e)}),
                    loop
                )
            finally:
                asyncio.run_coroutine_threadsafe(q.put(None), loop)

        threading.Thread(target=sync_worker, daemon=True).start()

        # 1. Immediately yield connected event so client and proxies know stream is alive
        yield 'data: {"type": "connected"}\n\n'

        # 2. Yield events as they arrive, with periodic keep-alive comments while waiting
        while True:
            try:
                item = await asyncio.wait_for(q.get(), timeout=2.0)
                if item is None:
                    break
                payload = json.dumps(item, ensure_ascii=False)
                yield f"data: {payload}\n\n"
            except asyncio.TimeoutError:
                # Keep-alive comment to prevent proxy or browser timeout
                yield ": keep-alive\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


app = Starlette(
    routes=[
        Route("/", homepage),
        Route("/api/stream", stream_research),
    ]
)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8501))
    print(f"Starting High-Performance Zero-Latency Web Server on http://localhost:{port}...")
    uvicorn.run("ui.server:app", host="0.0.0.0", port=port, log_level="info")
