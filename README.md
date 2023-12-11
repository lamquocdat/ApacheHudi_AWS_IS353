# ApacheHudi_AWS_IS353
This is the IS353 UIT social networking subject project. The project uses Apache Hudi technology combined with AWS to store, process, and analyze the dataset to find central metrics and social network communities in the dataset.
# Architecture
![image](./Readme_Images/architecture.png)

Ingredients included:
* Datasource: a csv file taken from kaggle (link: https://www.kaggle.com/datasets/mdhamani/goodreads-books-100k)
* Hudi datalake:
    * Raw table (Bucket S3): where to save the original data
    * ETL jobs: get data from raw table and put it into derived table
    * Derived table (Table in AWS Glue): Contains processed data
* Loke Storage: where the project's data is stored, containing both raw tables and derived tables.
* Queries (AWS Athena): Tool used to query data.

# Works
The work performed in the project includes:
* Ingest: put data into S3 and go through ETL processing to put it into a table on Glue
* Process: explore the dataset such as checking for missing values, finding top 10 authors...
* Enrich: applying centrality measures and community finding algorithms to the dataset.

Project run in PyCharm.

# Handle dataset
* handle_dataset.py is used to put data into an S3 bucket.
* It will read each line of data in the csv file and reformat the header line, adding id and ts (timestamp) columns.
* It then converts the data in each line into a json file and posts it to S3.

# ETL jobs
In this project has 3 ETL job:
* Hudi-ingest-S3.py : this is code help us put data in S3.
* Hudi_upsert_job.py: ETL job update data.
* Hudi_delete_job.py: ETL delete data.
When create them, you have to config in "job details":

``````
Maximum concurency                      4 
hudi-connection
job parameters:
--conf              spark.serializer=org.apache.spark.serializer.KryoSerializer
--datalake-formats  hudi
``````

![image](./Readme_Images/maximun_concurency.png)

![image](./Readme_Images/hudi_connection.png)

![image](./Readme_Images/job_parameters.png)

# Programs call ETL jobs
We have 3 programs call 3 ETL jobs:
* Hudi-ingest-S3.py: call Hudi-ingest-S3.
* Hudi_upsert_job.py: call Hudi_upsert_job.
* Hudi_delete_job: call Hudi_delete_job.
These programs will transmit configurations and requests such as updates and deletions to ETL jobs.
ETL jobs will be based on configurations from input parameters and process data as required.

# Notebook
The results of the process and data enrichment are stored here.
Centrality measure algorithms in enrich:
* Degree Centrality
* Closeness Centrality
* Betweenness Centrality
* Page Rank
* Harmonic
* Eigenvector Centrality

Community discovery algorithms in enrich:
* Louvain

![image](./Readme_Images/Louvain.png)

* K-means

![image](./Readme_Images/Kmeans.png)

* Spectral Clusterin

![image](./Readme_Images/SpectralClusterin.png)

# Main.py
Used to check whether apache hudi can be used locally or not. You must install hudi before run this code.