#!/bin/bash
yq w -i deploy/microserv/values.yaml numberOfServices $1
yq w -i deploy/microserv/values.yaml delay $2
yq w -i deploy/microserv/values.yaml pktfreq $3
yq w -i deploy/microserv/values.yaml pktsize $4

helm upgrade ms deploy/microserv