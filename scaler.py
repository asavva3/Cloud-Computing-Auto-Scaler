import cryptography
from loadbalancer import LoadBalancer
from podman import PodmanClient
import random
import pandas as pd
import math
import numpy as np


class Scaling:

    def __init__(self) -> None:
        self.client = PodmanClient(base_url="unix:///run/podman/podman.sock") 
        self.lb = LoadBalancer()
        self.ids = []
        containers = self.client.containers.list(filters={'ancestor': 'localhost/webapp'})
        for i in containers:
            self.ids.append(i.id)
        self.rates = []

    def getNumberCont(self):
        return len(self.ids)

    def analyzeStats(self):
        df = self.lb.getStatistics()
        s_curr = df['scur']
        avg_resp_time = df['rtime']
        max_resp_time = df['rtime_max']
        req_rate = df['rate']
        q_curr = df['qcur']
        q_time = df['qtime']
        self.rates.append(req_rate.iloc[-1])
        if len(self.rates) == 31:
            self.rates.pop(0)
        if len(self.rates) < 25 and self.getNumberCont() > 0:
            return
        
        avg = np.mean(self.rates)
        std = np.std(self.rates)
        z = 1.645

        if (avg - (std * z)/np.sqrt(len(self.rates))) < req_rate.iloc[-1] < (avg + (std * z)/np.sqrt(len(self.rates))):
            return

        n = 0
        
        n = math.ceil(avg / 10)

        mod = avg % 10

        if n < self.getNumberCont():
            if n == self.getNumberCont() - 1:
                if mod >= 5:
                    n = self.getNumberCont()
        elif mod < 2:
            if n == self.getNumberCont() + 1:
                n == self.getNumberCont()
        
        if n == 0:
            n = 1
        if n == self.getNumberCont():
            return
        # get old ids to comapre and see if ids have changed
        old_ids = self.ids.copy()
        conts = self.getNumberCont()
        if conts > n:
            self.deleteCont(conts-n)
        elif conts < n:
            print("Created cont")
            self.createCont(n - conts)

        # switch haproxy
        if not self.ids == old_ids:
            ips = self.get_ips()
            self.lb.updateConfig(ips)
            self.lb.fixImage()
            self.lb.switchHaproxy()
            

    def createCont(self, n_containers):
        for index in range(n_containers):
            created = self.client.containers.create("webapp", "", mounts=[{"type": "bind", "source": "/srv/objects", "target": "/data"}], detach = True)
            container = self.client.containers.get(created.id)
            container.start()
            container.wait(condition = 'running')
            self.ids.append(container.id)

    def deleteCont(self, n_containers):
        ids = []
        rand_id = random.sample(self.ids, n_containers)
        for i in rand_id:
            curr = self.client.containers.get(i)
            curr.stop()
            self.client.containers.remove(i)
            self.ids.remove(i)

    def get_ips(self):
        ips = []
        for item in self.ids:
            c = self.client.containers.get(item)
            c.wait(condition = 'running')
            if c.status == 'running':
                ips.append(c.attrs['NetworkSettings']['Networks']['podman']['IPAddress'])
        return ips

