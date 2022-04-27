from loadbalancer import LoadBalancer
from podman import PodmanClient


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

oh = Scaling()
n_cont = oh.createCont(3)
ips = oh.get_ips()

