import random
import time
from itertools import cycle
import json
import signal

from bs4 import BeautifulSoup
from engines.tool.proxies_bank import proxies
from engines.tool.print_helper import print_progress
from engines.tool.support import decode_email, scrape_infor_page_company, filter_company


def crawler(file_path, total_pages, max_retries_per_page, scraper, sleep_duration_on_success, url_base, page):
    start_time = time.time()  # Record the start time
    shuffled_proxies_list = proxies
    random.shuffle(shuffled_proxies_list)
    proxy_cycle = cycle(shuffled_proxies_list)
    with open(file_path, 'w') as file:
        while page <= 20:
            current_retries = 0
            success = False
            url = f"{url_base}{page}-company.html"
            while current_retries < max_retries_per_page and not success:
                try:
                    # Choose a random proxy for each request
                    proxy_iter = next(proxy_cycle)
                    proxy = {"http": f"https://{proxy_iter}"}
                    response = scraper.get(url, proxies=proxy)
                    # Check if we got a successful response
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        table = soup.find('table', class_='table table-striped col-md-12 col-sm-12 col-xs-12')

                        if table:
                            links = table.find_all('a')
                            for link in links:
                                file.write(link.get('href') + '\n')  # Write each link to the file

                            success = True  # Mark this page as successfully scraped
                            time.sleep(sleep_duration_on_success)  # Sleep after a successful scrape
                        else:
                            print(f"No table found on page {page}.")
                            break  # Stop the loop if no table is found
                    else:
                        print(f"Failed to retrieve page {page}: HTTP {response.status_code}")
                        raise Exception(f"HTTP Error: {response.status_code}")

                except Exception as e:
                    current_retries += 1
                    print(f"An error occurred for page {page}: {str(e)}")
                    print(f"Attempt {current_retries} of {max_retries_per_page}. Retrying with a new proxy...")
                    time.sleep(5)  # Wait for 5 seconds before retrying with a new proxy

            if not success:
                print(f"Failed to scrape page {page} after {max_retries_per_page} attempts.")
                # Decide whether to break or continue with the next page
                # break  # Uncomment this if you want to stop scraping completely

            print_progress(page, total_pages, start_time, proxy["http"])  # Print the progress
            page += 1  # Go to the next page regardless of success

    print("Finished scraping all pages or stopped due to errors.")


def crawler_info_companies(input_file_path, output_file_path, max_retries_per_page, scraper, sleep_duration_on_success):
    with open(input_file_path, 'r') as input_file:
        urls_companies = [line.strip() for line in input_file.readlines()]

    idx_company = 0
    total_companies = len(urls_companies)

    start_time = time.time()  # Record the start time
    shuffled_proxies_list = proxies.copy()
    random.shuffle(shuffled_proxies_list)
    proxy_cycle = cycle(shuffled_proxies_list)

    with open(output_file_path, 'a') as output_file:
        while idx_company < total_companies:
            current_retries = 0
            success = False
            while current_retries < max_retries_per_page and not success:
                try:
                    # Choose a random proxy for each request
                    proxy_iter = next(proxy_cycle)
                    proxy = {"http": f"https://{proxy_iter}"}
                    response = scraper.get(urls_companies[idx_company], proxies=proxy)
                    # Check if we got a successful response
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        company_infor = scrape_infor_page_company(soup)

                        company_infor = filter_company(company_infor)

                        json.dump(company_infor, output_file)
                        output_file.write('\n')

                        success = True  # Mark this page as successfully scraped
                        time.sleep(sleep_duration_on_success)  # Sleep after a successful scrape
                    else:
                        print(f"Failed to retrieve page {idx_company}: HTTP {response.status_code}")
                        raise Exception(f"HTTP Error: {response.status_code}")

                except Exception as e:
                    current_retries += 1
                    print(f"An error occurred for page {idx_company}: {str(e)}")
                    print(f"Attempt {current_retries} of {max_retries_per_page}. Retrying with a new proxy...")
                    time.sleep(5)  # Wait for 5 seconds before retrying with a new proxy

            if not success:
                print(f"Failed to scrape page {idx_company} after {max_retries_per_page} attempts.")
                # Decide whether to break or continue with the next page
                # break  # Uncomment this if you want to stop scraping completely
            idx_company += 1  # Go to the next page regardless of success
            print_progress(idx_company, total_companies, start_time, proxy["http"])  # Print the progress

    print("Finished scraping all pages or stopped due to errors.")
