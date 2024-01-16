from airflow import DAG
from airflow.operators.python import PythonOperator
import requests
from tqdm import tqdm
import os
from zipfile import ZipFile
import time
import datetime
current_dir = os.path.dirname(os.path.abspath(__file__))

def get_gov_au_data():
    print('GLEIF Crawling -------------------')
    url = "https://data.gov.au/data/api/3/action/package_show?id=7b8656f9-606d-4337-af29-66b89b2eeefb"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("API response: {}".format(response.status_code))
    
    gleif_data = response.json()
    data = gleif_data['result']['resources']
    return data

def get_url_download_csv():
    data = get_gov_au_data()
    url = None
    for i in data:
        if i.get('datastore_contains_all_records_of_source_file') == True:
            url = i['url']
    return url, 0

def download_file_from_url():
    """
    Download file from url
    """
    url_download, size = get_url_download_csv()
    file_name = url_download.split('/')[-1]
    
    # Check folder data exist or not, if not create folder data
    if not os.path.exists(os.path.join(current_dir, 'data-gov-au')):
        os.makedirs(os.path.join(current_dir, 'data-gov-au'))
        
    file_path = os.path.join(current_dir, 'data-gov-au', file_name)
    print('file_path', file_path)
    
    retries = 3  # Number of retries
    retry_delay = 5  # Delay between retries in seconds
    
    for attempt in range(retries):
        try:
            response = requests.get(url_download, stream=True)
            if response.status_code != 200:
                raise Exception("API response: {}".format(response.status_code))
            
            block_size = 1024  # 1 KB
            progress_bar = tqdm(total=size, unit='B', unit_scale=True)
            
            with open(file_path, 'wb') as file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)
            
            progress_bar.close()
            
            # Rename the file to data.csv
            new_file_path = os.path.join(current_dir, 'data-gov-au', 'data.csv')
            os.rename(file_path, new_file_path)
            
            return new_file_path
        
        except requests.exceptions.ChunkedEncodingError as e:
            if attempt < retries - 1:
                print("ChunkedEncodingError occurred. Retrying in {} seconds...".format(retry_delay))
                time.sleep(retry_delay)
            else:
                raise e

with DAG(
        dag_id='gov_au_crawler',
        start_date=datetime.datetime(2023, 12, 23),
        schedule=None,
        catchup=False
) as dag:
    download_task = PythonOperator(
        task_id='download_file',
        python_callable=download_file_from_url,
    )
    
if __name__ == "__main__":
    dag.test()