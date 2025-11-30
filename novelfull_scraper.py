import time
import cloudscraper
from bs4 import BeautifulSoup
from ebooklib import epub


# ====================================
# CLOUDSCRAPER — BYPASS CLOUDFLARE
# ====================================
scraper = cloudscraper.create_scraper(browser={
    'browser': 'chrome',
    'platform': 'windows',
    'mobile': False
})


# ====================================
# Fetch HTML
# ====================================
def fetch_html(url):
    r = scraper.get(url)
    r.raise_for_status()
    return r.text


# ====================================
# Ambil list chapter semua halaman
# ====================================
def get_all_chapters(novel_url):
    chapters = []
    page = 1

    while True:
        url = f"{novel_url}?page={page}"
        print(f"Loading: {url}")

        html = fetch_html(url)
        soup = BeautifulSoup(html, "html.parser")

        links = soup.select(".list-chapter li a")
        if not links:
            break

        for a in links:
            full = "https://novelfull.com" + a["href"]
            chapters.append(full)

        page += 1

    print(f"Total chapter ditemukan: {len(chapters)}")
    return chapters


# ====================================
# Filter range start → end
# ====================================
def filter_range(chapters, start, end):
    start_idx = chapters.index(start)
    end_idx = chapters.index(end)
    return chapters[start_idx:end_idx + 1]


# ====================================
# Scrape isi tiap chapter
# ====================================
def scrape_chapter(url):
    html = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")

    title = soup.select_one("span.chr-text")
    title = title.text.strip() if title else "Untitled"

    content = soup.select_one("#chapter-content")
    if not content:
        return title, "<p>(no content)</p>"

    # bersihkan style
    for tag in content.find_all():
        tag.attrs = {}

    return title, str(content)


# ====================================
# Buat EPUB
# ====================================
def build_epub(book_title, chapters, output):
    book = epub.EpubBook()

    book.set_identifier("novelfull-export")
    book.set_title(book_title)
    book.set_language("en")

    spine = ["nav"]
    toc_items = []

    for i, (title, html) in enumerate(chapters, 1):
        c = epub.EpubHtml(title=title, file_name=f"ch_{i}.xhtml")
        c.content = f"<h2>{title}</h2>{html}"

        book.add_item(c)
        spine.append(c)
        toc_items.append(c)

    book.toc = tuple(toc_items)
    book.spine = spine

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    epub.write_epub(output, book)
    print(f"\nSelesai → {output}")


# ====================================
# MAIN
# ====================================
def main():
    novel_url = "https://novelfull.com/i-might-be-a-fake-cultivator.html"

    start = "https://novelfull.com/i-might-be-a-fake-cultivator/chapter-1-why-is-this-immortal-so-happy.html"
    end = "https://novelfull.com/i-might-be-a-fake-cultivator/chapter-2399-end-extra-gate-of-truth-22.html"

    # Ambil semua chapter
    all_chapters = get_all_chapters(novel_url)

    # Filter start → end
    targets = filter_range(all_chapters, start, end)
    print(f"Total chapter to scrape: {len(targets)}")

    # Scrape satu per satu
    scraped = []
    for i, url in enumerate(targets, 1):
        print(f"Scraping {i}/{len(targets)} → {url}")
        title, html = scrape_chapter(url)
        scraped.append((title, html))
        time.sleep(0.5)

    # Generate EPUB
    build_epub("I Might Be A Fake Cultivator", scraped, "IMBAFC.epub")


if __name__ == "__main__":
    main()
