import psutil
import time

total_cpu = 0
count = 0
avg_cpu = -1
avg_io = -1
total_io = 0
f = open("monitor.txt", "a")
f.write("CPU current\tAverage_CPU\tIO_current\tAverage_IO\tMemory\tCPU_1min\tCPU_5min\tCPU_10min\n")
f.close()
while(1):
    f = open("monitor.txt", "a")
    cpu = psutil.cpu_percent()
    count += 1
    total_cpu += cpu
    avg_cpu = total_cpu / count
    io_percent = psutil.disk_usage('/')[3]
    total_io += io_percent
    avg_io = total_io / count
    mem = psutil.virtual_memory()[2]
    f.write(str(cpu)+"\t"+str(avg_cpu)+"\t"+str(io_percent)+"\t"+str(avg_io)+"\t"+str(mem)+"\t"+str(psutil.getloadavg()[0])+"\t"+
            str(psutil.getloadavg()[1])+"\t"+str(psutil.getloadavg()[2])+"\n")
    f.close()
    time.sleep(2)