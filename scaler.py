from loadbalancer import LoadBalancer
from podman import PodmanClient
import random
import pandas as pd



class Scaling:
    def __init__(self) -> None:
        self.client = PodmanClient(base_url="unix:///run/podman/podman.sock") 
        self.lb = LoadBalancer()
        self.ids = []
        containers = self.client.containers.list()
        for i in containers:
            self.ids.append(i.id)

    def analyzeStats(self):
        df = self.lb.getStatistics()
        s_curr = df['scurr']
        avg_resp_time = df['rtime']
        max_resp_time = df['rtime_max']

        # if req_rate > session rate container (ena pou cracharei kai ena pou den gia na testaroume)
        # cpu
        # if response time is over 130 and we measure that each of our container servers around 4-5 connections,
        # increase containers
        # qcurr and qtime if > 0 create container
        # rate: posous eksipiretei tautoxrona 
        if avg_resp_time.iloc[-1] < 100:
            self.createCont(1)

        




    def createCont(self, n_containers):
        for index in range(n_containers):
            created = self.client.containers.create("webapp", "", mounts=[{"type": "bind", "source": "/srv/objects", "target": "/data"}], detach = True)
            container = self.client.containers.get(created.id)
            container.start()
            container.wait(condition = 'running')
            self.ids.append(container.id)

    def deleteCont(self, n_containers):
        containers = self.client.containers.list()
        n_curr = len(containers)
        ids = []
        if n_curr > n_containers and n_containers >= 0:
                rand_id = random.sample(self.ids, n_curr-n_containers)
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


print("Starting number of containers: 0")
n_containers = 3
oh = Scaling()
print(oh.client.containers.list())
oh.deleteCont(n_containers)
print("After trying to delete 3, we have: ", len(oh.ids))
print(oh.client.containers.list())
n_cont = oh.createCont(n_containers)
print("Created: ", len(oh.ids))
print(oh.client.containers.list())
ips = oh.get_ips()
print("Ips ", ips)
print("trying to have 1 container")
oh.deleteCont(1)
print("We have: ", len(oh.ids))
print(oh.client.containers.list())
