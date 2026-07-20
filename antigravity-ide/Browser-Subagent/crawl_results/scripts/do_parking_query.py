import os
import time
from playwright.sync_api import sync_playwright

def run_query():
    target_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "screenshots")
    os.makedirs(target_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 900})
        page = context.new_page()

        print("Navigating to https://kpp.tbkc.gov.tw/ ...")
        page.goto("https://kpp.tbkc.gov.tw/", wait_until="networkidle")

        # Fill vehicle license plate number xxx-xxxx
        print("Filling carNum with 'xxx-xxxx'...")
        page.fill("#carNum", "xxx-xxxx")

        # Get captcha image element if present or read captcha
        captcha_img = page.query_selector("#btnCode img") or page.query_selector("img[src*='captcha']") or page.query_selector("img[src*='Captcha']")
        if captcha_img:
            captcha_img.screenshot(path=os.path.join(target_dir, "captcha.png"))
            print("Saved captcha.png")

        # Try to read captcha text or fill placeholder code
        page.fill("#PaymentNumbercode", "1234")

        print("Clicking submit button (#btnSend)...")
        dialog_message = []
        page.on("dialog", lambda dialog: (dialog_message.append(dialog.message), dialog.accept()))

        page.click("#btnSend")
        time.sleep(3)

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = os.path.join(target_dir, f"車號xxx-xxxx-{timestamp}.png")
        page.screenshot(path=filename, full_page=True)
        print(f"Result screenshot saved to {filename}")

        if dialog_message:
            print("Dialog message popped up:", dialog_message)

        browser.close()

if __name__ == "__main__":
    run_query()
