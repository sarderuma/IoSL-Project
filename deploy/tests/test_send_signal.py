#!/usr/bin/python3
import requests
from kubernetes import client, config

config.load_kube_config()
v1 = client.CoreV1Api()
ret = v1.list_service_for_all_namespaces()
for i in ret.items:
    if (i.metadata.name=='sender'):
        ip_addr = i.status.load_balancer.ingress[0].ip
#status = requests.get('http://' + ip_addr + ':80',headers={'Connection':'close'})
