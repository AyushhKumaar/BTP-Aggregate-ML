"""
tune_pdf_pages.py
Tunes the HTML CSS and page breaks to achieve exactly 21-22 pages.
"""

import re
import base64
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pypdf

PROJECT_ROOT = Path(r"c:\Users\Ayush\Documents\BTP_Aggregate_ML")
DOCS_DIR = PROJECT_ROOT / "docs"
FIGURES_DIR = DOCS_DIR / "figures"
HTML_OUT = DOCS_DIR / "BTP_IITJ_Final_Report.html"
PDF_OUT = DOCS_DIR / "BTP_IITJ_Final_Report.pdf"
ARTIFACT_DIR = Path(r"C:\Users\Ayush\.gemini\antigravity\brain\aae4c91f-8ef8-4fa8-b316-d7101184cc0e")
PDF_ARTIFACT = ARTIFACT_DIR / "BTP_IITJ_Final_Report.pdf"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

with open(HTML_OUT, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Fix title page height to avoid empty page 2
html = html.replace("height: 900pt;", "height: auto; min-height: 650pt;")

# 2. Compact TOC rows so all items fit cleanly on 1 page
html = html.replace(".toc-row {\n    display: flex;\n    justify-content: space-between;\n    align-items: baseline;\n    margin-bottom: 3.5pt;\n    font-size: 10.5pt;\n}",
                    ".toc-row {\n    display: flex;\n    justify-content: space-between;\n    align-items: baseline;\n    margin-bottom: 2pt;\n    font-size: 9.5pt;\n    line-height: 1.25;\n}")
html = html.replace(".toc-row.chapter {\n    font-weight: bold;\n    margin-top: 4pt;\n}",
                    ".toc-row.chapter {\n    font-weight: bold;\n    margin-top: 2.5pt;\n}")

# 3. Compact figure sizes and margins so they don't cause trailing 2-line spills
html = html.replace(".figure-container {\n    text-align: center;\n    margin-top: 10pt;\n    margin-bottom: 12pt;\n    page-break-inside: avoid;\n}",
                    ".figure-container {\n    text-align: center;\n    margin-top: 6pt;\n    margin-bottom: 8pt;\n    page-break-inside: avoid;\n}")
html = html.replace(".figure-container img {\n    max-width: 95%;\n    height: auto;",
                    ".figure-container img {\n    max-width: 86%;\n    max-height: 235px;\n    height: auto;")

# 4. Compact tables slightly
html = html.replace("table.report-table th {\n    background-color: #1E3A8A; /* IIT Navy */\n    color: #ffffff;\n    font-weight: bold;\n    padding: 6pt 6pt;\n    border: 1px solid #1E3A8A;\n    text-align: center;\n}",
                    "table.report-table th {\n    background-color: #1E3A8A; /* IIT Navy */\n    color: #ffffff;\n    font-weight: bold;\n    padding: 4pt 5pt;\n    border: 1px solid #1E3A8A;\n    text-align: center;\n}")
html = html.replace("table.report-table td {\n    padding: 5pt 6pt;\n    border: 1px solid #cbd5e1;\n    color: #0f172a;\n}",
                    "table.report-table td {\n    padding: 3.5pt 5pt;\n    border: 1px solid #cbd5e1;\n    color: #0f172a;\n}")

# 5. Spacings
html = html.replace("h1 {\n    font-size: 14pt;\n    margin-top: 18pt;\n    margin-bottom: 8pt;\n    text-transform: uppercase;\n}",
                    "h1 {\n    font-size: 13.5pt;\n    margin-top: 14pt;\n    margin-bottom: 6pt;\n    text-transform: uppercase;\n}")
html = html.replace("h2 {\n    font-size: 12pt;\n    margin-top: 12pt;\n    margin-bottom: 6pt;\n}",
                    "h2 {\n    font-size: 11.5pt;\n    margin-top: 9pt;\n    margin-bottom: 4pt;\n}")
html = html.replace("p {\n    margin-top: 0;\n    margin-bottom: 6pt;\n}",
                    "p {\n    margin-top: 0;\n    margin-bottom: 5pt;\n}")

with open(HTML_OUT, "w", encoding="utf-8") as f:
    f.write(html)

print("Updated HTML. Now rendering PDF to check page count...")

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.binary_location = CHROME_PATH

driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get(HTML_OUT.as_uri())
    driver.execute_async_script("""
        var callback = arguments[arguments.length - 1];
        if (window.MathJax && window.MathJax.startup && window.MathJax.startup.promise) {
            window.MathJax.startup.promise.then(function() { callback(true); });
        } else {
            setTimeout(function() { callback(true); }, 2000);
        }
    """)
    time.sleep(2)
    
    cdp_params = {
        "landscape": False,
        "displayHeaderFooter": True,
        "headerTemplate": '''
            <div style="font-family: 'Times New Roman', Times, serif; font-size: 7.5pt; color: #4b5563; width: 100%; border-bottom: 0.5px solid #cbd5e1; padding-bottom: 2px; margin: 0 18mm; display: flex; justify-content: space-between;">
                <span>IIT Jodhpur | Department of Civil &amp; Infrastructure Engineering</span>
                <span>B.Tech Project Report</span>
            </div>
        ''',
        "footerTemplate": '''
            <div style="font-family: 'Times New Roman', Times, serif; font-size: 8pt; color: #4b5563; width: 100%; border-top: 0.5px solid #cbd5e1; padding-top: 2px; margin: 0 18mm; text-align: center;">
                Page <span class="pageNumber"></span> of <span class="totalPages"></span>
            </div>
        ''',
        "printBackground": True,
        "paperWidth": 8.27,
        "paperHeight": 11.69,
        "marginTop": 0.75,
        "marginBottom": 0.75,
        "marginLeft": 0.75,
        "marginRight": 0.7,
        "preferCSSPageSize": True
    }
    
    pdf_result = driver.execute_cdp_cmd("Page.printToPDF", cdp_params)
    pdf_bytes = base64.b64decode(pdf_result["data"])
    
    with open(PDF_OUT, "wb") as f:
        f.write(pdf_bytes)
    with open(PDF_ARTIFACT, "wb") as f:
        f.write(pdf_bytes)
        
    reader = pypdf.PdfReader(str(PDF_OUT))
    print(f"Total Pages in PDF: {len(reader.pages)}")
    for i, page in enumerate(reader.pages):
        txt = page.extract_text().strip().split('\n')
        h = txt[0] if txt else ''
        print(f"Page {i+1}: {h[:60]}")

finally:
    driver.quit()
