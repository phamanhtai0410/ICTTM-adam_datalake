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

### Folder Structure
#### 1. `dags/`

This folder contains all the Directed Acyclic Graphs (DAGs) representing different data pipelines. Each DAG is defined in a separate Python file.

#### 2. `notebooks/`

The `notebooks` folder contains Jupyter notebooks with PySpark code for operating on data in the data lake. These notebooks can be used for exploratory data analysis, data transformation, and other tasks related to data processing.

#### 3. `examples/`

The `examples` folder provides practical demonstrations of how to iterate over a data source and process data. It includes sample scripts or notebooks showcasing specific use cases or scenarios.

### 6. `docs/`

Documentation related to the project, including DAG documentation, operator documentation, or any other relevant information, can be found in this folder.


## Examples
### 1. Data Ingestion