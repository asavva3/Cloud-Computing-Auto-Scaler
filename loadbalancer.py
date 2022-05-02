from locale import currency
import requests
import pandas as pd
from io import StringIO
import shutil
import os
from podman import PodmanClient
from multiprocessing import Process


class LoadBalancer:
    
    def __init__(self) -> None:
        self.client = PodmanClient(base_url="unix:///run/podman/podman.sock")
        cont_list = self.client.containers.list(filters={'ancestor': 'localhost/haproxyimg'})
        self.current = None
        if len(cont_list) > 0:
            self.current = self.client.containers.get(cont_list[0].id)
        self.current.wait(condition='running')
        ip = self.current.attrs['NetworkSettings']['Networks']['podman']['IPAddress']
        self.uri = "http://"+ip+":9999/stats;csv"

    def getStatistics(self):
        response = requests.get(self.uri)
        status = response.status_code
        if not status == 200:
            print("Error")
            exit()
        results = response.text
        df = pd.read_csv(filepath_or_buffer=StringIO(results), sep=",")
        return df

    def updateConfig(self, ips):
        f = open("defaulthap.cfg", "r")
        contents = f.read()
        f.close()
        f = open("haproxy.cfg", "w")
        count = 0
        for i in ips:
            contents += '\n\tserver server'+str(count) +' '+i+":5000"
            count += 1
        contents += '\n'
        f.write(contents)
        f.close()

    def overwriteConfig(self):
        shutil.copy('haproxy.cfg', '/etc/haproxy/')

    def fixImage(self):
        os.system('buildah copy haproxycontainer haproxy.cfg /etc/haproxy/haproxy.cfg')
        os.system('buildah commit haproxycontainer haproxyimg')
    
    def switchHaproxy(self):
        os.system(f"podman run -d --network container:wait --rm haproxyimg")
        cont_list = self.client.containers.list(filters={'ancestor': 'localhost/haproxyimg'})
        created_cont_id = None
        created = None
        if len(cont_list):
            for i in cont_list:
                if not i.id == self.current.id:
                    created_cont_id = i.id
                    break
        if created_cont_id is None:
            return False
        created = self.client.containers.get(created_cont_id)
        created.start()
        created.wait(condition='running')
        if not created.status == 'running':
            return False
        self.current.stop()
        self.current = created
        return True
