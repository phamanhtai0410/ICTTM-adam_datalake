# India Company Crawler

This Python script crawls the Zauba Corp website to extract company listing data from pages pertaining to companies registered in India.

It uses the Cloudscraper library to perform HTTP requests with randomized user-agent headers and TLS/SSL protocols to bypass certain anti-bot protections. Proxies are also cycled randomly for each request to avoid detection.

## Logic Process

    Initialize start time and shuffled proxy list
    
    Loop from page to total_pages
    
        Set retry count and success flag
    
        Retry request with random proxy until success or max retries
    
            Scrape data on success and write to file
    
            Sleep, handle errors, increment retry count on failure
    
        Print progress
    
        Increment page number
    
    Print finished message

### Logic Diagram
![alt text](diagram/crawler_indian_companies.svg)

## Usage

Copy new crawler, rename it depend on RoC-City.

Update the configuration variables at the top of crawler_india_{city}_companies.py file:

file_path: Path to save scraped data

max_retries_per_page: Maximum retries per page

sleep_duration_on_success: Sleep duration after successful scrape

total_pages: Total number of pages to scrape

page_start: Starting page number

url: Base URL template string


### Run the scraper:

Example:
```commandline
python3 crawler_india_kanpur_companies.py
```
The output will be scraped company links/data saved to the specified file path. It will cycle through randomly selected proxy servers on each request to avoid detection.

Progress is printed periodically to stdout including elapsed/estimated remaining time.

Notes:

Increase sleep_duration_on_success for less aggressive scraping to avoid getting blocked

Reduce max_retries_per_page if failing too often to avoid excessive retries

Increase concurrency by launching multiple scraper instances with different page_start/end chunks


### Alert
Let me know if any other part of the documentation needs explanation or improvement!

#### Contact
Long Phan (ICTTM)

Email: long@icttm.net