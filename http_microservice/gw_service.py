import json
import requests
from flask import Flask
from flask import request
from lib.tracing import init_tracer
import opentracing
from opentracing.ext import tags
import time
from flask import json


app = Flask('microservice_sa_5G')
init_tracer('microservice_sa_5G')


@app.route("/from-client",methods=['GET', 'POST'])
def from_client():
    span_ctx = opentracing.tracer.extract(
        opentracing.Format.HTTP_HEADERS,
        request.headers,
    )
    with opentracing.tracer.start_active_span(
        'from-client',
        child_of=span_ctx,
        tags={tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER},
    ) as scope:
        data_received = json.dumps(request.json)
        print("data_received ==== ",data_received)
        processing_delay = time.sleep(10)
        processing_delay = get_ms_delay(); #get delay configured by configuration dashboard
        microservice_ip = get_ms_ip()  ##call service discovery to discover microservices ip
        #microservice_ip = "http://localhost:8085"
        resp_ms = call_other_microservice(microservice_ip,data_received)
        scope.span.set_tag('response', resp_ms)
        return resp_ms


"""
Method to fetch Delay informaton set by configuration dashboard
"""
def get_ms_delay():
    with opentracing.tracer.start_active_span(
        'get-ms-delay',
    ) as scope:
        url = 'http://localhost:8081/getmsdelay'  #url for service discovery api
        resp_from_delay_server = get_data(url)
        ms_delay = json.loads(resp_from_delay_server)  #deserialize the received data
        scope.span.log_kv({
            'hostname': ms_delay['hostname'],
            'ip': ms_delay['ip'],
            'delay': ms_delay['delay'],  
        })
        return ms_delay['delay']

"""
Call service discovery mechanism to get microservices ip,hostname,or DNS
"""
def get_ms_ip():
    with opentracing.tracer.start_active_span(
        'get-ms-ip',
    ) as scope:
        url = 'http://localhost:8081/getip'  #url for service discovery api
        resp_from_service_discovery = get_data(url)
        ms_ip = json.loads(resp_from_service_discovery)
        scope.span.log_kv({
            'hostname': ms_ip['hostname'],             #other details also as per configuration, 
            'ip': ms_ip['ip'],                          #need to see later
        })
        return ms_ip['ip']

"""
Method to call another microservice
"""
def call_other_microservice(microservice_ip,data_received):
    with opentracing.tracer.start_active_span(
        'call-other-microservice-ip',
    ):
        url = microservice_ip + '/' + 'from-previous-ms'
        print("-------",url)
        return post_data(url , data_received)


def get_data(url, params=None):
    span = opentracing.tracer.active_span
    span.set_tag(tags.HTTP_URL, url)
    span.set_tag(tags.HTTP_METHOD, 'GET')
    span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_CLIENT)
    headers = {}
    opentracing.tracer.inject(
        span.context, 
        opentracing.Format.HTTP_HEADERS,
        headers,
    )
    r = requests.get(url, params=params, headers=headers)
    assert r.status_code == 200
    return r.text

def post_data(url, data_received):
    span = opentracing.tracer.active_span
    span.set_tag(tags.HTTP_URL, url)
    span.set_tag(tags.HTTP_METHOD, 'POST')
    span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_SERVER)
    headers = {'Content-type': 'application/json'}
    opentracing.tracer.inject(
        span.context, 
        opentracing.Format.HTTP_HEADERS,
        headers,
    )
    r = requests.post(url, data=data_received, headers=headers)
    assert r.status_code == 200
    return r.text


if __name__ == "__main__":
    app.run(port=8080)
