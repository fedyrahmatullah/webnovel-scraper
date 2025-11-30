import time
from bs4 import BeautifulSoup
from ebooklib import epub
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# =========================================
# SETUP SELENIUM
# =========================================
def setup_driver():
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
    )

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    return driver


def fetch_html(driver, url):
    driver.get(url)
    time.sleep(1.2)
    return driver.page_source


# =========================================
# PAGINATION: AMBIL SEMUA CHAPTER
# =========================================
def get_chapter_list(driver, novel_url):
    print("Mengambil daftar chapter dari semua halaman...\n")

    all_chapters = []
    page = 1

    while True:
        url = f"{novel_url}?page={page}"
        print(f"Mengambil halaman: {url}")

        html = fetch_html(driver, url)
        soup = BeautifulSoup(html, "html.parser")

        links = soup.select(".list-chapter li a")

        if not links:
            print("\nPagination selesai.")
            break

        for a in links:
            full = "https://novelfull.com" + a["href"]
            all_chapters.append(full)

        page += 1
        time.sleep(0.8)

    print(f"\nTotal chapter ditemukan: {len(all_chapters)}\n")
    return all_chapters


# =========================================
# FETCH SATU CHAPTER
# =========================================
def fetch_chapter(driver, url):
    html = fetch_html(driver, url)
    soup = BeautifulSoup(html, "html.parser")

    title = soup.select_one("span.chr-text").get_text(strip=True)
    content = soup.select_one("#chapter-content")

    return title, str(content)


# =========================================
# BUILD EPUB
# =========================================
def build_epub(novel_title, chapters):
    book = epub.EpubBook()
    book.set_identifier("novelfull-crawler")
    book.set_title(novel_title)
    book.set_language("en")

    epub_chapters = []

    for i, ch in enumerate(chapters):
        c = epub.EpubHtml(
            title=ch["title"],
            file_name=f"chap_{i + 1}.xhtml",
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


# =========================================
# MAIN
# =========================================
def main():
    driver = setup_driver()
    novel_url = "https://novelfull.com/i-might-be-a-fake-cultivator.html"

    # Ambil semua chapter dari semua halaman
    chapter_urls = get_chapter_list(driver, novel_url)

    chapters = []
    for idx, url in enumerate(chapter_urls, 1):
        print(f"Scraping Chapter {idx}/{len(chapter_urls)}")
        title, content = fetch_chapter(driver, url)
        chapters.append({"title": title, "content": content})

    build_epub("I Might Be A Fake Cultivator", chapters)
    driver.quit()


if __name__ == "__main__":
    main()
