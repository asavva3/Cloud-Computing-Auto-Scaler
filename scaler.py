from loadbalancer import LoadBalancer
from podman import PodmanClient



class Scaling:

    def __init__(self) -> None:
        self.client = PodmanClient(base_url="unix:///run/podman/podman.sock") 


    def createCont(self, n_containers):
            for index in range(n_containers):
                self.client.containers.run("webapp", detach = True)
    
    def get_ips(self):
        containers = self.client.containers.list()
        ips = []
        
        for item in containers: 
            name = item.name
            c = self.client.containers.get("name")
            if c.status == 'running':
                ips.append(c.attrs['NetworkSettings']['Networks']['podman']['IPAddress'])

        return ips


