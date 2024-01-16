from datetime import timedelta
import time


def print_progress(current_page, total_pages, start_time, proxy_url):
    elapsed_time = time.time() - start_time
    pages_left = total_pages - current_page
    average_time_per_page = elapsed_time / current_page
    estimated_time_remaining = pages_left * average_time_per_page

    formatted_elapsed_time = str(timedelta(seconds=elapsed_time)).split(".")[0]  # Remove microseconds
    formatted_estimated_remaining = str(timedelta(seconds=estimated_time_remaining)).split(".")[0]  # Remove
    # microseconds
    progress = (current_page / total_pages) * 100
    proxy_url_string = proxy_url.split("://")[1].split(":")[0]
    print(
        f"Progress: {progress:.2f}% ({current_page}/{total_pages}) - Elapsed Time: {formatted_elapsed_time} - "
        f"Remaining Time: {formatted_estimated_remaining} - "
        f"Using proxy: {proxy_url_string}",
        end='\r', flush=True
    )
