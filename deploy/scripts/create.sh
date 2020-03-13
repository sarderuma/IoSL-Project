#!/bin/bash
yq w -i deploy/microserv/values.yaml serviceName $1
yq w -i deploy/microserv/values.yaml numberOfServices $2
yq w -i deploy/microserv/values.yaml delay $3
yq w -i deploy/microserv/values.yaml pktfreq $4
yq w -i deploy/microserv/values.yaml pktsize $5
helm install --name ms deploy/microserv
