import os
import sys
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

HEADLESS = os.environ.get("HEADLESS", "true").lower() != "false"


def login():
    username = os.environ.get("FORUM_USERNAME")
    password = os.environ.get("FORUM_PASSWORD")
    forum_url = os.environ.get("FORUM_URL")

    if not all([username, password, forum_url]):
        print("Error: FORUM_USERNAME, FORUM_PASSWORD, dan FORUM_URL harus di-set.")
        sys.exit(1)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=HEADLESS)
            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
                ignore_https_errors=True,
            )
            page = context.new_page()

            print(f"Membuka {forum_url} ...")
            page.goto(forum_url, wait_until="load", timeout=60000)

            print(f"Judul halaman : {page.title()}")
            print(f"URL saat ini  : {page.url}")

            page.wait_for_selector('input[name="username"]', timeout=15000)
            page.fill('input[name="username"]', username)
            page.fill('input[name="password"]', password)

            # Submit via Enter key — most reliable for Discuz! AJAX forms
            page.press('input[name="password"]', "Enter")

            # Give AJAX time to complete then check result
            page.wait_for_timeout(6000)

            final_url = page.url
            title = page.title()
            print(f"URL setelah submit : {final_url}")
            print(f"Judul setelah submit: {title}")

            # Check for any visible error/info message on page
            error_el = page.query_selector(".alert_error, .alert_info, #messagetext, .login_error, .errorhandle")
            if error_el:
                msg = error_el.inner_text().strip()
                print(f"Pesan di halaman: {msg}")

            if "logging" in final_url or "login" in final_url.lower():
                print("Login GAGAL — masih di halaman login.")
                browser.close()
                sys.exit(1)
            else:
                print("Login BERHASIL.")

            browser.close()

    except PlaywrightTimeoutError as e:
        print(f"Timeout: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Login gagal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    login()
