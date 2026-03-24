from flask import Flask, jsonify
from scapy.all import sniff, IP
from threading import Thread

app = Flask(__name__)

packet_count = 0
alerts = []

def detect(packet):
    global packet_count

    if packet.haslayer(IP):
        packet_count += 1

        if packet_count > 20:
            alert = f"🚨 Suspicious traffic detected: {packet_count}"
            alerts.append(alert)
            print(alert)

def sniff_packets():
    sniff(prn=detect, store=False)

# Run sniffing in background
thread = Thread(target=sniff_packets)
thread.daemon = True
thread.start()

@app.route("/")
def home():
    return f"""
    <h1>NIDS Dashboard</h1>
    <p>Packets: {packet_count}</p>
    <p>Alerts: {alerts}</p>
    """

@app.route("/data")
def data():
    return jsonify({
        "packets": packet_count,
        "alerts": alerts
    })

if __name__ == "__main__":
    app.run(debug=True)