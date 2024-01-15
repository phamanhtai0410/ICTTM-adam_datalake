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

This folder contains all the Directed Acyclic Graphs (DAGs) representing different data pipelines. Each DAG is defined
in a separate Python file.

#### 2. `notebooks/`

The `notebooks` folder contains Jupyter notebooks with PySpark code for operating on data in the data lake. These
notebooks can be used for exploratory data analysis, data transformation, and other tasks related to data processing.

#### 3. `examples/`

The `examples` folder provides practical demonstrations of how to iterate over a data source and process data. It
includes sample scripts or notebooks showcasing specific use cases or scenarios.

#### 4. `devops/`

The `devops` folder contains instructions and configurations for setting up the project in a DevOps environment. It
includes information on deployment, continuous integration, and other DevOps-related practices.

#### 5. `crawlers/`

The `crawlers` folder contains source code for crawlers and instructions for setting them up locally or on a server.
Crawlers are responsible for retrieving data from external sources.

#### 6. `tools/`

The `tools` folder contains some tools helpful for developer.

#### 7. `docs/`

The `docs` folder documents about how each data source is crawled and processed

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

- For files in `dags/` folder: `action`_`datasource`  
  - Ex1: crawler_lavita_companies.py  
  - Ex2: crawler_update_lavita_companies.py

- For files in `notebooks/` folder: `(action)`_`datasource`  
  - Ex1: pipeline_bol.ipynb or bol.ipynb

### Definition

- **Crawler**: Is a task that runs once, or periodically, to get data from an external source to our datalake. Crawlers
  can run locally, on private servers, or on datalake dags.
- **Pipeline**: Pipeline typically refers to a data processing workflow that involves a series of steps to extract,
  transform, and load (ETL) data from one stage to another.
- **Layer/Data Layer**: These layers are part of a Data Lakehouse or a Data Warehouse architecture, and the concept is
  aligned with principles of data governance, data quality, and data processing. The idea behind using different layers
  is to create a structured approach to data processing, ensuring that raw data is preserved, intermediate stages allow
  for quality improvements, and the final stage provides a reliable and optimized data set for analytics and reporting.
    - **Bronze Layer**: Raw and unprocessed data ingested directly from various sources. It's a folder in bucket
    - **Silver Layer**: Intermediate stage where data undergoes cleansing and transformation for improved quality. It's a
      folder in bucket
    - **Gold Layer**: Final stage with optimized data for efficient analytics and reporting. It's a folder in bucket
- **Table/Delta table**: A table is a structured and distributed collection of data, organized in rows and columns, used
  for analysis and processing. It serves as a logical representation of structured data that can be queried and
  manipulated using SQL or programming languages like Python and Scala. In object storage, it's a collection of parquet
  files and metadata json files