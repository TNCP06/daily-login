import os
import sys
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from playwright_stealth import stealth_sync

HEADLESS = os.environ.get("HEADLESS", "true").lower() != "false"


def wait_for_cloudflare(page, timeout_ms=30000):
    """Block until Cloudflare 'Just a moment...' challenge passes."""
    try:
        page.wait_for_function(
            "() => !document.title.toLowerCase().includes('just a moment')",
            timeout=timeout_ms,
        )
        page.wait_for_load_state("load", timeout=15000)
        print("Cloudflare challenge passed.")
    except PlaywrightTimeoutError:
        raise RuntimeError("Cloudflare challenge tidak selesai dalam batas waktu.")


def login():
    username = os.environ.get("FORUM_USERNAME")
    password = os.environ.get("FORUM_PASSWORD")
    forum_url = os.environ.get("FORUM_URL")

    if not all([username, password, forum_url]):
        print("Error: FORUM_USERNAME, FORUM_PASSWORD, dan FORUM_URL harus di-set.")
        sys.exit(1)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=HEADLESS,
                args=["--disable-blink-features=AutomationControlled"],
            )
            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
                ignore_https_errors=True,
            )
            page = context.new_page()
            stealth_sync(page)

            print(f"Membuka {forum_url} ...")
            page.goto(forum_url, wait_until="load", timeout=60000)

            if "just a moment" in page.title().lower():
                print("Cloudflare terdeteksi, menunggu challenge selesai...")
                wait_for_cloudflare(page)

            print(f"Judul halaman : {page.title()}")
            print(f"URL saat ini  : {page.url}")

            page.wait_for_selector('input[name="username"]', timeout=30000)
            page.fill('input[name="username"]', username)
            page.fill('input[name="password"]', password)
            page.press('input[name="password"]', "Enter")

            # Wait for AJAX redirect to complete
            page.wait_for_timeout(6000)

            final_url = page.url
            print(f"URL akhir: {final_url}")

            if "logging" in final_url or "login" in final_url.lower():
                error_el = page.query_selector(
                    ".alert_error, .alert_info, #messagetext, .login_error, .errorhandle"
                )
                msg = error_el.inner_text().strip() if error_el else "tidak ada pesan error"
                print(f"Login GAGAL — {msg}")
                browser.close()
                sys.exit(1)

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
