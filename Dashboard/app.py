#required library 
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import json
from datetime import datetime
import os
import subprocess
app = dash.Dash()

#communication overhead variable
e2e=0.0

# example data can be loaded dynamically later directly from the services
cpu_monitor={}           
memory_monitor={}
#creat logfile for each microservice span duration
Logfile=open("logfile.txt",'a')
#create memlog for CPU and memory usage
memlog=open("memlog.txt",'a')
#create requestlog for communication overhead  
request=open("requestlog.txt",'a')

#function for getting IP from jaeger    
def get_jaeger_ip():
    output = subprocess.check_output('gcloud compute instances list | awk \'FNR == 2 {print $5}\'',shell=True)
    return output.decode("utf-8").strip()

#function for loading json data of CPU and momory usage
def read_usage_stat(std_data):
    #Read the data of json
    json_obj=json.loads(std_data)  
    items=json_obj['items'] 

    ##store microservice name, cpu, memory and time 
    stat=[] 
    memlog.write('#####\n')
    for item in items: 
        #data has many containers
        if 'containers' in item.keys(): 
            #if the containers value is not null
            if item['containers']!=[]:
                timestamp=item['metadata']['creationTimestamp'].strip('Z').split('T')   
                timestamp_year=timestamp[0]  
                ts=timestamp[1]   
                
                #start from first containers
                pd=item['containers'][0]
                #found name of the microservices  
                name=pd['name'] 
                #usage contains CPU data and CPU percentage usage is (current cpu usage*100/number of cores);number of cores is 2  
                cpu_usage=pd['usage']['cpu']    
                cpu_usage=int(cpu_usage.strip('n'))/(2*10000000)  
                #usage contains memory data
                memory=pd['usage']['memory']   
                #memory calculation unit is in KB and to sacle in dashboard divide by 1000
                if 'M' in memory:  
                    memory=int(memory.strip('Mi'))*1024/1000
                elif 'K' in memory:
                    memory=int(memory.strip('Ki'))/1000
 
                #required data stored
                stat.append({'name':name, 'cpu':cpu_usage,'memory': memory, 'year':timestamp_year, 'time':ts})
                memlog.write('\t'.join([str(timestamp), str(name), str(cpu_usage), str(memory)])+'\n') 
                #dynamically genarate CPU and memory data with respect to time
                if name in cpu_monitor.keys(): 
                    cpu_monitor[name]['data'].append((ts, cpu_usage))
                else:
                    cpu_monitor[name]={'data':[(ts,cpu_usage)]}

                if name in memory_monitor.keys(): 
                    memory_monitor[name]['data'].append((ts,memory))
                else:
                    memory_monitor[name]={'data':[(ts,memory)]}


    return True

#function for converting given time to decimal
def time2decimal(t):
    ts=t.split(':') 
    return int(ts[0])*3600+int(ts[1])*60+int(ts[2]) 

#function for getting delay, requested packet     
def get_microsrv_info(filename='deploy/microserv/values.yaml'):   
    n_microsrv=0
    delay=0
    frequency=0
    with open(filename) as F:
        for line in F:
            if line.startswith('numberOfServices'):
                n_microsrv=int(line.strip().split(':')[1])
            if line.startswith('delay'):
                delay=int(line.strip().split(':')[1])
            if line.startswith('pktfreq'):
                frequency=int(line.strip().split(':')[1])
                    
    print(n_microsrv, delay, frequency)
    return n_microsrv, delay, frequency 

#funtion for microservice rootspan info
def read_ms_spans(cmd_out, conf_file):
    ms_stat=[]
    ms,d,frequency=get_microsrv_info(conf_file)
    json_obj=json.loads(cmd_out)

    
    # stores the duration for each root span found
    durs=[] 
    mss=[]
    # Read the data of json 
    traces=json_obj['data'] 
    # Read the data of json 
    Logfile.write('#### new Run ##\n')

    for trace in traces:  
        # each trace has many spans 
        msvcs=[]
        for span in trace['spans']:  
            # looking for root span operation in operationName
            
            if span['operationName']=='root span': 
                durs.append(int(span['duration']))
            elif span['operationName']=='post_data':
                dt=int(span['duration'])
                for tag in span['tags']:
                    if tag['key']=='http.url':
                        msvcs.append((tag['value'],dt) )
        mss.append(msvcs)
        msvcs=[]


            
    # no of root span found
    no_root_span=len(durs)  
    for sd, sms in zip(durs,mss):
        Logfile.write(str(sd)+':'+str(sms) +'\n')
    average_duration=round(sum(durs)/no_root_span) 
    duration_max=average_duration
    
    #Communication Overhead
    e2e=((duration_max/1000000)-(ms*d))*1000
    e2e='%.5f' %e2e
    print(e2e)

    #number_packets=no_root_span
    number_request=no_root_span
    print(number_request)
    ms_info=[]
    request.write(str(number_request)+','+str(e2e)+'\n')

    return (ms_info, e2e, duration_max/1000, number_request)


