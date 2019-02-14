# airflow-sandbox

Sandbox for airflow in docker container


# Quick Start:

1 - buid the image:

  `$ docker build -t airflow-sandbox .`

2 - run the container:
  
  ```
  $ docker run -e AIRFLOW__CORE__SQL_ALCHEMY_CONN='postgresql://airflow:airflow_password@host.docker.internal/airflow' \
    -e DB_PORT=5432 \
    -e DB_HOST=host.docker.internal -d \
    -p 8080:8080 \
    --rm --name airflow_container \
    airflow-sandbox
  ```

3 - launch particular DAG, e.g. `my_dag`:

   `docker exec airflow_container airflow trigger_dag my_dag`


# To check metrics exported to Prometheus:

Just go to default url in your browser - `your_host:8080/admin/metrics`
