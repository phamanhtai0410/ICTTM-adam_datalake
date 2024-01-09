# OpenSanctions Example with Apache Airflow and PySpark

This repository contains an example demonstrating the integration of Apache Airflow and PySpark to download and process
data from OpenSanctions. The example includes setting up the environment, creating an Airflow DAG for scheduled data
downloads and uploads to MinIO, and using a PySpark notebook to process and transform data stored in MinIO.

## 1. Prepare Environment

### Install Dependencies

Ensure you have the required dependencies installed:

```bash
./chmod +x requirements.apt.sh
./requirements.apt.sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.pip.txt
```

### Start Airflow Standalone

- Start Apache Airflow in standalone mode, open new terminal and type:

```bash
airflow webserver -p 8080
```

- Default username is "admin", password is located in file "~/airflow/standalone_admin_password.txt"

### Start Docker MinIO

Start MinIO using Docker, open new terminal and type:

```bash
docker compose -f docker_resources/minio-docker-compose.yml
```

- Open MinIO Web Interface  
  Open a web browser and navigate to http://localhost:9000. Log in with the following credentials:

```
Username: ROOTNAME  
Passw: CHANGEME123  
```

- Create New MinIO User Credentials  
  Click on the "Access Keys" menu on the left-hand side.
  Click on the "Create Access Key +" button.
  Enter a AccessKeys and SecretKeys with value below:

```
AccessKeys: demo-access-key 
SecretKeys:  demo-secret-key
```

- Click on the "Create" button.
- Create Bucket name "warehouse": Click on the "Buckets" menu on the left-hand side. Click "Create Bucket".

## 2. Dags example

- Copy file in folder dags to $HOME_AIRFLOW/dags folder, normally in ~/airflow. Maybe we need create:

```commandline
mkdir ~/airflow/dags
cp examples/example_opensanctions/dags/crawler_opensanction.py ~/airflow/dags
```

- Open Airflow Web Interface http://localhost:9000. Find your dags and run at first time
- Open MinIO Web Interface  http://localhost:9000. Check upload file and folders 