#function for generating microservice spanlength slider
def slider_design(ms_stat):
    hslider=[]
    h3=[html.P("{},  Duration:{} msec".format(x['pid'], x['duration']/1000000))   for x in ms_stat]
    slider=[dcc.RangeSlider(id="",dots=True, min=x['mn'], max=x['mx'],
        value=[x['start'], x['end']], 
        marks={ x['start']:{'label':str(datetime.fromtimestamp(x['start']//1000000).time()) }, x['end']:{'label':str(datetime.fromtimestamp(x['end']//1000000).time())} }, 
        step=(x['mx']-x['mn'])/5000.0 ) for x in ms_stat ]
    for x,y in zip(h3,slider):
        hslider.append(x)
        hslider.append(y)
    #print(slider)
    #return hslider


def get_cpu_monitor():
    pass

def get_memory_monitor():
    pass

#define dasboard background color    
colors = {
    'background': '#111111',
    'text': '#8E44AD'
}    

#dashboard content layout
app.layout = html.Div([
    #header define
    html.H1("Evaluation Dashboard", style={ 'textAlign': 'center', 'color': colors['text'] }),
    
    #dashbord is sepearted into two tabs 
    #CPU and memory visualization    
    dcc.Tabs(id="tabs-example", value='CPU & load',
        children=[
            dcc.Tab(label='Resource Utilization', value='tab-1-example', 
                children=[

                html.Div([
                    #two seperate graph is grenerated
                    dcc.Graph(id='cpu_usage'),

                    dcc.Graph(id='memory_usage')
                    ]), 
                    
                    #dinamically read data in 2s interval
                    dcc.Interval(id='timer', interval=2*1000, n_intervals=0)

            ]),
            
            #evaluation service details
            dcc.Tab(label='Network Performance', value='tab-2-example', 

                children=[
                    #show respectively avearge end to end time, communication overhead, no of requests
                    html.H2(id='transfer_time', style={ 'textAlign': 'center'}),
                    html.H2(id='ene_delay', style={ 'textAlign': 'center'}),
                    html.H2(id='request_pkt', style={ 'textAlign': 'center'}),
                    dcc.Interval(id='timer-tab-2', interval=2*1000, n_intervals=0)  
            ]),
    ]) 

]) 


#find the process ID
def process_output(d, pid):
    d1=sorted(d, key=lambda x:time2decimal(x[0]))
    x=[x[0] for x in d1]
    y=[x[1] for x in d1]
    return {'x':x, 'y':y, 'type':'line', 'name':pid }

#dash callback for CPU and memory
@app.callback([Output('cpu_usage','figure'), Output('memory_usage', 'figure')], [Input('timer','n_intervals')])

#dinamically loading json data from metrics server for cpu and memory utilization
def update_cpu_usage(value):
    std_out=os.popen('curl 127.0.0.1:8001/apis/metrics.k8s.io/v1beta1/namespaces/default/pods').read()
    s=read_usage_stat(std_out)
    
    #CPU graph
    figure1={ 'data': [ process_output(cpu_monitor[pid]['data'], pid) for pid in cpu_monitor.keys()
                    ],

                    'layout':{ 'title':'CPU Usage Monitoring', 'yaxis':{"title": "CPU Usage (%)"}, 'xaxis':{"title": "Time (UTC)"}}
                    }

    #Memory graph               
    figure2={   'data': [ process_output(memory_monitor[pid]['data'], pid) for pid in memory_monitor.keys()
                        ],

                        'layout':{ 'title':'Memory Usage Monitoring', 'yaxis':{"title": "Memory Usage (KB)"}, 'xaxis':{"title": "Time (UTC)"}}
                        }

    return figure1, figure2


#dash callback for evaluation service
@app.callback([Output('transfer_time', 'children'), Output('ene_delay', 'children'), Output('request_pkt', 'children')], [Input('timer-tab-2', 'n_intervals')])

#getting evaluation service info from jaeger tracing data
def update_delay(value):

    std_out=os.popen('curl http://'+ jaeger_ip + ":32417/api/traces?service=msvc").read()
    ms_stat, e2e, trans_dur, number_request=read_ms_spans(std_out, conf_file="deploy/microserv/values.yaml")
    trans_lbl="Average End to End Time: "+str(trans_dur)+" ms"
    delay_lbl="Average Communication Overhead: "+str(e2e)+" ms"
    request_no="Number of Requests: "+str(number_request)+" "
    print  ("\n\n"+ trans_lbl)
    print  ("\n\n"+ delay_lbl)
    print (jaeger_ip)
    return trans_lbl, delay_lbl, request_no
    
if __name__ == '__main__':
    jaeger_ip=get_jaeger_ip() #gets ip for svc jaeger so as to use in update_delay()

    app.run_server(debug=True)

       