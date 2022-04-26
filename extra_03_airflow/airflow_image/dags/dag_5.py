from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime
from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.sensors.file_sensor import FileSensor


default_args = {
    "start_date": datetime.fromisoformat("2021-02-05T00:00:00.000")
}

list_files = [x for x in range(1, 11)]


class MyAwesomeOperator(BaseOperator):
    @apply_defaults
    def __init__(self, super_variable, **kwargs):
        super().__init__(**kwargs)
        self.super_variable = super_variable

    def execute(self, context):
        self.log.info("Task Context %r", context)
        self.log.info("Operator Context %r", dir(self))
        return self.super_variable


class MyAwesomeOperatorTemplated(BaseOperator):
    template_fields = ("templated_variable", )

    @apply_defaults
    def __init__(self, templated_variable, **kwargs):
        super().__init__(**kwargs)
        self.templated_variable = templated_variable
        self.log.info("`__init__` templated_variable: %r", self.templated_variable)

    def execute(self, context):
        self.log.info("`execute` templated_variable: %r", self.templated_variable)
        return None


with DAG(dag_id="dag-5.0-example", default_args=default_args, schedule_interval="@daily") as dag:
    start_task = DummyOperator(
        task_id="start_task_name",
        # dag=dag, # Not required in with clause
    )

    dummy_stuff = DummyOperator(
        task_id="do_nothing",
        # dag=dag, # Not required in with clause
    )

    start_task >> dummy_stuff

    end_task = DummyOperator(
        task_id="end_task_name",
        trigger_rule="one_success" # https://airflow.apache.org/docs/apache-airflow/stable/concepts.html#trigger-rules
        # dag=dag, # Not required in with clause
    )

    for item in list_files:
        job_task_id = "super_awesome_python_operator_%s" % item

        job_task = FileSensor(
            task_id=job_task_id,
            filepath="/opt/airflow/dags/%s" % item,
            fs_conn_id="my-file-path",
            poke_interval=5,
            mode="poke",  # By default poke
            # mode="reschedule", # Not recommended use less than 1 min interval
        )
        dummy_stuff >> job_task >> end_task
