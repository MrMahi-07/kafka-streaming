#!/bin/bash

pip install -r /opt/airflow/requirements.txt

airflow db init

# Check if the user already exists before creating
airflow users list | grep -q admin
if [ $? -ne 0 ]; then
  airflow users create \
    --username admin \
    --firstname admin \
    --lastname admin \
    --role Admin \
    --email admin@example.com \
    --password admin
fi

exec airflow webserver
