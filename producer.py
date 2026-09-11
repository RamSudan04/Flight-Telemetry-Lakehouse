import time, json, stomp, random

with open('setting.json', 'r') as f:
    config = json.load(f)

class FlightProducer:
    def __init__(self):
        host, port = config['activemq_ip'], config['activemq']['port']
        user, password = config['activemq']['username'], config['activemq']['password']
        self.destination = config['activemq']['raw_topic']

        self.conn = stomp.Connection([(host, port)])
        self.conn.connect(user, password, wait=True)

    def send_data(self):
        print("Starting flight telemetry stream... (Press Ctrl + C to stop)")
        try:
            while True:
                data = {
                    "speed": round(random.uniform(200.0, 800.0), 2),
                    "altitude": round(random.uniform(10000.0, 35000.0), 2),
                    "roll": round(random.uniform(-45.0, 45.0), 2)
                }
                self.conn.send(body=json.dumps(data), destination=self.destination)
                print(f"📡 Broadcasted to Raw Topic: {data}")
                time.sleep(1)
        except KeyboardInterrupt:
            self.conn.disconnect()

if __name__ == "__main__":
    producer = FlightProducer()
    producer.send_data()