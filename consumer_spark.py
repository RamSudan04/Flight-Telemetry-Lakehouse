import json, time, stomp
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

with open('setting.json', 'r') as f:
    config = json.load(f)

influx_url = f"http://{config['influxdb_ip']}:{config['influxdb']['port']}"
client = InfluxDBClient(url=influx_url, token=config['influxdb']['token'], org=config['influxdb']['org'])
write_api = client.write_api(write_options=SYNCHRONOUS)

class SparkConsumerListener(stomp.ConnectionListener):
    def on_message(self, frame):
        data = json.loads(frame.body)
        point = Point("telemetry").field("speed", data.get("speed", 0)).field("altitude", data.get("altitude", 0)).field("roll", data.get("roll", 0)).time(time.time_ns(), WritePrecision.NS)
        
        if "speed_warning" in data:
            point.field("speed_warning", data["speed_warning"])
            
        write_api.write(bucket=config['influxdb']['spark_bucket'], org=config['influxdb']['org'], record=point)
        print(f"✨ Saved to Spark Bucket: {data}")

host, port = config['activemq_ip'], config['activemq']['port']
conn = stomp.Connection([(host, port)])
conn.set_listener("", SparkConsumerListener())
conn.connect(config['activemq']['username'], config['activemq']['password'], wait=True)

conn.subscribe(destination=config['activemq']['processed_topic'], id=4, ack="auto")
print("Spark Consumer listening... (Press Ctrl + C to stop)")

try:
    while True: time.sleep(1)
except KeyboardInterrupt:
    conn.disconnect()