import kubernetes.config as k8s_config
from kubernetes import client as k8s_client

from kubernetes.watch import Watch

from airflow.exceptions import AirflowException
from airflow.models import BaseOperator

from airflow.utils.decorators import apply_defaults

from utils.helpers import yaml_2_json


class SparkJobOperator(BaseOperator):

    template_fields = ('namespace', 'job_name')

    @apply_defaults
    def __init__(self, namespace, job_name, yml_file, timeout, config_map_name=None, *args, **kwargs):
        """
        :param yaml_file: str, file obj
        :param timeout: int as seconds
        """
        super(SparkJobOperator, self).__init__(*args, **kwargs)
        self.namespace = namespace
        self.job_name = job_name
        self.crd_file = yml_file
        self.timeout = timeout
        # TODO check later when new version will be available
        self.group = 'sparkoperator.k8s.io'
        self.version = 'v1beta1'
        self.plural = 'sparkapplications'
        self.config_map_name = config_map_name

    def execute(self, context):
        # initialize config
        try:
            config = k8s_config.load_incluster_config()
        except:
            config = k8s_config.load_kube_config()
        # create an instance of the API class
        api_core_instance = k8s_client.CoreV1Api(k8s_client.ApiClient(config))
        api_custom_instance = k8s_client.CustomObjectsApi(k8s_client.ApiClient(config))
        # params to create custom object
        custom_params = [self.group, self.version, self.namespace, self.plural]
        resources = yaml_2_json(self.crd_file)
        for resource in resources:
            if resource['kind'] == "SparkApplication":
                crd_created = self.create_custom_definition(api_custom_instance, resource, *custom_params)
                if crd_created:
                    w = Watch()
                    for event in w.stream(api_custom_instance.list_namespaced_custom_object, *custom_params,
                                          timeout_seconds=self.timeout):
                        job_name = event.get('object', {}).get('metadata', {}).get('name')
                        job_state = event.get('object', {}).get('status', {}).get('applicationState', {}).get('state')
                        if job_name == self.job_name and job_state == "COMPLETED":
                            break
            elif resource['kind'] == "ConfigMap":
                if self.config_map_name is not None:
                    self.create_config_map(api_core_instance, resource)

    def create_custom_definition(self, api_instance, resource, *params):
        resource['metadata']['name'] = self.job_name
        try:
            success = True
            api_instance.create_namespaced_custom_object(*params, resource, pretty=False)
        except AirflowException as e:
            success = False
            print("Exception when calling CustomObjectsApi -> create_namespaced_custom_object: %s\n" % e)
        return success

    def create_config_map(self, api_instance, resource):
        resource['metadata']['name'] = self.config_map_name
        try:
            success = True
            api_instance.create_namespaced_config_map(
                namespace=self.namespace,
                body=resource
            )
        except AirflowException as e:
            success = False
            print("Exception when calling Create Config Map -> create_namespaced_config_map: %s\n" % e)
        return success
