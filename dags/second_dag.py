import pprint
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 2, 6),
    'email': [],
    'email_on_failure': 'viktor.pecheniuk@gmail.com',
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('my_second_dag', default_args=default_args,  schedule_interval=timedelta(minutes=2))


def print_context(ds, **kwargs):
    print("Here first arg >>>", ds)
    pprint.pprint(kwargs)
    return "Done.................."

with dag:
    t1 = BashOperator(
        task_id='bash_example',
        bash_command='echo 1111111111111111111111',
        dag=dag)

    t2 = PythonOperator(
        task_id='print_the_context',
        provide_context=True,
        python_callable=print_context,
        dag=dag)

    t3 = BashOperator(
    task_id='also_run_this',
    bash_command='echo "run_id={{ run_id }} | dag_run={{ dag_run }}"',
    dag=dag)

t2 >> t3 >> t1
