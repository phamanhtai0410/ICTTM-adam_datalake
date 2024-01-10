import requests
from tqdm import tqdm
import os
from zipfile import ZipFile
import time
import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

current_dir = os.path.dirname(os.path.abspath(__file__))

def get_gleif_data():
    """
    Get GLEIF data from API
    """
    print('GLEIF Crawling -------------------')
    url = "https://goldencopy.gleif.org/api/v2/golden-copies/publishes"
    response = requests.get(url)
    response.raise_for_status()
    
    gleif_data = response.json()
    data = gleif_data['data'][0]
    return data

def get_url_download_csv():
    """
    Get URL and size of the CSV file to download
    """
    data = get_gleif_data()
    url = data['lei2']['full_file']["csv"]["url"]
    size = data['lei2']['full_file']["csv"]["size"]
    return url, size

def download_file_from_url():
    """
    Download file from URL.

    This function downloads a file from a given URL and saves it to the local file system.
    It creates necessary folders if they don't exist and handles retries in case of network errors.

    Returns:
        str: The file path of the downloaded file.
    """
    url_download, size = get_url_download_csv()
    file_name = url_download.split('/')[-1]
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    
    # Check if the 'data' folder exists, if not create it
    data_folder = os.path.join(current_dir, 'data')
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    
    # Check if the current date folder exists, if not create it
    current_date_folder = os.path.join(data_folder, current_date)
    if not os.path.exists(current_date_folder):
        os.makedirs(current_date_folder)
        
    file_path = os.path.join(current_date_folder, file_name)
    print('file_path', file_path)
    
    retries = 3  # Number of retries
    retry_delay = 5  # Delay between retries in seconds
    
    for attempt in range(retries):
        try:
            response = requests.get(url_download, stream=True)
            response.raise_for_status()
            
            block_size = 1024  # 1 KB
            progress_bar = tqdm(total=size, unit='B', unit_scale=True)
            
            with open(file_path, 'wb') as file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)
            
            progress_bar.close()
            return file_path
        
        except requests.exceptions.ChunkedEncodingError as e:
            if attempt < retries - 1:
                print("ChunkedEncodingError occurred. Retrying in {} seconds...".format(retry_delay))
                time.sleep(retry_delay)
            else:
                raise e
            
def extract_zip_file():
    """
    Extract zip file
    """
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    file_path = download_file_from_url()
    folder_name = os.path.splitext(os.path.basename(file_path))[0]
    extract_folder = os.path.join(current_dir, 'data', current_date, folder_name)
    with ZipFile(file_path, 'r') as zipObj:
        zipObj.extractall(extract_folder)
    return file_path


with DAG(
        dag_id='gleif_crawler',
        start_date=datetime.datetime(2023, 12, 23),
        schedule=None,
        catchup=False
) as dag:
    download_task = PythonOperator(
        task_id='download_file',
        python_callable=extract_zip_file,
    )
    
if __name__ == "__main__":
    dag.test()