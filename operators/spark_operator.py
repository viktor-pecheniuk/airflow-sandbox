from kubernetes import client as kube_client
from kubernetes import config as kube_config
from kubernetes import watch

from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from utils.helpers import yaml_2_json


class SparkJobOperator(BaseOperator):

    @apply_defaults
    def __init__(self, yaml_file, timeout, *args, **kwargs):
        """
        :param yaml_file: str, file obj
        :param timeout: int as seconds
        """
        super(SparkJobOperator, self).__init__(*args, **kwargs)
        self.crd_file = yaml_file
        self.timeout = timeout

    def execute(self, context):
        # TODO check later with prod kube
        config = kube_config.load_kube_config()
        # create an instance of the API class
        api_instance = kube_client.CustomObjectsApi(kube_client.ApiClient(config))
        # params to create custom object
        group = 'sparkoperator.k8s.io'
        version = 'v1beta1'
        namespace = 'default'
        plural = 'sparkapplications'
        spark_app_name = 'spark-pi'
        crd_body = yaml_2_json(self.crd_file)
        w = watch.Watch()
        api_params = [group, version, namespace, plural]
        try:
            api_instance.create_namespaced_custom_object(*api_params, crd_body, pretty=True)
        except AirflowException as e:
            print("Exception when calling CustomObjectsApi -> create_namespaced_custom_object: %s\n" % e)

        for event in w.stream(api_instance.list_namespaced_custom_object, *api_params):
            print(event.get('object', {}).get('status', {}).get('applicationState', {}).get('state'))
            if event.get('object', {}).get('status', {}).get('applicationState', {}).get('state') == "COMPLETED":
                break

        try:
            api_instance.delete_namespaced_custom_object(
                group, version, namespace, plural, spark_app_name,
                kube_client.V1DeleteOptions(), grace_period_seconds=10
            )
        except AirflowException as e:
            print("Exception when calling CustomObjectsApi -> delete_namespaced_custom_object: %s\n" % e)
