# airflow-sandbox

Sandbox for airflow in docker container


# Quick Start:

1 - buid the image:

  `$ docker build -t airflow-sandbox .`

2 - run the container:
  
  `$ docker run -d -p 8080:8080 --rm --name airflow_container airflow-sandbox`
  
3 - launch particular DAG, e.g. `my_dag`:

   `docker exec airflow_container airflow trigger_dag my_dag`


# To check metrics exported to Prometheus:

Just go to default url in your browser - `your_host:8080/admin/metrics`
