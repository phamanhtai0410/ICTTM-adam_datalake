import random
import time
from itertools import cycle

from bs4 import BeautifulSoup
from engines.proxies_bank import proxies
from engines.print_helper import print_progress


def crawler(file_path, total_pages, max_retries_per_page, scraper, sleep_duration_on_success, url, page):
    start_time = time.time()  # Record the start time
    shuffled_proxies_list = proxies.copy()
    random.shuffle(shuffled_proxies_list)
    with open(file_path, 'w') as file:
        while page <= total_pages:
            current_retries = 0
            success = False

            while current_retries < max_retries_per_page and not success:
                try:
                    # Choose a random proxy for each request
                    proxy = {"http": f"https://{cycle(shuffled_proxies_list)}"}
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
            print_progress(page, total_pages, start_time, proxy)  # Print the progress
            page += 1  # Go to the next page regardless of success

    print("Finished scraping all pages or stopped due to errors.")
