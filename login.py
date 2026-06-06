import os
import sys
import cloudscraper
from bs4 import BeautifulSoup


def login():
    username = os.environ.get("FORUM_USERNAME")
    password = os.environ.get("FORUM_PASSWORD")
    forum_url = os.environ.get("FORUM_URL")

    if not all([username, password, forum_url]):
        print("Error: FORUM_USERNAME, FORUM_PASSWORD, dan FORUM_URL harus di-set.")
        sys.exit(1)

    scraper = cloudscraper.create_scraper(
        browser={"browser": "chrome", "platform": "windows", "mobile": False}
    )

    print(f"Membuka {forum_url} ...")
    resp = scraper.get(forum_url, timeout=30)

    if resp.status_code != 200:
        print(f"Gagal mengakses halaman login: HTTP {resp.status_code}")
        sys.exit(1)

    soup = BeautifulSoup(resp.text, "html.parser")
    formhash_input = soup.find("input", {"name": "formhash"})
    if not formhash_input:
        print("formhash tidak ditemukan — halaman mungkin masih di-block Cloudflare.")
        print(f"Judul halaman: {soup.title.string if soup.title else 'N/A'}")
        sys.exit(1)

    formhash = formhash_input["value"]
    base_url = forum_url.split("member.php")[0]
    print(f"Halaman login berhasil diakses.")

    login_data = {
        "formhash": formhash,
        "referer": base_url,
        "loginfield": "email",
        "username": username,
        "password": password,
        "questionid": "0",
        "answer": "",
        "loginsubmit": "true",
    }

    login_url = f"{base_url}member.php?mod=logging&action=login&loginsubmit=yes"
    resp = scraper.post(login_url, data=login_data, timeout=30, allow_redirects=True)

    final_url = resp.url
    print(f"URL akhir: {final_url}")

    if "logging" in final_url or "login" in final_url.lower():
        soup = BeautifulSoup(resp.text, "html.parser")
        error_el = (
            soup.find(class_=["alert_error", "alert_info"])
            or soup.find(id="messagetext")
        )
        msg = error_el.get_text().strip() if error_el else "masih di halaman login"
        print(f"Login GAGAL: {msg}")
        sys.exit(1)

    print("Login BERHASIL.")


if __name__ == "__main__":
    login()
