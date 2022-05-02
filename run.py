from scaler import Scaling

sc = Scaling()
current_cont = sc.getNumberCont()
print("Starting with: ", current_cont)
while(1):
    sc.analyzeStats()
    if not sc.getNumberCont == current_cont:
        print("Containers where: ", current_cont)
        current_cont = sc.getNumberCont()
        print("Current containers: ", current_cont)