# IoSL-Project
For this project the Kubernates Cluster is set up in GKE while the configuration and monitoring dashboard runs on Local machine

# Cluster setup
Get a GKE account

1. Install and Initialize [Google Cloud SDK](https://cloud.google.com/sdk/docs/quickstart-macos)

2. Install kubectl:
    ```
    gcloud components install kubectl
    ```

3. Install [Helm](https://helm.sh/docs/intro/install/) (v2.16.0)

4. Create a cluster (use the same zone as the one set as default when initializing Google Cloud SDK ):
    ```
    gcloud container clusters create phase1-http-cluster --zone us-central1-a --cluster-version 1.14.10-gke.17 --num-nodes 4 --machine-type n1-standard-2
    ```

5. Initialize kubectl for cluster:
    ```
    gcloud container clusters get-credentials phase1-http-cluster
    ```
    **Note**: You might need to enable Kubernetes API for a new project

6. Initialize helm for cluster :
    ```
    bash deploy/scripts/init_helm_gke.sh
    ```

7. Install firewall rules for sender and jaeger (one time setup for every project):
    ```
    bash deploy/scripts/install_fw_rules.sh
    ```

8. Run following commands to test if kubectl/helm are properly configured:
    ```
    kubectl get nodes
    helm version
    ```


## Istio setup

1. Install [Istioctl](https://istio.io/docs/setup/getting-started/#download) (v1.4.2)

    For MacOS recommended way to install istioctl is:
    ```
    brew install istioctl
    ```

2. Install Istio on cluster:
    ```
    istioctl manifest apply --set profile=demo
    ```

# Dashboard setup
1. Install Python dependencies: 
    ```
    pip install -r requirements.txt 
    ```
2. Install [yq](http://mikefarah.github.io/yq/) (v1.6) (a cli tool to manipulate yaml files)

3. Start kube proxy service:
    ```
    kubectl proxy --port=8001
    ```

# Usage

## Configuration dashboard
```
python deploy/config_dashboard.py
```
*packet size* : Supports sizes 1KB, 2KB, 4KB and 8KB

*packet interval* : Time interval in seconds between sending of two packets

*packet count* : Total number of packets which will be sent for the experiment

Enter parameters and use *create* button to create microservices. 
When all pods are up, *start* button is enabled which triggers sending packets.
  

NOTE: When you enable/disable Istio, you need to delete and re-create microservices. This is due to requirements of Istio automatic injection.

## Monitoring dashboard
```
python Dashboard/app.py
```

Navigate to [http://127.0.0.1:8050](http://127.0.0.1:8050)

# Contributors
**Abhishek Dandekar** (*deploy*): Code for creating microservices and configuration dashboard.

**Liming Liu** (*http_sender*): Code for dockerized sender.

**Uma Sarder** (*Dashboard*): Code for monitoring dashboard.

**Ashish Sanjay Sharma** (*http_microservice*): Code for dockerized microservice and receiver.


# Code structure
Explaination for code structure can be found in individual readme in each directory.

For microservices code and receiver - please take a look at branch : http_ms_rx_helm3.0

The http_ms code in the master branch is a dummy code and example for reference.

**Note that** the code is supposed to run as a docker container and is not meant to be directly executable, unless if certain lines are uncommented.

# Misc Commands
To delete cluster:
```
gcloud container clusters delete phase1-http-cluster 
```

To check if sidecar proxy exists:
```
kubectl get pods <POD-NAME> -o jsonpath='{.spec.containers[*].name}'
```

# Debugging
If you get error saying GOOGLE_APPLICATION_CREDENTIALS not set, follow [this](https://cloud.google.com/docs/authentication/getting-started) guide
