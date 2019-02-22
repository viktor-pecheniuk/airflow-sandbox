# Airflow on top of *Kubernetes*

## There are couple approaches to deploy your Airflow:

--------------------------------------------

### 1. Airflow as a docker container.

1 - buid the image:

  `$ docker build -f ci/docker/Dockerfile -t airflow-sandbox .`

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

  `$ docker exec airflow_container airflow trigger_dag my_dag`


### To check metrics exposed to Prometheus:

Just go to default url in your browser - `your_host:8080/admin/metrics`

--------------------------------------------

### 2. Airflow in k8s.

Make sure you have registered your local docker registry - e.g. [HERE](https://docs.docker.com/registry/)

Also you need to install and configure `minikube` and `kubectl` on your machine.

1 - `Build a docker image` as it's describe above and push it to your registry e.g `docker push localhost:5000/airflow-sandbox:0.1.0`

2 - Make sure you have your cluster ready, e.g. `kubectl get all`

3 - Create deployment and service for DB (I'm using PostgreSQL):

  `$ kubectl create -f ci/kube/postges.yml`

4 - Create deployment and service for airflow (Pod is creating from your airflow docker image):

  `$ kubectl create -f ci/kube/airflow.yml`

Now you should see that pods, services, deployments... are successfully running

--------------------------------------------

### 3. Deploy by k8s Airflow Operator.

Please check this [Repo](https://github.com/GoogleCloudPlatform/airflow-operator) for details.

To deploy **airflow-operator** you need to install `go` and `kubebuilder` on your machine.

#### Get Started:

1 - clone repo:

  ```
  $ mkdir -p $GOPATH/src/k8s.io
  $ cd $GOPATH/src/k8s.io
  $ git clone git@github.com:GoogleCloudPlatform/airflow-operator.git
  ```

2 - Setup your cluster to understand Application resources:

  `$ kubectl apply -f "https://raw.githubusercontent.com/GoogleCloudPlatform/marketplace-k8s-app-tools/master/crd/app-crd.yaml"`

3 - Build manager binary:

  `$ make manager`

4 - Run against the configured Kubernetes cluster in ~/.kube/config

  `$ make run`

5 - Create `AirflowBase` and `AirflowCluster` on your cluster

  `$ kubectl apply -f ci/kube/base.yml`

  wait before it will be in state running

  `$ kubectl apply -f ci/kube/cluster.yml`


All done. Now you will see that airflow ui, scheduler are running on your kube.

# Enjoy!
