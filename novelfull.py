import time
import random
from bs4 import BeautifulSoup
from ebooklib import epub
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# -----------------------------
# Setup Selenium Headless Driver
# -----------------------------
def setup_driver():
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120 Safari/537.36"
    )

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=opts)


# -----------------------------
# Fetch HTML
# -----------------------------
def fetch_html(driver, url):
    driver.get(url)
    time.sleep(random.uniform(1.2, 2.0))
    return driver.page_source


# -----------------------------
# Ambil daftar chapter dari page 1 sampai page limit
# -----------------------------
def get_chapter_list(driver, novel_url, page_limit):
    print(f"Mengambil daftar chapter dari halaman 1 sampai {page_limit}...\n")

    chapter_links = []

    for page in range(1, page_limit + 1):
        page_url = f"{novel_url}?page={page}"
        print(f"Memuat halaman: {page_url}")

        html = fetch_html(driver, page_url)
        soup = BeautifulSoup(html, "html.parser")

        links = soup.select(".list-chapter li a")
        if not links:
            print(f"⚠ Halaman {page} tidak ada chapter.")
            continue

        for a in links:
            chapter_links.append("https://novelfull.com" + a["href"])

    print(f"\nTotal chapter terkumpul dari {page_limit} halaman: {len(chapter_links)}\n")
    return chapter_links


# -----------------------------
# Ambil satu chapter (retry 5x)
# -----------------------------
def fetch_chapter(driver, url):
    for attempt in range(5):
        try:
            html = fetch_html(driver, url)
            soup = BeautifulSoup(html, "html.parser")

            # Title
            title_el = soup.select_one("span.chr-text") or soup.select_one("h2")
            title = title_el.get_text(strip=True) if title_el else "No Title"

            # Content
            content_el = soup.select_one("#chapter-content")
            content = str(content_el) if content_el else "<p>No content found</p>"

            return title, content

        except Exception as e:
            print(f"⚠ Gagal mengambil chapter (attempt {attempt+1}/5): {e}")
            time.sleep(1.5)

    print(f"❌ Gagal total memuat: {url}")
    return "Unknown Chapter", "<p>Failed to fetch content.</p>"


# -----------------------------
# Build EPUB
# -----------------------------
def build_epub(novel_title, chapters):
    book = epub.EpubBook()
    book.set_identifier("novelfull-crawler")
    book.set_title(novel_title)
    book.set_language("en")

    epub_chapters = []

    for i, ch in enumerate(chapters):
        c = epub.EpubHtml(
            title=ch["title"],
            file_name=f"chap_{i+1}.xhtml",
            lang="en"
        )
        c.content = f"<h2>{ch['title']}</h2>{ch['content']}"
        book.add_item(c)
        epub_chapters.append(c)

    book.toc = tuple(epub_chapters)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["nav"] + epub_chapters

    filename = f"{novel_title.replace(' ', '_')}.epub"
    epub.write_epub(filename, book)

    print(f"\n✨ EPUB berhasil dibuat: {filename}")


# -----------------------------
# Main
# -----------------------------
def main():
    novel_url = "https://novelfull.com/i-might-be-a-fake-cultivator.html"
    novel_title = "I Might Be A Fake Cultivator"

    # --------------------------------
    # ❗ Kamu bisa UBAH LIMIT PAGE DI SINI
    # --------------------------------
    # Contoh: sampai halaman 48
    # last_page = 48

    # atau gunakan input:
    last_page = int(input("Masukkan batas halaman (misal 48): ").strip())

    driver = setup_driver()

    chapter_urls = get_chapter_list(driver, novel_url, last_page)

    # Urutkan berdasarkan nomor chapter
    try:
        chapter_urls = sorted(
            chapter_urls,
            key=lambda x: int(x.split("-")[-1].replace(".html", "").replace("/", "") or 0)
        )
    except:
        pass  # kalau gagal, biarkan apa adanya

    chapters = []
    for idx, url in enumerate(chapter_urls, 1):
        print(f"Scraping Chapter {idx}/{len(chapter_urls)}")
        title, content = fetch_chapter(driver, url)
        chapters.append({"title": title, "content": content})

    build_epub(novel_title, chapters)
    driver.quit()


if __name__ == "__main__":
    main()
