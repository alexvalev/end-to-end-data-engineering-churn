# End-to-End Data Engineering Platform for Customer Churn Prediction

## Overview
This project demonstrates an end-to-end data engineering and machine learning workflow using Databricks, SQL, dbt, and MLflow. The goal is to build a scalable analytics platform that ingests raw data, transforms it into analytics-ready models, and deploys a machine learning model to predict customer churn.

## Business Problem
Customer churn is a critical metric for subscription-based businesses. This project answers the question:

> Which customers are likely to churn in the next 30 days?

## Architecture
The platform follows a Medallion Architecture:

- **Bronze**: Raw ingested data
- **Silver**: Cleaned and standardized data
- **Gold**: Analytics-ready tables and ML features

Technologies used:
- Databricks (Spark, Delta Lake)
- SQL & Python
- dbt (analytics engineering)
- MLflow (model tracking)

## Data Flow
1. Raw data is ingested into Delta Lake (Bronze)
2. Data is cleaned and standardized (Silver)
3. Business models and feature tables are created (Gold)
4. A machine learning model is trained and logged using MLflow
5. Batch predictions are written back to Gold tables

## dbt Lineage
![dbt lineage](images/dbt_dag.png)

## Limitations
This project uses Databricks Community Edition, which does not support job scheduling or production clusters. Orchestration is simulated through notebook execution order and documentation.

## Repository Structure
See the folder structure for notebooks, dbt models, and documentation.

## Future Improvements
- Add job orchestration using Databricks Jobs or Airflow
- Deploy real-time inference API
- Add CI/CD for dbt

