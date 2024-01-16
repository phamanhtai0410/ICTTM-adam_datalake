import cloudscraper
import random
from engines.crawler_engine import crawler_info_companies

def main():
    # Create a CloudScraper instance
    scraper = cloudscraper.create_scraper()
    input_file_path = 'data/sample.txt'  # File path to get url (.txt file)
    output_file_path = 'data/infor_companies_Ahmedabad.json'   # File path to save data companies (.json file)
    index_file = 'data/index.txt'
    idx_company = 0
    max_retries_per_page = 5  # Maximum number of retries for a page
    sleep_duration_on_success = random.uniform(0, 0.2)  # Duration to sleep after each successful response (in seconds)

    crawler_info_companies(input_file_path, output_file_path,index_file, max_retries_per_page, scraper, sleep_duration_on_success)


if __name__ == "__main__":
    main()