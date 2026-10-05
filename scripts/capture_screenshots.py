import http.server
import socketserver
import threading
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

PORT = 8095
DIRECTORY = "site"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

httpd = socketserver.TCPServer(("", PORT), Handler)
server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
server_thread.start()
print(f"HTTP server started on port {PORT}")

out_dir = Path("docs/images")
out_dir.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
    
    # 1. Portal Overview Screenshot (Clean Unclustered Graph + Programs Sidebar)
    page = context.new_page()
    page.goto(f"http://localhost:{PORT}/index.html#program=INQCUST&tab=call_graph")
    page.wait_for_timeout(1500)
    page.evaluate("if (typeof toggleSidebar === 'function') toggleSidebar(true);")
    page.wait_for_timeout(1000)
    page.screenshot(path=str(out_dir / "portal_overview.png"))
    print("Captured portal_overview.png (unclustered UI)")

    # 2. Standalone Call Graph with Wider Split Code (Alt+C)
    cg_page = context.new_page()
    cg_page.goto(f"http://localhost:{PORT}/INQCUST.html")
    cg_page.wait_for_timeout(1500)
    # Clear local storage ratio if any so it uses the new 42/58 default
    cg_page.evaluate("localStorage.removeItem('cobolscope_code_split_ratio');")
    cg_page.keyboard.press("Alt+c")
    cg_page.wait_for_timeout(1000)
    cg_page.screenshot(path=str(out_dir / "call_graph_split_code.png"))
    print("Captured call_graph_split_code.png (wider code pane)")

    # 3. Level 3 Intra-Procedural Flowchart Modal
    cg_page.evaluate("""
        const btn = document.getElementById('btnOpenLevel3');
        if (btn) {
            btn.click();
        } else if (typeof openLevel3Modal === 'function') {
            openLevel3Modal(selectedRoutineNode);
        }
    """)
    cg_page.wait_for_timeout(1000)
    cg_page.evaluate("""
        if (typeof window.cyLevel3 !== 'undefined' && window.cyLevel3) {
            window.cyLevel3.fit(undefined, 30);
            window.cyLevel3.zoom(window.cyLevel3.zoom() * 1.35);
            window.cyLevel3.center();
        }
    """)
    cg_page.wait_for_timeout(800)
    cg_page.screenshot(path=str(out_dir / "level3_flowchart.png"))
    print("Captured level3_flowchart.png (crisp L3 modal)")

    # 4. Standalone Data Dictionary with Split Code Drawer Open
    dict_page = context.new_page()
    dict_page.goto(f"http://localhost:{PORT}/INQCUST_dict.html")
    dict_page.wait_for_timeout(1500)
    rows = dict_page.query_selector_all("table tbody tr")
    if len(rows) > 3:
        rows[3].click()
        dict_page.wait_for_timeout(1000)
    dict_page.screenshot(path=str(out_dir / "data_dictionary_split.png"))
    print("Captured data_dictionary_split.png")

    # 5. Portal Data Dictionary View
    p_dict_page = context.new_page()
    p_dict_page.goto(f"http://localhost:{PORT}/index.html#program=INQCUST&tab=data_dictionary")
    p_dict_page.wait_for_timeout(1500)
    p_dict_page.evaluate("if (typeof toggleSidebar === 'function') toggleSidebar(true);")
    p_dict_page.wait_for_timeout(1000)
    p_dict_page.screenshot(path=str(out_dir / "portal_data_dictionary.png"))
    print("Captured portal_data_dictionary.png")

    browser.close()

httpd.shutdown()
print("All updated screenshots generated and server stopped successfully!")
