import os
from playwright.sync_api import sync_playwright

def inspect_captcha_and_button():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1280, 'height': 800})
        page.goto("https://kpp.tbkc.gov.tw/", wait_until="networkidle")

        imgs = page.query_selector_all("img")
        print(f"Found {len(imgs)} images:")
        for idx, img in enumerate(imgs):
            src = img.get_attribute("src") or ""
            id_attr = img.get_attribute("id") or ""
            alt = img.get_attribute("alt") or ""
            print(f"  Img {idx}: id={id_attr}, alt={alt}, src={src}")

        buttons = page.query_selector_all("button, input[type='submit'], a.btn, input[type='button']")
        print(f"Found {len(buttons)} buttons/submit controls:")
        for idx, btn in enumerate(buttons):
            text = btn.inner_text() or btn.get_attribute("value") or ""
            id_attr = btn.get_attribute("id") or ""
            class_attr = btn.get_attribute("class") or ""
            print(f"  Button {idx}: id={id_attr}, text={text.strip()}, class={class_attr}")

        browser.close()

if __name__ == "__main__":
    inspect_captcha_and_button()
