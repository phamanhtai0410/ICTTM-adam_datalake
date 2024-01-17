from airflow import DAG
from airflow.operators.python import PythonOperator
import requests
import os
from zipfile import ZipFile
import time
import datetime
from tqdm import tqdm
import boto3
from airflow.models import Variable
from airflow.exceptions import AirflowException

object_storage_access_key = Variable.get("objs3_access_key", "demo-access-key")
object_storage_secret_key = Variable.get("objs3_secret_key", 'demo-secret-key')
object_storage_endpoint = Variable.get("objs3_endpoint", "http://172.17.0.1:9000")


current_dir = os.path.dirname(os.path.abspath(__file__))

def get_gleif_data():
    print('GLEIF Crawling -------------------')
    url = "https://goldencopy.gleif.org/api/v2/golden-copies/publishes"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("API response: {}".format(response.status_code))
    
    gleif_data = response.json()
    data = gleif_data['data'][0]
    return data

def get_url_download_csv():
    data = get_gleif_data()
    url = data['lei2']['full_file']["csv"]["url"]
    size = data['lei2']['full_file']["csv"]["size"]
    return url, size

def download_file_from_url():
    """
    Download file from url
    """
    url_download, size = get_url_download_csv()
    file_name = url_download.split('/')[-1]
    
    # Check folder data exist or not, if not create folder data
    if not os.path.exists(os.path.join(current_dir, 'data-gleif')):
        os.makedirs(os.path.join(current_dir, 'data-gleif'))

    file_path = os.path.join(current_dir, 'data-gleif', file_name)
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
            return file_path
        
        except requests.exceptions.ChunkedEncodingError as e:
            if attempt < retries - 1:
                print("ChunkedEncodingError occurred. Retrying in {} seconds...".format(retry_delay))
                time.sleep(retry_delay)
            else:
                raise e
            
def extract_zip_file():
    """
    Extract zip file and rename CSV file to data.csv
    """
    # current_date = datetime.datetime.now().strftime("%Y%m%d")
    file_path = download_file_from_url()
    extract_folder = os.path.join(current_dir, 'data-gleif')
    with ZipFile(file_path, 'r') as zipObj:
        for file in zipObj.namelist():
            if file.endswith('.csv'):
                zipObj.extract(file, extract_folder)
                new_file_path = os.path.join(extract_folder, file)
                new_file_name = os.path.join(extract_folder, 'data.csv')
                os.rename(new_file_path, new_file_name)
    #Remove zip file after extract
    os.remove(file_path)
    return new_file_name

def upload_file_to_minio(file_path, minio_bucket, minio_object_name):
    try:
        s3c = boto3.resource('s3',
                            endpoint_url=object_storage_endpoint,
                            aws_access_key_id=object_storage_access_key,
                            aws_secret_access_key=object_storage_secret_key,
                            config=boto3.session.Config(signature_version='s3v4'),
                            verify=False
                            )
        s3c.Bucket(minio_bucket).upload_file(file_path, minio_object_name)
    except Exception as e:
        raise AirflowException(f"Failed to upload file to Minio: {str(e)}")
    
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
    upload_task = PythonOperator(
        task_id='upload_file',
        python_callable=upload_file_to_minio,
        op_kwargs={'file_path': os.path.join(current_dir, 'data-gleif', 'data.csv'), 
                   'minio_bucket': 'warehouse',
                   'minio_object_name': 'files/gleif.file/data.csv'}
    )

    download_task >> upload_task  # Set dependencies
    
if __name__ == "__main__":
    dag.test()