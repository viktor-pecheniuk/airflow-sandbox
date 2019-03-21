from kubernetes import client as kube_client
from kubernetes import config as kube_config

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
        # create an instance of the API class
        config = kube_config.load_kube_config()
        api_instance = kube_client.CustomObjectsApi(kube_client.ApiClient(config))
        # params to create custom object
        group = 'sparkoperator.k8s.io'
        version = 'v1beta1'
        namespace = 'default'
        plural = 'sparkapplications'
        crd_body = yaml_2_json(self.crd_file)
        try:
            api_response = api_instance.create_namespaced_custom_object(group,
                                                                        version,
                                                                        namespace,
                                                                        plural,
                                                                        crd_body,
                                                                        pretty=True)
        except AirflowException as e:
            api_response = {}
            print("Exception when calling CustomObjectsApi -> create_namespaced_custom_object: %s\n" % e)
        return api_response
