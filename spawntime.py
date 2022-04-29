import time
import numpy as np
from podman import PodmanClient
from scaler import Scaling

sc = Scaling()

client = PodmanClient(base_url="unix:///run/podman/podman.sock") 

f = open("spawntimes.txt", "w")

# check time for spawning continuously
for i in range(3):
    times = []
    for index in range(10):
        start_time = time.time()
        created = client.containers.create("webapp", "", mounts=[{"type": "bind", "source": "/srv/objects", "target": "/data"}], detach = True)
        container = client.containers.get(created.id)
        container.start()
        container.wait(condition = 'running')
        end_time = time.time()
        elapsed = end_time - start_time
        times.append(elapsed)
        f.write(str(elapsed)+"\t")
    f.write(np.mean(times))
    f.write("\n")
    sc.deleteCont(0)

# check for individual container
times = []
for i in range(10):
    start_time = time.time()
    created = client.containers.create("webapp", "", mounts=[{"type": "bind", "source": "/srv/objects", "target": "/data"}], detach = True)
    container = client.containers.get(created.id)
    container.start()
    container.wait(condition = 'running')
    end_time = time.time()
    elapsed = end_time - start_time
    times.append(elapsed)
    f.write(str(elapsed)+"\t")
    sc.deleteCont(0)

f.write(np.mean(times)+"\n")
f.close()