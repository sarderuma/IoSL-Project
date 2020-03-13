This code creates microservice deployments using helm templates.

# config_dashboard
This launches a GUI using Python wx. It performs basic CRUD operations on microservices by calling corresponding bash scripts. It also sends trigger packet to the sender service. 

# microserv
This is a helm chart for creating microservices. For more info about structure of helm chart see [Helm charts](https://helm.sh/docs/topics/charts/)

## templates
Helm uses Go templates, to learn more see - [Chart template guide](https://helm.sh/docs/chart_template_guide/getting_started/) and [Golang templates](https://golang.org/pkg/text/template/)

For every microservice foo, *foo.deployment.yaml* template creates kubernetes pods while template *foo.service.yaml* creates kubernetes service. Templates consist of variables for which the values are assigned from *values.yaml* file. e.g
 *microservice* template uses for loop (*range*) to generate n number of microservices depending on *numberOfServices* in *values.yaml* file.

The sender and jaeger services use NodePort as they have to be accesible from outside while microservice and receiver services use ClusterIP.
Environment variables are used to pass user provided variables like packet frequency, packet size to the pods. The NEXT_HOP variable is auto-generated such that it points to the next microservice. 

# Scripts

## create/update/delete
These scripts are called by the GUI as result of a button onClick event. They create, update and delete microservices respectivly. *yq* is a cli tool used for inplace manipulation of YAML files. This is used to update *values.yaml* file.
e.g When a user clicks *create* button in GUI, the *create.sh* file reads values of microservice parameters from the GUI and writes them to *values.yaml* using yq. Then it calls the helm command to install microserv chart to cluster.

## init_helm_gke
Creates new service account and clusterrolebinding for current user in GKE, then initializes helm.

## install_fw_rules
Installs firewall rules for sender service port and jaeger service port in current GKE project.

# payloads
Files of specific size generated using random data by *mkfile* 