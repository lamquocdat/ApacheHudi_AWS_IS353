# ApacheHudi_AWS_IS353
This is the IS353 UIT social networking subject project. The project uses Apache Hudi technology combined with AWS to store, process, and analyze the dataset to find central metrics and social network communities in the dataset.
## Architecture

<p align="center">
  <img src="./Readme_Images/architecture.png" alt="architecture"/>
</p>

Ingredients included:
* Datasource: a csv file taken from kaggle (link: https://www.kaggle.com/datasets/mdhamani/goodreads-books-100k)
* Hudi datalake:
    * Raw table (Bucket S3): where to save the original data
    * ETL jobs: get data from raw table and put it into derived table
    * Derived table (Table in AWS Glue): Contains processed data
* Loke Storage: where the project's data is stored, containing both raw tables and derived tables.
* Queries (AWS Athena): Tool used to query data.

## Works
The work performed in the project includes:
* Ingest: put data into S3 and go through ETL processing to put it into a table on Glue
* Process: explore the dataset such as checking for missing values, finding top 10 authors...
* Enrich: applying centrality measures and community finding algorithms to the dataset.

Project run in PyCharm.

## Handle dataset
* handle_dataset.py is used to put data into an S3 bucket. This program is run from local.
* It will read each line of data in the csv file and reformat the header line, adding id and ts (timestamp) columns.
* It then converts the data in each line into a json file and posts it to S3.

## ETL jobs
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

<p align="center">
  <img src="./Readme_Images/maximun_concurency.png" alt="maximun concurency"/>
</p>

<p align="center">
  <img src="./Readme_Images/hudi_connection.png" alt="hudi connection"/>
</p>

<p align="center">
  <img src="./Readme_Images/job_parameters.png" alt="job parameters"/>
</p>

## Programs call ETL jobs
We have 3 local programs call 3 ETL jobs on AWS Glue:
* Hudi-ingest-S3.py: call Hudi-ingest-S3.
* Hudi_upsert_job.py: call Hudi_upsert_job.
* Hudi_delete_job: call Hudi_delete_job.
These programs will transmit configurations and requests such as updates and deletions to ETL jobs.
ETL jobs will be based on configurations from input parameters and process data as required.

To run these programs, you need to create an .env file by copying the content in .env.example file. 
Then save the authentication keys on AWS (ACCESS_KEY, SECRET_KEY, REGION_NAME) into .env file.
## Notebook
Process_Enrich.ipynb is results of the Data Processing and Data Enrichment.
In Data Processing includes:
* Data exploration
* Statistics and handling of missing values
* Find the values that appear most often in the top 10.

Centrality measure algorithms in Enrich:
* Degree Centrality
* Closeness Centrality
* Betweenness Centrality
* Page Rank
* Harmonic
* Eigenvector Centrality

Community discovery algorithms in Enrich:
* Louvain

<p align="center">
  <img src="./Readme_Images/Louvain.png" alt="Louvain"/>
</p>

* K-means

<p align="center">
  <img src="./Readme_Images/Kmeans.png" alt="Kmeans" />
</p>

* Spectral Clusterin

<p align="center">
  <img src="./Readme_Images/SpectralClusterin.png" alt="Spectral Clusterin"/>
</p>

## Main.py
Used to check whether apache hudi can be used locally or not. You must install Apache Hudi before run this code.