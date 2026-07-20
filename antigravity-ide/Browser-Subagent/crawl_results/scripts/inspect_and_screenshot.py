import os
import time
from playwright.sync_api import sync_playwright

def inspect_and_query():
    os.makedirs("screenshots", exist_ok=True)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    output_png = f"screenshots/車號xxx-xxxx-{timestamp}.png"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()

        print("Navigating to https://kpp.tbkc.gov.tw/ ...")
        page.goto("https://kpp.tbkc.gov.tw/", wait_until="networkidle")

        # Let's log inputs and forms
        inputs = page.query_selector_all("input")
        print(f"Found {len(inputs)} input elements:")
        for idx, inp in enumerate(inputs):
            name = inp.get_attribute("name") or ""
            id_attr = inp.get_attribute("id") or ""
            placeholder = inp.get_attribute("placeholder") or ""
            type_attr = inp.get_attribute("type") or ""
            print(f"  Input {idx}: type={type_attr}, name={name}, id={id_attr}, placeholder={placeholder}")

        # Save initial page screenshot
        page.screenshot(path="screenshots/initial_page.png")
        print("Initial screenshot saved.")

        browser.close()

if __name__ == "__main__":
    inspect_and_query()
