import os
import sys
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def login():
    username = os.environ.get("FORUM_USERNAME")
    password = os.environ.get("FORUM_PASSWORD")
    forum_url = os.environ.get("FORUM_URL")

    if not all([username, password, forum_url]):
        print("Error: FORUM_USERNAME, FORUM_PASSWORD, dan FORUM_URL harus di-set.")
        sys.exit(1)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            print(f"Membuka {forum_url} ...")
            page.goto(forum_url, timeout=30000)

            page.fill('input[name="username"]', username)
            page.fill('input[name="password"]', password)
            page.click('button[type="submit"]')

            time.sleep(3)

            final_url = page.url
            print(f"URL akhir: {final_url}")
            print("Login selesai.")

            browser.close()

    except PlaywrightTimeoutError as e:
        print(f"Timeout saat membuka halaman: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Login gagal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    login()
