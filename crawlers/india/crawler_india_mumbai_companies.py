import cloudscraper
import random

from engines.crawler_engine import crawler


def main():
    # Create a CloudScraper instance
    scraper = cloudscraper.create_scraper()
    file_path = 'data/india_mumbai_roc_ageF.txt'  # File path to save the elements
    max_retries_per_page = 5  # Maximum number of retries for a page
    sleep_duration_on_success = random.uniform(0, 0.2)  # Duration to sleep after each successful response (in seconds)
    total_pages = 5921  # Total number of pages to scrape
    url_base = f"https://www.zaubacorp.com/company-list/age-F/roc-RoC-Mumbai/p-"
    page_start = 1
    crawler(file_path, total_pages, max_retries_per_page, scraper, sleep_duration_on_success, url_base, page_start)


if __name__ == "__main__":
    main()
