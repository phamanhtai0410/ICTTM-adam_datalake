import cloudscraper
from bs4 import BeautifulSoup
import time
import random
from datetime import timedelta
def print_progress(current_page, total_pages, start_time):
    elapsed_time = time.time() - start_time
    pages_left = total_pages - current_page
    average_time_per_page = elapsed_time / current_page
    estimated_time_remaining = pages_left * average_time_per_page

    formatted_elapsed_time = str(timedelta(seconds=elapsed_time)).split(".")[0]  # Remove microseconds
    formatted_estimated_remaining = str(timedelta(seconds=estimated_time_remaining)).split(".")[
        0]  # Remove microseconds
    progress = (current_page / total_pages) * 100

    print(
        f"Progress: {progress:.2f}% ({current_page}/{total_pages}) - Elapsed Time: {formatted_elapsed_time} - Remaining Time: {formatted_estimated_remaining}",
        end='\r', flush=True)
def main():
    proxies = [
    '38.154.227.167:5868',
    '185.199.229.156:7492',
    '185.199.228.220:7300',
    '185.199.231.45:8382',
    '188.74.210.207:6286',
    '188.74.183.10:8279',
    '188.74.210.21:6100',
    '45.155.68.129:8133',
    '154.95.36.199:6893',
    '45.94.47.66:8110',
    ]
    # Create a CloudScraper instance
    scraper = cloudscraper.create_scraper()

    file_path = 'url/page_india_Bangalore_roc.txt'  # File path to save the elements

    max_retries_per_page = 5  # Maximum number of retries for a page
    sleep_duration_on_success = 0.5  # Duration to sleep after each successful response (in seconds)
    page_count = 6072
    start_time = time.time() 
    def get_random_proxy(proxies):
        return random.choice(proxies) if proxies else None


    with open(file_path, 'w') as file:
        page = 1
        while page < page_count + 1:
            current_retries = 0
            success = False

            while current_retries < max_retries_per_page and not success:
                try:
                    if not proxies:
                        print("All proxies are banned or not working.")
                        break
                    else :
                        proxy = {"http": f"http://{get_random_proxy(proxies)}"}
                        url = f"https://www.zaubacorp.com/company-list/roc-RoC-Bangalore/p-{page}-company.html"
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
                        elif response.status_code == 403:  # If the proxy is banned
                            proxies.remove(proxy)  # Remove the banned proxy from the list
                            print(f"Proxy {proxy} banned, switching proxy.")
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
            else:
                print_progress(page, page_count, start_time)
                page += 1  # Only increment the page number if the page was successfully scraped

    print("Finished scraping all pages or stopped due to errors.")
if __name__ == "__main__":
    main()