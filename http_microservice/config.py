from flask import Flask
from flask import request
from lib.tracing import init_tracer
import opentracing
from opentracing.ext import tags
from flask import json
import time
from flask import jsonify, make_response


app = Flask('config')
init_tracer('config')


@app.route("/getmsdelay",methods=['GET', 'POST'])
def getmsdelay():
    span_ctx = opentracing.tracer.extract(
        opentracing.Format.HTTP_HEADERS,
        request.headers,
    )
    with opentracing.tracer.start_active_span(
        'get_ms_delay',
        child_of=span_ctx,
        tags={tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER},
    ) as scope:
        data = {
            "hostname": "ms.com.nsa",
            "ip": "http://localhost:8085",
            "delay":"10"
            }
        res = make_response(jsonify(data), 200)
        time.sleep(5)
        return res


@app.route("/getip",methods=['GET', 'POST'])
def getip():
    span_ctx = opentracing.tracer.extract(
        opentracing.Format.HTTP_HEADERS,
        request.headers,
    )
    with opentracing.tracer.start_active_span(
        'get_ip',
        child_of=span_ctx,
        tags={tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER},
    ) as scope:
        data = {
            "hostname": "ms.com.nsa",
            "ip": "http://localhost:8085"
            }
        res = make_response(jsonify(data), 200)
        time.sleep(5)
        return res



if __name__ == "__main__":
    app.run(port=8081)
