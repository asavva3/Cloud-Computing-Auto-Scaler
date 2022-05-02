import os
from podman import PodmanClient
from loadbalancer import LoadBalancer
from scaler import Scaling

rand_delay_min=[5, 100, 5]
rand_delay_max=[20, 200, 200]
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
				print("Testing for ",c," containers| Users ", u," delay ",rand_delay_min[i],":",rand_delay_max[i]," requests ", req_per_seq[j])
				os.system(f'buildah config --entrypoint "python3 objst.py {rand_delay_min[i]} {rand_delay_max[i]} {req_per_seq[j]}" webappcontainer')
				os.system("buildah commit webappcontainer webapp")
				sc.createCont(c)
				ips = sc.get_ips()
				lb.updateConfig(ips)
				lb.fixImage()
				lb.switchHaproxy()
				os.system(f"locust -f loadtest.py -u {u} -r 5 -t1m --headless --csv=example -H http://10.88.0.44:8080")
				os.system(f"mv example_stats.csv results/multiple/{c}cont{u}users{rand_delay_min[i]}min{rand_delay_max[i]}max{j}req_stats.csv")
				os.system(f"mv example_failures.csv results/multiple/{c}ccont{u}users{rand_delay_min[i]}min{rand_delay_max[i]}max{j}req_failures.csv")
				sc.deleteCont(c)