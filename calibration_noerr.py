import os
from podman import PodmanClient
from loadbalancer import LoadBalancer
from scaler import Scaling

rand_delay_min=5
rand_delay_max=20
req_per_seq=100
users=80
containers = [1, 2, 6]
ips = []
client = PodmanClient(base_url="unix:///run/podman/podman.sock")
lb = LoadBalancer("http://10.88.0.44")
sc = Scaling()

for c in containers:
    os.system(f'buildah config --entrypoint "python3 objst.py {rand_delay_min} {rand_delay_max} {req_per_seq}" webappcontainer')
    os.system("buildah commit webappcontainer webapp")
    sc.createCont(c)
    ips = sc.get_ips()
    lb.updateConfig(ips)
    lb.fixImage()
    lb.switchHaproxy()
    os.system(f"locust -f loadtest_noerr.py -u {users} -r 5 -t1m --headless --csv=example -H http://10.88.0.44:8080")
    os.system(f"mv example_stats.csv results/noerrors/{c}cont_stats.csv")
    os.system(f"mv example_failures.csv results/noerrors/{c}cont_req_failures.csv")
    sc.deleteCont(c)