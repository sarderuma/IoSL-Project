from flask import Flask
from flask import request
from lib.tracing import init_tracer
import opentracing
from opentracing.ext import tags
from flask import json
import time

app = Flask('ms_01')
init_tracer('ms_01')


@app.route("/from-previous-ms",methods=['GET', 'POST'])
def from_previous_ms():
    span_ctx = opentracing.tracer.extract(
        opentracing.Format.HTTP_HEADERS,
        request.headers,
    )
    with opentracing.tracer.start_active_span(
        'from_previous_ms',
        child_of=span_ctx,
        tags={tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER},
    ) as scope:
        #print("from-previous-m === ",json.dumps(request.json))
        time.sleep(5)
        return 'OK', 200

if __name__ == "__main__":
    app.run(port=8085)
