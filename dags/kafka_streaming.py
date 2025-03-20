from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator
from datetime import datetime
from faker import Faker
from json import dumps
from kafka import KafkaProducer
from random import uniform
from time import sleep
from typing import Any


default_args = {
    "owner": "airflow",
}

fake = Faker()


def generate_user():
    sleep(uniform(0.0, 1.5))
    
    return {
        "name": fake.name(),
        "email": fake.email(),
        "phone_number": fake.phone_number(),
        "address": fake.address(),
        "city": fake.city(),
        "postal_code": fake.postcode(),
        "dob": fake.date_of_birth().isoformat(),
        "company": fake.company(),
    }


def stream_user(user: dict[str, Any]):
    producer = KafkaProducer(
        bootstrap_servers="broker:29092",  # <-- Very important!
        value_serializer=lambda v: dumps(v).encode("utf-8"),
    )
    print(f"User: {user['name']}, Email: {user['email']}")
    producer.send("user", value=user)
    producer.flush()
    producer.close()


with DAG(
    dag_id="kafka_user_streaming",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule=None,  # You can change this to '*/5 * * * *' or similar
    catchup=False,
    tags=["kafka", "streaming"],
) as dag:

    streaming_task = PythonOperator(
        task_id="stream_user_from_faker", python_callable=stream_user
    )
