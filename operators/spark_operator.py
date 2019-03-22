from kubernetes.client import ApiClient, CustomObjectsApi, V1DeleteOptions
import kubernetes.config as kube_config

from kubernetes.watch import Watch

from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from utils.helpers import yaml_2_json


class SparkJobOperator(BaseOperator):

    @apply_defaults
    def __init__(self, namespace, job_name, yml_file, timeout, *args, **kwargs):
        """
        :param yaml_file: str, file obj
        :param timeout: int as seconds
        """
        super(SparkJobOperator, self).__init__(*args, **kwargs)
        self.namespace = namespace
        self.job_name = job_name
        self.crd_file = yml_file
        self.timeout = timeout

    def execute(self, context):
        # TODO check later with prod kube
        config = kube_config.load_kube_config()
        # create an instance of the API class
        api_instance = CustomObjectsApi(ApiClient(config))
        # params to create custom object
        group = 'sparkoperator.k8s.io'
        version = 'v1beta1'
        plural = 'sparkapplications'
        namespace = self.namespace
        crd_body = yaml_2_json(self.crd_file)
        spark_app_name = self.job_name
        w = Watch()
        params = [group, version, namespace, plural]
        try:
            api_resp = api_instance.get_namespaced_custom_object(
                group, version, namespace, plural, spark_app_name
            )
            print(api_resp.keys())
            try:
                if api_resp['metadata']['name'] == self.job_name:
                    api_instance.delete_namespaced_custom_object(
                        group, version, namespace, plural, spark_app_name,
                        V1DeleteOptions(), grace_period_seconds=5
                    )
            except AirflowException as e:
                print("Exception when calling CustomObjectsApi -> delete_namespaced_custom_object: %s\n" % e)

            api_instance.create_namespaced_custom_object(*params, crd_body, pretty=True)

        except AirflowException as e:
            print("Exception when calling CustomObjectsApi -> create_namespaced_custom_object: %s\n" % e)

        for event in w.stream(api_instance.list_namespaced_custom_object, *params, timeout_seconds=self.timeout):
            print(event.get('object', {}).get('status', {}).get('applicationState', {}).get('state'))
            if event.get('object', {}).get('status', {}).get('applicationState', {}).get('state') == "COMPLETED":
                break
