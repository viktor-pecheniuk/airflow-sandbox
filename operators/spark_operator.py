from kubernetes import client as kube_client
from kubernetes import config as kube_config

from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from utils.helpers import yaml_2_json

from kubernetes.client.rest import ApiException


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
        group = 'sparkoperator.k8s.io'  # str | The custom resource's group name
        version = 'v1beta1'  # str | The custom resource's version
        namespace = 'default'  # str | The custom resource's namespace
        plural = 'sparkapplications'  # str | The custom resource's plural name. For TPRs this would be lowercase plural kind.
        crd_body = yaml_2_json(self.crd_file)
        try:
            api_response = api_instance.create_namespaced_custom_object(group,
                                                                        version,
                                                                        namespace,
                                                                        plural,
                                                                        crd_body,
                                                                        pretty=True)
            print(api_response)
        except ApiException as e:
            print("Exception when calling CustomObjectsApi->create_namespaced_custom_object: %s\n" % e)
