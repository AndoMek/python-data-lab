from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
# from inspect import getfullargspec
# from functools import wraps

default_args = {
    "start_date": datetime.fromisoformat("2021-02-05T00:00:00.000")
}


# def dec(fn):
#     print("Call function %r, %r" % (fn.__name__, getfullargspec(fn)))
#
#     @wraps
#     def xxx(*a, **kw):
#         print("args: %r" % a)
#         print("kwargs: %r" % kw)
#         return fn(*a, **kw)
#
#     return xxx


def some_function(*args, **kwargs):
    print("args: %s" % (args, ))
    print("kwargs: %s" % (kwargs, ))
    return 1


with DAG(dag_id="dag-2.1-example", default_args=default_args, schedule_interval="@daily") as dag:
    start_task = DummyOperator(
        task_id="start_task_name",
        # dag=dag, # Not required in with clause
    )

    job_task = PythonOperator(
        task_id="awesome_python_operator",
        python_callable=some_function,
        op_kwargs={"kw1": 2, "kw2": 42, },
        op_args=(1, 2, 3)
    )

    end_task = DummyOperator(
        task_id="end_task_name",
        # dag=dag, # Not required in with clause
    )

    # start_task >> job_task
    # job_task >> end_task

    start_task >> job_task >> end_task
