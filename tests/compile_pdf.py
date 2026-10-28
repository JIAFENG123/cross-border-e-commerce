import subprocess
import re
import os

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
html_path = r"D:\study\interviews\贾峰-AI-Agent应用开发工程师-简历.html"
pdf_path = r"D:\study\interviews\贾峰-AI-Agent应用开发工程师-简历.pdf"
shot_full_path = r"D:\study\interviews\full_preview.png"

url = "file:///" + html_path.replace("\\", "/")

# 1. Compile PDF
cmd_pdf = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    url
]
subprocess.run(cmd_pdf)

if os.path.exists(pdf_path):
    with open(pdf_path, "rb") as f:
        data = f.read()
    pages = len(re.findall(rb"/Type\s*/Page\b", data))
    print(f"Target PDF generated: {pages} pages, {len(data)} bytes")

# 2. Take Screenshot
cmd_shot = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--window-size=800,2350",
    f"--screenshot={shot_full_path}",
    url
]
subprocess.run(cmd_shot)
print("Screenshot generated:", os.path.exists(shot_full_path))
