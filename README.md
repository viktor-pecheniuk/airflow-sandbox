# airflow-sandbox

Sandbox for airflow in docker container

Getting started:

1 - buid the image:

  `$ docker build -t airflow-sandbox .`

2 - run the container:
  
  `$ docker run -d -p 8080:8080 --rm --name airflow_container airflow-sandbox`
  
3 - launch particular DAG, e.g. `my_dag`:

   `docker exec airflow_container airflow trigger_dag my_dag`
