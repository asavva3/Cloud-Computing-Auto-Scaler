# import requests
import pandas as pd
from io import StringIO
import shutil

class LoadBalancer:
    
    def __init__(self) -> None:
        self.uri = "http://127.0.0.1:9999/stats;csv"

    def getStatistics(self):
        response = requests.get(self.uri)
        status = response.status_code
        if not status == 200:
            print("Error")
            exit()
        results = response.text
        df = pd.read_csv(StringIO(results), ",")
        return df

    def updateConfig(self, ips):
        f = open("defaulthap.cfg", "r")
        contents = f.read()
        f.close()
        f = open("haproxy.cfg", "w")
        count = 0
        for i in ips:
            contents += '\n\tserver server'+str(count) +' '+i
            count += 1
        f.write(contents)
        f.close()

    def overwriteConfig(self):
        shutil.copy('haproxy.cfg', '/etc/haproxy/')

lb = LoadBalancer()
ips = ['127.0.0.1', '127.0.0.2', '127.0.0.3']
lb.updateConfig(ips)        
