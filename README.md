# adam_datalake

Lakehouse for data of AdamKYC, AdamFtd and so on

### 1. What is data lake?
Vietnamese: https://bizflycloud.vn/tin-tuc/data-lake-la-gi-phan-biet-data-lake-voi-data-warehouse-20220516174403628.htm  
English: https://www.databricks.com/discover/data-lakes  


### 2. Different between data lake and data warehouse
Vietnamese: https://bizflycloud.vn/tin-tuc/data-lake-la-gi-phan-biet-data-lake-voi-data-warehouse-20220516174403628.htm  
English: https://aws.amazon.com/compare/the-difference-between-a-data-warehouse-data-lake-and-data-mart  

### 3. Why data lake?
Vietnamese: https://renovacloud.com/data-lake-la-gi/
English: https://www.confluent.io/learn/databases-data-lakes-and-data-warehouses-compared

## About this repository
Welcome to the Data Lake repository! A Data Lake is a centralized repository that allows you to store and manage vast
amounts of raw data in its native format until it's needed. This repository is designed to help you understand the
concept of a Data Lake and provide examples to get you started.  

## Folder Structure
#### 1. `dags/`

This folder contains all the Directed Acyclic Graphs (DAGs) representing different data pipelines. Each DAG is defined in a separate Python file.

#### 2. `notebooks/`

The `notebooks` folder contains Jupyter notebooks with PySpark code for operating on data in the data lake. These notebooks can be used for exploratory data analysis, data transformation, and other tasks related to data processing.

#### 3. `examples/`

The `examples` folder provides practical demonstrations of how to iterate over a data source and process data. It includes sample scripts or notebooks showcasing specific use cases or scenarios.

#### 4. `devops/`

The `devops` folder contains instructions and configurations for setting up the project in a DevOps environment. It includes information on deployment, continuous integration, and other DevOps-related practices.

#### 5. `crawlers/`

The `crawlers` folder contains source code for crawlers and instructions for setting them up locally or on a server. Crawlers are responsible for retrieving data from external sources.

## Getting Started

### Setup
1. Install packages

```bash
./chmod +x requirements.apt.sh
./requirements.apt.sh
```

2. Setup and activate virtualenv
bash
```commandline
python -m venv venv
source venv/bin/activate
```

3. Install libraries
```bash
pip install -r requirements.pip.txt
```

### Naming Convention
Dag: action_datasource  
Ex1: crawler_lavita_companies.py  
Ex2: crawler_update_lavita_companies.py

Notebooks: datasource  
Ex1: bol.ipynb  
Ex2: openownership.ipynb