import cloudscraper
import random
from engines.crawler_engine import crawler_info_companies

def main():
    # Create a CloudScraper instance
    scraper = cloudscraper.create_scraper()
    input_file_path = 'url/india_mumbai_roc_ageB.txt'  # File path to get url (.txt file)
    output_file_path = 'url/infor_companies_mumbai_roc_age_B.json'  # File path to save url companies (.json file)

    max_retries_per_page = 5  # Maximum number of retries for a page
    sleep_duration_on_success = random.uniform(0, 0.2)  # Duration to sleep after each successful response (in seconds)

    crawler_info_companies(input_file_path, output_file_path, max_retries_per_page, scraper, sleep_duration_on_success)


if __name__ == "__main__":
    main()