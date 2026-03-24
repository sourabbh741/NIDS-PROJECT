from scapy.all import sniff, IP
import matplotlib.pyplot as plt
from collections import deque

# Data storage
packet_counts = deque(maxlen=50)

count = 0

plt.ion()  # interactive mode ON

def detect(packet):
    global count
    
    if packet.haslayer(IP):
        count += 1
        
        packet_counts.append(count)

        print(f"Packets: {count}")

        # Graph update
        plt.clf()
        plt.plot(packet_counts)
        plt.title("Real-Time Packet Count")
        plt.xlabel("Time")
        plt.ylabel("Packets")
        plt.pause(0.01)

print("🚀 NIDS with Real-Time Graph Started")
sniff(prn=detect, store=False)