from airflow import DAG
from airflow.operators.python import PythonOperator

import boto3
import requests
from datetime import datetime
from airflow.models import Variable

object_storage_access_key = Variable.get("objs3_access_key", "demo-access-key")
object_storage_secret_key = Variable.get("objs3_secret_key", 'demo-secret-key')
object_storage_endpoint = Variable.get("objs3_endpoint", 'http://localhost:9000')

def download_file(url, file_path):
    response = requests.get(url, stream=True)
    with open(file_path, 'wb') as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)


def upload_file_to_minio(file_path, minio_bucket, minio_object_name):
    s3c = boto3.resource('s3',
                         endpoint_url=object_storage_endpoint,
                         aws_access_key_id=object_storage_access_key,
                         aws_secret_access_key=object_storage_secret_key,
                         config=boto3.session.Config(signature_version='s3v4'),
                         verify=False
                         )
    s3c.Bucket(minio_bucket).upload_file(file_path, minio_object_name)


with DAG(
        dag_id='download_and_upload_file',
        start_date=datetime(2023, 12, 23),
        schedule=None,
        catchup=False
) as dag:
    download_task = PythonOperator(
        task_id='download_file',
        python_callable=download_file,
        op_kwargs={'url': 'https://data.opensanctions.org/datasets/20240109/default/entities.ftm.json',
                   'file_path': '/tmp/source.json'}
    )

    upload_task = PythonOperator(
        task_id='upload_file',
        python_callable=upload_file_to_minio,
        op_kwargs={'file_path': '/tmp/source.json', 'minio_bucket': 'warehouse',
                   'minio_object_name': 'files/opensanctions.file/entities.ftm.json'}
    )

    download_task >> upload_task  # Set dependencies

if __name__ == "__main__":
    dag.test()
    # dag.cli()
