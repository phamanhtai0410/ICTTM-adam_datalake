from airflow import DAG
from airflow.operators.python import PythonOperator
import requests
from tqdm import tqdm
import os
from zipfile import ZipFile
import time
import datetime
import boto3
from airflow.models import Variable
from airflow.exceptions import AirflowException

object_storage_access_key = Variable.get("objs3_access_key", "demo-access-key")
object_storage_secret_key = Variable.get("objs3_secret_key", 'demo-secret-key')
object_storage_endpoint = Variable.get("objs3_endpoint", "http://172.17.0.1:9000")

current_dir = os.path.dirname(os.path.abspath(__file__))
#Get api https://date.gov.md/ckan/ro/dataset/11736-date-din-registrul-de-stat-al-unitatilor-de-drept-privind-intreprinderile-inregistrate-in-repu

def get_moldova_data():
    print('Moldova Crawling -------------------')
    url = "https://date.gov.md/ckan/ro/dataset/11736-date-din-registrul-de-stat-al-unitatilor-de-drept-privind-intreprinderile-inregistrate-in-repu"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("API response: {}".format(response.status_code))
    # find .xlsx file in //*[@id="dataset-resources"]
    files = response.text.split('href="')
    result = None
    for file in files:
        if '.xlsx' in file and "/date.gov.md/ro/system/files/resources/" in file:
            file = file.split('"')[0]
            # print(file)
            result = file
    return result

def get_url_download_xlsx():
    data = get_moldova_data()
    url = data
    return url , 0

def download_file_from_url():
    """
    Download file from url
    """
    url_download, size = get_url_download_xlsx()
    file_name = url_download.split('/')[-1]
    # current_date = datetime.datetime.now().strftime("%Y%m%d")
    
    # Check folder data exist or not, if not create folder data
    if not os.path.exists(os.path.join(current_dir, 'data-moldova')):
        os.makedirs(os.path.join(current_dir, 'data-moldova'))
        
    file_path = os.path.join(current_dir, 'data-moldova', file_name)
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
            new_file_path = os.path.join(current_dir, 'data-moldova', 'data.csv')
            os.rename(file_path, new_file_path)
            return file_path
        
        except requests.exceptions.ChunkedEncodingError as e:
            if attempt < retries - 1:
                print("ChunkedEncodingError occurred. Retrying in {} seconds...".format(retry_delay))
                time.sleep(retry_delay)
            else:
                raise e

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
        dag_id='moldova_crawler',
        start_date=datetime.datetime(2023, 12, 23),
        schedule=None,
        catchup=False
) as dag:
    # download_task = PythonOperator(
    #     task_id='download_file',
    #     python_callable=download_file_from_url,
    # )
    upload_task = PythonOperator(
        task_id='upload_file',
        python_callable=upload_file_to_minio,
        op_kwargs={'file_path': os.path.join(current_dir, 'data-moldova', 'data.csv'), 
                   'minio_bucket': 'warehouse',
                   'minio_object_name': 'files/moldova.file/data.csv'}
    )

    # download_task >> upload_task  # Set dependencies
    
if __name__ == "__main__":
    dag.test()