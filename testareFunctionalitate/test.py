networks = []

with open('test.txt', 'r') as f:
    for line in f:
        if "C " in line:
            parts = line.split()
            network = parts[1].split('/')[0]
            networks.append(network)

for network in networks:
    print(network)