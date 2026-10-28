# 🚢 跨境电商 Deep Research Agent 云端免费部署指南

本项目已为你配置好 **100% 免费** 云端部署所需的所有依赖与配置文件，支持免信用卡、极速一键部署。

---

## 🌟 方案一：Streamlit Community Cloud（最推荐 · 3 分钟极速上线）

这是最简单、体验最好的免费方案，**免绑定信用卡**，永久免费。

### 步骤 1：推送到你的 GitHub 仓库
在本地终端执行（如果尚未建立远程仓库）：
```bash
git add .
git commit -m "feat: complete deployment configurations"
# 如果已有远程仓库直接 push，否则在 GitHub 创建新仓库并关联：
# git remote add origin https://github.com/<你的用户名>/cross-border-deep-research.git
git push -u origin master
```
> **安全保障已生效**：`.gitignore` 已自动将包含真实密钥的 `.env` 隔离，不会被泄露到公网 GitHub。

### 步骤 2：在 Streamlit Cloud 创建应用
1. 访问并登录 [share.streamlit.io](https://share.streamlit.io/)（使用 GitHub 账号登录）。
2. 点击右上角 **Create app**。
3. 选择你的仓库，填写配置：
   - **Repository**: 选择你刚推送的仓库
   - **Branch**: `master`（或 `main`）
   - **Main file path**: `ui/app.py`
   - **App URL**: 可自定义你的专属二级域名（如 `my-amazon-deep-research.streamlit.app`）

### 步骤 3：配置云端密钥（Secrets）
点击 **Advanced settings -> Secrets**，将 [`.streamlit/secrets.toml.example`](file:///.streamlit/secrets.toml.example) 中的内容复制进去并填上你的 API Key：
```toml
DEFAULT_PROVIDER = "groq"

# 推荐 Groq 免费 API (从 https://console.groq.com 获取)
GROQ_API_KEY = "gsk_xxxxxxxxxxxxxx"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
GROQ_MODEL = "openai/gpt-oss-120b"
GROQ_MODEL_REASONING = "openai/gpt-oss-120b"
GROQ_MODEL_FAST = "openai/gpt-oss-20b"
```
4. 点击 **Deploy!** 约 1~2 分钟构建完成后，即可通过公网链接分享访问！

---

## 🚀 方案二：Hugging Face Spaces（16GB 内存 · 极高规格）

如果你需要更大的内存与算力：
1. 打开 [huggingface.co/spaces](https://huggingface.co/spaces) 并创建 Space。
2. Space SDK 选择 **Streamlit**，硬件选择 **CPU Basic (2 vCPU, 16GB RAM，完全免费)**。
3. 将代码推送到该 Space，或在 **Settings -> GitHub integration** 关联你的 GitHub。
4. 在 **Settings -> Variables and secrets** 中添加环境变量 `GROQ_API_KEY`。

---

## 🐳 方案三：Render / Koyeb / Docker 部署（定制界面 `main.py`）

如果你想部署基于 Starlette + Tailwind 的定制轻量界面：
- 本项目已生成 [`Procfile`](file:///Procfile) 与 [`Dockerfile`](file:///Dockerfile)。
- 平台（如 Render / Koyeb）会自动识别并启动：
  ```bash
  python main.py
  # 或者容器自动映射 8501 端口
  ```
