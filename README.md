<p align="center">
  <b><h1 align="center">Web Novel Scraper 📚</h1></b>
</p>

<p align="center">
A Python-based tool for scraping web novels and saving chapters into structured Word documents. This project also includes a utility to clean up blank lines from the content after scraping.
</p>

## Features 🚀

- Chapter Extraction: Automatically scrapes titles and content from web novel chapters.
- Pagination Handling: Navigates through multiple chapters using "Next Chapter" links.
- Content Cleaning: Removes unnecessary blank lines and ensures clean formatting.
- Word Document Export: Saves scraped chapters as `.docx` files for easy offline reading.
- Customizable Scraping: Allows you to specify start and end URLs to control the scraping range.

## Files 📂

- `webnovel_scraper.py`: Main script for scraping web novels and saving them as `.docx` files.
- `remove_empty_lines.py`: Utility to remove blank lines from the content after scraping.

## FRequirements ⚙️

- Python 3.7+
- Libraries:
	- `requests`
	- `beautifulsoup4`
	- `python-docx`

## Installation
1. Clone this repository:
	```bash
	git clone https://github.com/fedyrahmatullah/webnovel-scraper.git
	```
2. Navigate to the project directory:
	```bash
	cd webnovel-scraper
	```
3. Install dependencies:
	```bash
	pip install requests beautifulsoup4 python-docx
	```

## Usage 🛠️
1. Scraping Web Novel (webnovel_scraper.py)
	1. Open the script file (webnovel_scraper.py) in a text editor.
	2. Update the following variables:
		- `start_url`: The URL of the first chapter you want to scrape.
		- `end_url`: (Optional) The URL of the last chapter to scrape. If not provided, the scraper will continue until it can no longer find a "Next Chapter" link.
	3. Run the script:
	```bash
	python webnovel_scraper.py
	```
	4. The scraped content will be saved as a `.docx` file in the project directory.
2. Cleaning the Scraped Content (remove_empty_lines.py)
	1. After running webnovel_scraper.py, use remove_empty_lines.py to clean up blank lines in the scraped `.docx` file.
	2. Run the script:
	```bash
	python remove_empty_lines.py
	```
	This will remove unnecessary blank lines, especially after titles, and update the .docx file.
	
## File Output 📝
The output .docx file will include:
- Chapter titles formatted as headings.
- Chapter content in clean and organized paragraphs, free of unnecessary blank lines.

Example Output:
```text
Chapter 1: The Beginning
This is the content of Chapter 1.

Chapter 2: The Journey
This is the content of Chapter 2.
```
## Disclaimer ⚠️
This project is intended for educational purposes only. It demonstrates how web scraping techniques can be used to extract and organize data.

Important:
- This tool is not intended for illegal activities, such as pirating or redistributing copyrighted content from web novels or other sources.
- Always ensure you have permission from the website owner or follow their terms of service before using this scraper.
- The author of this repository is not responsible for any misuse of this tool.
- By using this project, you agree to use it ethically and in compliance with applicable laws and regulations.
