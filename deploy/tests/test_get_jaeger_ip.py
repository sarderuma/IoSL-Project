#!/usr/bin/python3
# import requests
# from kubernetes import client, config

# config.load_kube_config()
# v1 = client.CoreV1Api()
# ret = v1.list_node()
# for i in ret.items:
#     print (i.status.addresses[1].address)
#     break
#     # if (i.metadata.name=='jaeger'):
#     #     j_ip = i.status.load_balancer.ingress[0].ip
#     #     break
# #print (j_ip)
import subprocess

output = subprocess.check_output('gcloud compute instances list | awk \'FNR == 2 {print $5}\'',shell=True)
print('http://' + output.decode("utf-8").strip() + ':30001')