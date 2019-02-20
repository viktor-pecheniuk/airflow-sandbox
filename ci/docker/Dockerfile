FROM python:3.6.3
MAINTAINER "viktor.pecheniuk@gmail.com"

# Airflow setup
ARG AIRFLOW_VERSION=1.10.2
ARG JSON_LOGGER_VERSION=0.1.10
ARG PROMETHEUS_CLI_VERSION=0.5.0

ENV AIRFLOW_HOME=/app/airflow
ENV SLUGIFY_USES_TEXT_UNIDECODE=yes
ENV PYTHONPATH=$AIRFLOW_HOME

RUN apt-get update \
  && apt-get install -y supervisor \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/* \
  && pip install apache-airflow[postgres]==${AIRFLOW_VERSION} \
  && pip install python-json-logger==${JSON_LOGGER_VERSION} \
  && pip install prometheus-client==${PROMETHEUS_CLI_VERSION} \
  && pip install psycopg2

# replace owns configs
COPY ./ci/conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY ./ci/conf/airflow.cfg $AIRFLOW_HOME/airflow.cfg
COPY utils/configs.py $AIRFLOW_HOME/utils/configs.py

COPY dags $AIRFLOW_HOME/dags
COPY plugins $AIRFLOW_HOME/plugins
COPY tests $AIRFLOW_HOME/tests

CMD airflow initdb
# run tests before deploy
CMD cd $AIRFLOW_HOME && python -m unittest

EXPOSE 8080

CMD ["/usr/bin/supervisord"]
