import os
import uvicorn


def main():
    port = int(os.environ.get("PORT", 8501))
    print(f"🚢 启动跨境电商 Deep Research 零延迟交互工作台: http://127.0.0.1:{port}")
    uvicorn.run("ui.server:app", host="0.0.0.0", port=port, log_level="info")


if __name__ == "__main__":
    main()
