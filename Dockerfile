FROM python:3.6.3
MAINTAINER "viktor.pecheniuk@gmail.com"

RUN apt-get update && apt-get install -y supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
# Airflow setup
ARG AIRFLOW_VERSION=1.10.2

ENV AIRFLOW_HOME=/app/airflow
ENV SLUGIFY_USES_TEXT_UNIDECODE=yes
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False

RUN pip install apache-airflow==${AIRFLOW_VERSION}

COPY /dags/* $AIRFLOW_HOME/dags/
RUN airflow initdb
EXPOSE 8080

CMD ["/usr/bin/supervisord"]
