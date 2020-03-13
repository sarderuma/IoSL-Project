#!/usr/bin/python3
import wx
import subprocess
import requests
import time
from kubernetes import client, config


def check_pod_health():
    "Checks if all pods are up"
    config.load_kube_config()
    v1 = client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(watch=False)
    pods_up = True
    for i in ret.items:
        if (i.metadata.namespace=='default'):
            if (i.status.phase == "Running"):
                pods_up= pods_up and True
            else:
                pods_up= pods_up and False

    return pods_up

 
def send_pkt(pkt_size, pkt_count, pkt_interval):
    "Starts sending http packets with specified parameters to the senderpod"
    data = "deploy/payloads/" + str(pkt_size) + 'K.payload'
    ip_addr = subprocess.check_output('gcloud compute instances list | awk \'FNR == 2 {print $5}\'',shell=True).decode("utf-8").strip()
    sender_endpoint= 'http://' + ip_addr + ':30001'
    for x in range(pkt_count):
        response = requests.post(sender_endpoint, data=data)
        time.sleep(pkt_interval)


class ConfigDash(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        self.SetTitle('Microservice Configuration Dashboard')
        self.panel = wx.Panel(self) 
        self.BtnStatus = True
        #Define widgets
        self.create = wx.Button(self.panel, label="Create")
        self.upgrade = wx.Button(self.panel, label="Update")
        self.delete = wx.Button(self.panel, label="Delete")
        self.start = wx.Button(self.panel, label="Start")
        self.Istio = wx.ToggleButton(self.panel, label='Enable Istio')

        self.label1 = wx.StaticText(self.panel, label="Number of microservices:")
        self.msvc = wx.SpinCtrl(self.panel, size=(60, -1))

        self.label2 = wx.StaticText(self.panel, label="Microservice Delay (s):")
        self.delay = wx.SpinCtrl(self.panel, size=(60, -1))

        self.label3 = wx.StaticText(self.panel, label="Packet size (KB):")
        self.size = wx.SpinCtrl(self.panel, size=(60, -1))

        self.label4 = wx.StaticText(self.panel, label="Packet Interval (s):")
        self.interval = wx.SpinCtrl(self.panel, size=(60, -1))

        self.label5 = wx.StaticText(self.panel, label="Packet count (int):")
        self.count = wx.SpinCtrl(self.panel, size=(60, -1))

        self.sb = wx.StatusBar(self)
        self.sb.SetStatusText("NOT Ready!")
        
 
        self.windowSizer = wx.BoxSizer()
        self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)        

        #Set Grid size
        self.sizer = wx.GridBagSizer(20, 20)
        
        #Set relative positions
        self.sizer.Add(self.label1, (2, 0))
        self.sizer.Add(self.label2, (3, 0))
        self.sizer.Add(self.label3, (4, 0))
        self.sizer.Add(self.label4, (5, 0))
        self.sizer.Add(self.label5, (6, 0))
        

        self.sizer.Add(self.msvc, (2, 1))
        self.sizer.Add(self.delay, (3, 1))
        self.sizer.Add(self.size, (4, 1))
        self.sizer.Add(self.interval, (5, 1))
        self.sizer.Add(self.count, (6, 1))

        self.sizer.Add(self.create, (7, 0),flag=wx.EXPAND)
        self.sizer.Add(self.upgrade, (7, 1),flag=wx.EXPAND)
        self.sizer.Add(self.delete, (7, 2),flag=wx.EXPAND)
        self.sizer.Add(self.start, (7, 3),flag=wx.EXPAND)
        self.sizer.Add(self.Istio,   (1, 0),(1,4),flag=wx.EXPAND)
    

        self.border = wx.BoxSizer()
        self.border.Add(self.sizer, 1, wx.ALL | wx.EXPAND, 5)
        self.panel.SetSizerAndFit(self.border)  
        self.SetSizerAndFit(self.windowSizer)  

        # Set event handlers
        self.create.Bind(wx.EVT_BUTTON, self.OnCreate)
        self.upgrade.Bind(wx.EVT_BUTTON, self.OnUpgrade)
        self.delete.Bind(wx.EVT_BUTTON, self.OnDelete)
        self.start.Bind(wx.EVT_BUTTON, self.OnStart)
        self.Istio.Bind(wx.EVT_TOGGLEBUTTON, self.OnIstio)
        self.start.Disable()
 
    def OnCreate(self, e):
        "Calls create bash script and whn pod is up, sets status to Ready"
        subprocess.check_call(['./deploy/scripts/create.sh', "msvc", str(self.msvc.GetValue()), str(self.delay.GetValue()), str(self.size.GetValue()), str(self.interval.GetValue())])
        while True:
            if check_pod_health():
                """Enable start button and update status"""
                self.start.Enable()
                self.sb.SetStatusText('Ready!!')
                break
        
    def OnUpgrade(self, e):
        "Calls update bash script"
        subprocess.check_call(['./deploy/scripts/update.sh', str(self.msvc.GetValue()), str(self.delay.GetValue()), str(self.size.GetValue()), str(self.interval.GetValue())])
        while True:
            if check_pod_health():
                """Enable start button and update status"""
                self.start.Enable()
                self.sb.SetStatusText('Ready!!')
                break
    def OnDelete(self, e):
        "Calls delete bash script"
        subprocess.check_call('./deploy/scripts/delete.sh')
    def OnStart(self, e):
        "Calls send_pkt on click"
        self.sb.SetStatusText('Experiment started!!')
        send_pkt(self.size.GetValue(), self.count.GetValue(), self.interval.GetValue())
        self.sb.SetStatusText('Experiment stopped!!')
        
    def OnIstio(self, e):
        obj = e.GetEventObject()
        isPressed = obj.GetValue()
        if isPressed:
            _ = subprocess.check_output('kubectl label namespace default istio-injection=enabled',shell=True).decode("utf-8").strip()
            print("Istio enabled")
            self.Istio.SetLabel("Disable Istio")
        else:
            _ = subprocess.check_output('kubectl label namespace default istio-injection-',shell=True).decode("utf-8").strip()
            print("Istio Disabled")
            self.Istio.SetLabel("Enable Istio")
    
app = wx.App(False)
frame = ConfigDash(None)
frame.Show()
app.MainLoop()

