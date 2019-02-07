FROM python:3.6.3
MAINTAINER "viktor.pecheniuk@gmail.com"

RUN apt-get update && apt-get install -y supervisor
# Airflow setup
ARG AIRFLOW_VERSION=1.10.2
ARG JSON_LOGGER=0.1.10
ARG PROMETHEUS_VERSION=0.5.0

ENV AIRFLOW_HOME=/app/airflow
ENV SLUGIFY_USES_TEXT_UNIDECODE=yes
ENV PYTHONPATH=$AIRFLOW_HOME

RUN pip install apache-airflow==${AIRFLOW_VERSION}
RUN pip install python-json-logger==${JSON_LOGGER}
RUN pip install prometheus-client==${PROMETHEUS_VERSION}

# replace owns configs
COPY conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY conf/airflow.cfg $AIRFLOW_HOME/airflow.cfg
COPY utils/configs.py $AIRFLOW_HOME/utils/configs.py

COPY dags $AIRFLOW_HOME/dags
COPY plugins $AIRFLOW_HOME/plugins

RUN airflow initdb
EXPOSE 8080

CMD ["/usr/bin/supervisord"]
