FROM python:3.6.3
MAINTAINER "viktor.pecheniuk@gmail.com"

RUN apt-get update && apt-get install -y supervisor
# Airflow setup
ARG AIRFLOW_VERSION=1.10.2

ENV AIRFLOW_HOME=/app/airflow
ENV SLUGIFY_USES_TEXT_UNIDECODE=yes
ENV PYTHONPATH=$AIRFLOW_HOME

RUN pip install apache-airflow==${AIRFLOW_VERSION}
RUN pip install python-json-logger

# replace owns configs
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY airflow.cfg $AIRFLOW_HOME/airflow.cfg
COPY dags/* $AIRFLOW_HOME/dags/
COPY utils/configs.py $AIRFLOW_HOME/utils/configs.py

RUN airflow initdb
EXPOSE 8080

CMD ["/usr/bin/supervisord"]
