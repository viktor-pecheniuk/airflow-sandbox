import os

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator

from operators.spark_operator import SparkJobOperator


default_args = {
    'owner': 'viktor',
    'depends_on_past': False,
    'start_date': datetime(2019, 3, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('spark_dag',
          default_args=default_args,
          schedule_interval=timedelta(minutes=3))

t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag)

t2 = SparkJobOperator(
    yaml_file='{}/../ci/kube/spark_prometheus.yml'.format(os.path.abspath('.')),
    timeout=60,
    task_id='k8s_spark',
    dag=dag
)

t2.set_upstream(t1)
