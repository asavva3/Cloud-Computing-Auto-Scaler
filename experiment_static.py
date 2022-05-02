import os
from podman import PodmanClient

rand_delay_min=5
rand_delay_max=20
req_per_seq=15
users=[15, 80]

client = PodmanClient(base_url="unix:///run/podman/podman.sock")
for u in users:
	os.system(f"locust -f loadtest.py -u {u} -r 5 -t2m --headless --csv=example -H http://10.88.0.44:8080")
	os.system(f"mv example_stats.csv results/final/{u}stats.csv")
	os.system(f"mv example_failures.csv results/final/{u}failures.csv")
	containers = client.containers.list(filters={'ancestor': 'localhost/webapp'})
	while(len(containers)!= 1):
		containers = client.containers.list(filters={'ancestor': 'localhost/webapp'})