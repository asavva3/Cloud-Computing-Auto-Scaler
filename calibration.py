import os
from podman import PodmanClient

rand_delay_min=[5, 100, 5]
rand_delay_max=[20, 200, 200]
req_per_seq=[10, 50, 100]
users=[10, 20, 40, 80]

client = PodmanClient(base_url="unix:///run/podman/podman.sock")

for u in users:
    for i in range(len(rand_delay_min)):
        for j in range(len(req_per_seq)):
            os.system(f'buildah config --entrypoint "python3 objst.py {rand_delay_min[i]} {rand_delay_max[i]} {req_per_seq[j]}" alpine-working-container')
            os.system("buildah commit alpine-working-container objstpyimage")
            created = client.containers.create("objstpyimage", "", mounts=[{"type": "bind", "source": "/srv/objects", "target": "/data"}], detach = True)
            container = client.containers.get(created.id)
            container.start()
            c = client.containers.get(container.id)
            ip = c.attrs['NetworkSettings']['Networks']['podman']['IPAddress']
            os.system(f'''podman exec -it {created.id} nohup python3 monitor.py &''')
            os.system(f"locust -f test.py -u {u} -r {5} -t1m --headless --csv=example -H http://{ip}:5000")
            os.system(f"mv example_stats.csv results/{u}users{rand_delay_min[i]}min{rand_delay_max[i]}max{j}req_stats.csv")
            os.system(f"mv example_failures.csv results/{u}users{rand_delay_min[i]}min{rand_delay_max[i]}max{j}req_failures.csv")
            os.system(f"podman cp {created.id}:/monitor.txt monitor{u}users{rand_delay_min[i]}min{rand_delay_max[i]}max{j}.txt")
            container.stop()
            client.containers.remove(created.id)
            
