from airflow import DAG
from airflow.decorators import task
from datetime import datetime
from faker import Faker
from json import dumps
from kafka import KafkaProducer
from random import uniform
from time import sleep, time
from typing import Any
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


default_args = {
    "owner": "airflow",
}

fake = Faker()


def generate_user():
    sleep(uniform(2, 5))

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


def stream_user():
    producer = KafkaProducer(
        bootstrap_servers="broker:29092",  # <-- Very important!
        value_serializer=lambda v: dumps(v).encode("utf-8"),
    )

    start_time = time()
    while (time() - start_time) < 560:

        user = generate_user()

        logger.info(f"User: {user['name']}, Email: {user['email']}")
        producer.send("user", value=user)
    # producer.flush()
    # producer.close()


with DAG(
    dag_id="kafka_user_streaming",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule=None,  # You can change this to '*/5 * * * *' or similar
    catchup=False,
    tags=["kafka", "streaming"],
) as dag:

    @task()
    def stream_user_task(user: dict[str, Any]):
        stream_user(user)

    stream_user_task()
