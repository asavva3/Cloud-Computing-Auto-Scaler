from loadbalancer import LoadBalancer
from podman import PodmanClient
import random



class Scaling:
    def __init__(self) -> None:
        self.client = PodmanClient(base_url="unix:///run/podman/podman.sock") 

    def createCont(self, n_containers):
    	for index in range(n_containers):
            print("Creating container....")
            created = self.client.containers.create("webapp", "", mounts=[{"type": "bind", "source": "/srv/objects", "target": "/data"}], detach = True)
            container = self.client.containers.get(created.id)
            container.start()
            print("Container created successfully!", container.id)  

    def deleteCont(self, n_containers):
        
        containers = self.client.containers.list()
        n_curr = len(containers)
        ids = []
        if n_curr > n_containers:	
            for item in containers:
                names = self.client.containers.get(item.name)
                ids.append(names.id)

            rand_id = random.sample(ids, n_curr-n_containers)
            for i in rand_id:
                curr = self.client.containers.get(i)
                curr.stop()
                self.client.containers.remove(i)
        else:
            exit()

    def get_ips(self):
        containers = self.client.containers.list()
        ips = []
        for item in containers: 
            name = item.name
            c = self.client.containers.get(name)
            c.wait(condition = 'running')
            c = self.client.containers.get(c.id)
            if c.status == 'running':
                ips.append(c.attrs['NetworkSettings']['Networks']['podman']['IPAddress'])
        return ips



n_containers = 8
oh = Scaling()
delete = oh.deleteCont(n_containers)
n_cont = oh.createCont(n_containers)
ips = oh.get_ips()



