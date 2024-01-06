from datetime import datetime, timedelta
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow import DAG
import requests
import boto3
from botocore.exceptions import NoCredentialsError
from airflow.models import Variable

object_storage_access_key = Variable.get("objs3_access_key")
object_storage_secret_key = Variable.get("objs3_secret_key")
object_storage_endpoint = Variable.get("objs3_endpoint")

class DownloadFileOperator(BaseOperator):
    """
    Custom operator to download a file from a URL.
    """

    @apply_defaults
    def __init__(self, url, *args, **kwargs):
        super(DownloadFileOperator, self).__init__(*args, **kwargs)
        self.url = url

    def execute(self, context):
        # Download the file from the URL in chunks
        chunk_size = 1024  # Set your desired chunk size
        downloaded_content = bytearray()

        with requests.get(self.url, stream=True) as response:
            for chunk in response.iter_content(chunk_size=chunk_size):
                downloaded_content.extend(chunk)

        return bytes(downloaded_content)


class UploadToObjectStorageOperator(BaseOperator):
    """
    Custom operator to upload a file to generic object storage (S3-compatible).
    """

    @apply_defaults
    def __init__(self, object_storage_access_key, object_storage_secret_key, object_storage_bucket,
                 object_storage_endpoint, *args, **kwargs):
        super(UploadToObjectStorageOperator, self).__init__(*args, **kwargs)
        self.object_storage_access_key = object_storage_access_key
        self.object_storage_secret_key = object_storage_secret_key
        self.object_storage_bucket = object_storage_bucket
        self.object_storage_endpoint = object_storage_endpoint

    def execute(self, context, downloaded_content):
        # Upload the file to object storage in chunks
        try:
            s3 = boto3.client('s3',
                              aws_access_key_id=self.object_storage_access_key,
                              aws_secret_access_key=self.object_storage_secret_key,
                              endpoint_url=self.object_storage_endpoint
                              )

            # Upload the file
            chunk_size = 5 * 1024 * 1024  # Set your desired chunk size for object storage
            for i in range(0, len(downloaded_content), chunk_size):
                chunk = downloaded_content[i:i + chunk_size]
                s3.upload_part(Body=chunk, Bucket=self.object_storage_bucket, Key='uploaded_file.txt',
                               PartNumber=i // chunk_size + 1)

            # Complete the multipart upload
            s3.complete_multipart_upload(Bucket=self.object_storage_bucket, Key='uploaded_file.txt', UploadId=None)

            self.log.info("File uploaded to object storage successfully.")

        except NoCredentialsError:
            self.log.error("Credentials not available.")

        except Exception as e:
            self.log.error(f"Error uploading file to object storage: {str(e)}")
            raise e


# Define your DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    # 'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'download_and_upload_to_object_storage',
    default_args=default_args,
    description='A DAG to download a large file and upload it to object storage (S3-compatible)',
)

# Create instances of the custom operators
download_task = DownloadFileOperator(
    task_id='download_task',
    url='https://example.com/path/to/large_file.txt',
    dag=dag,
)

upload_task = UploadToObjectStorageOperator(
    task_id='upload_task',
    object_storage_access_key='your-access-key',
    object_storage_secret_key='your-secret-key',
    object_storage_bucket='your-bucket-name',
    object_storage_endpoint='http://your-object-storage-endpoint',  # Replace with your object storage endpoint
    dag=dag,
)

# Set the task dependencies
download_task >> upload_task
