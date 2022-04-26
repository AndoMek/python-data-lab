from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    "start_date": datetime.fromisoformat("2021-02-05T00:00:00.000")
}

#
# start_date "2021-02-05T00:00:00.000"
# Daily!
# period 2021-02-05 = ["2021-02-05T00:00:00.000",  "2021-02-06T00:00:00.000")] +
# period 2021-02-06 = ["2021-02-06T00:00:00.000",  "2021-02-07T00:00:00.000")] +
# period 2021-02-07 = ["2021-02-07T00:00:00.000",  "2021-02-08T00:00:00.000")] +
# period 2021-02-08 = ["2021-02-08T00:00:00.000",  "2021-02-09T00:00:00.000")] +
# period 2021-02-09 = ["2021-02-09T00:00:00.000",  "2021-02-10T00:00:00.000")] +
# period 2021-02-10 = ["2021-02-10T00:00:00.000",  "2021-02-11T00:00:00.000")] +
# period 2021-02-11 = ["2021-02-11T00:00:00.000",  "2021-02-12T00:00:00.000")] +
# period 2021-02-12 = ["2021-02-12T00:00:00.000",  "2021-02-13T00:00:00.000")] -

with DAG(dag_id="dag-1.1-example", default_args=default_args, schedule_interval="@daily") as dag:
    start_task = DummyOperator(
        task_id="start_task_name",
        # dag=dag, # Not required in with clause
    )

    job_task = BashOperator(
        task_id="print_date",
        bash_command="echo {{ prev_execution_date }} {{ execution_date }} {{ next_execution_date }}"
    )

    end_task = DummyOperator(
        task_id="end_task_name",
        # dag=dag, # Not required in with clause
    )

    # start_task >> job_task
    # job_task >> end_task

    start_task >> job_task >> end_task
