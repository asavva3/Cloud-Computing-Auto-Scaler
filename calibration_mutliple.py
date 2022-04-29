import os
from podman import PodmanClient
from loadbalancer import LoadBalancer
from scaler import Scaling

rand_delay_min=[100, 5]
rand_delay_max=[200, 200]
req_per_seq=[50, 100]
users=[20, 40, 80]
containers = [2, 6]
ips = []
client = PodmanClient(base_url="unix:///run/podman/podman.sock")
lb = LoadBalancer()
sc = Scaling()

for c in containers:
    for u in users:
        for i in range(len(rand_delay_min)):
            for j in range(len(req_per_seq)):
                os.system(f'buildah config --entrypoint "python3 objst.py {rand_delay_min[i]} {rand_delay_max[i]} {req_per_seq[j]}" alpine-working-container')
                os.system("buildah commit alpine-working-container objstpyimage")
                sc.createCont(c)
                ips = sc.get_ips()
                lb.updateConfig(ips)
                lb.overwriteConfig()
                os.system("systemctl restart haproxy")
                os.system(f"locust -f test.py -u {u} -r {5} -t1m --headless --csv=example -H http://127.0.0.1:8080")
                os.system(f"mv example_stats.csv results/{c}cont{u}users{rand_delay_min[i]}min{rand_delay_max[i]}max{j}req_stats.csv")
                os.system(f"mv example_failures.csv results/{c}cont{u}users{rand_delay_min[i]}min{rand_delay_max[i]}max{j}req_failures.csv")
                sc.deleteCont(0)
