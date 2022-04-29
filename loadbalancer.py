import requests
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
            contents += '\n\tserver server'+str(count) +' '+i+":5000"
            count += 1
        contents += '\n'
        f.write(contents)
        f.close()

    def overwriteConfig(self):
        shutil.copy('haproxy.cfg', '/etc/haproxy/')

lb = LoadBalancer()
ips = ['127.0.0.1', '127.0.0.2']
lb.updateConfig(ips)
