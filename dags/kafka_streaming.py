from airflow import DAG
from time import sleep, time
from datetime import datetime
from random import uniform
from faker import Faker



default_args = {
    "owner": "airflow",
}

fake = Faker()


def generate_user():
    sleep(uniform(0.0, 1.5))

    return {
        "name": fake.name(),
        "address": fake.address(),
        "email": fake.email(),
        "phone_number": fake.phone_number(),
    }


# dag = DAG(
#     'user_automation',
#     default_args=default_args,
#     description='Kafka streaming DAG',
#     schedule_interval='@daily',
#     catchup=False,
# )

with DAG(
    "user_automation",
    default_args=default_args,
    description="Kafka streaming DAG",
    schedule_interval="@daily",
    catchup=False,
    start_date=datetime(2025, 3, 1),
) as dag:
    pass


for i in range(10):
    start_time = time()
    user = generate_user()
    end_time = time()
    execution_time = end_time - start_time
    print(f"Execution {i+1}: {execution_time} seconds. User: {user}")

    generate_user()
