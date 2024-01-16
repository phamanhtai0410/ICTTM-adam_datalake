import cloudscraper
import random

from engines.crawler_engine import crawler


def main():
    # Create a CloudScraper instance
    scraper = cloudscraper.create_scraper()
    file_path = 'data/india_kanpur.txt'  # File path to save the elements
    max_retries_per_page = 5  # Maximum number of retries for a page
    sleep_duration_on_success = random.uniform(0, 0.2)  # Duration to sleep after each successful response (in seconds)
    total_pages = 5920  # Total number of pages to scrape
    page_start = 1
    url = f"https://www.zaubacorp.com/company-list/roc-RoC-Kanpur/p-"
    crawler(file_path, total_pages, max_retries_per_page, scraper, sleep_duration_on_success, url, page_start)


if __name__ == "__main__":
    main()
