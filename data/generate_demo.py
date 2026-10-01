import random, csv
random.seed(42)
with open("demo_events.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["latency_ms","amount","decline_rate","retries"])
    for i in range(500):
        w.writerow([round(random.gauss(120,18),2),round(random.gauss(1000,150),2),round(random.uniform(.01,.08),3),random.randint(0,2)])
    for i in range(12):
        w.writerow([round(random.gauss(900,80),2),round(random.gauss(7000,500),2),round(random.uniform(.55,.9),3),random.randint(6,12)])
