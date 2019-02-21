from datetime import timedelta

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator


default_args = {
    'owner': 'viktor',
    'depends_on_past': False,
    'start_date': '2019-01-01',
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('new_dag', default_args=default_args,  schedule_interval=timedelta(minutes=3))

dummy_task = DummyOperator(task_id='kick_off_dag')

t2 = BashOperator(
    task_id='k8s_sync_print',
    bash_command="echo 'HELLO Airflow operator!'",
    dag=dag
)

t2.set_upstream(dummy_task)
