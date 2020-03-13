sample microservice applications built on flask

* http based microservice prototype with opentracing
* config.py - microservice to configure next_hop and delay
* gw_service.py - microservice to recevie packet, get configuration parameters and invoke next microservice
* ms_process.py - microservice acting as a receiver

To install:

pip install -r requirements.txt 

Install the opentracing tool

https://www.jaegertracing.io/docs/1.8/getting-started/ 

$ docker run -d --name jaeger \
  -e COLLECTOR_ZIPKIN_HTTP_PORT=9411 \
  -p 5775:5775/udp \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 5778:5778 \
  -p 16686:16686 \
  -p 14268:14268 \
  -p 9411:9411 \
  jaegertracing/all-in-one:1.8

To run:

python ms_process.py
python gw_service.py
python config.py

Use http anyclient to send POST request with JSON body to gw_service.py -  http://localhost:8080/from-client

e.g
{
"packetID": "1",
"timeStamp": "11:59"
 }
 
http://localhost:16686 for ui tool to search trace