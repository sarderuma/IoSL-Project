
# Objective

The objective of the evaluation dashboard is to o visualize the resource usage of the network components and the comparative performance between point to point and service mesh communication mode. The evaluation dashboard is designed by Python Dash. 

The dashboard is divided into parts. One is used for resource utilization (CPU and memory Usage) and other one is used to calculate the network perforamce (end to end time, communication overhead and number of requests) during service operation time. 

1. Resource Utilization: 
   CPU Usage (%) = (current CPU usage/no. of CPU cores)*100
   For example, minikube has 2 CPU cores in phase-1.
   
   Memory Consumption (KB) = current consuming memory
   (To scale in the dashboard, the memory usage is divided by 1000)

2. Communication Performace: 
One packet is successfully transmitted between the sender and receiver when the sender will receive acknowledgment of the packet. The duration it takes to get the acknowledgment is called the end to end of this packet. Here, the root span duration is the total end to end time of a successful transmission. Therefore, no. of requests are equal to the total no. of root span during the operation time. 

   Average End to End Time: sum of root spans duration / total number of root spans
   Average Communication Overhead: Average end to end time - (no. of microservices * delay)
   Number of Requests: Total number of root span
 
  
# Requirements

- python
- pip install dash
- pip install kubernetes


# Run

- python app.py

# Dashboard URL

 - http://127.0.0.1:8050/



