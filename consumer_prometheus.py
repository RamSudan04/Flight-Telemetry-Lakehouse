import json
import time
import stomp
from prometheus_client import start_http_server, Gauge

with open('setting.json', 'r') as f:
    config = json.load(f)

# Define Prometheus Metric Gauges
PROM_SPEED = Gauge('flight_speed_knots', 'Current flight speed in knots')
PROM_ALTITUDE = Gauge('flight_altitude_feet', 'Current flight altitude in feet')
PROM_ROLL = Gauge('flight_roll_degrees', 'Current flight roll angle')

class PrometheusExporterListener(stomp.ConnectionListener):
    def on_message(self, frame):
        try:
            data = json.loads(frame.body)
            # Update metric values instantly when a new message arrives from the topic
            PROM_SPEED.set(data.get("speed", 0))
            PROM_ALTITUDE.set(data.get("altitude", 0))
            PROM_ROLL.set(data.get("roll", 0))
            print(f"📊 Prometheus Metrics Updated: {data}")
        except Exception as e:
            print(f"⚠️ Exporter error: {e}")

# Start local HTTP server for Prometheus to scrape
start_http_server(8000)
print("Prometheus Exporter HTTP server running on http://localhost:8000/metrics")

host, port = config['activemq_ip'], config['activemq']['port']
user, password = config['activemq']['username'], config['activemq']['password']

conn = stomp.Connection([(host, port)])
conn.set_listener("", PrometheusExporterListener())
conn.connect(user, password, wait=True)

# Subscribe to the existing raw topic—ActiveMQ will broadcast a copy here automatically!
conn.subscribe(destination=config['activemq']['raw_topic'], id=5, ack="auto")
print("Prometheus Consumer listening... (Press Ctrl + C to stop)")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    conn.disconnect()