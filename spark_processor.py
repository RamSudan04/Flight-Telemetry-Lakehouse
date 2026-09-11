import os
import json
import time
import stomp
import threading
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, DoubleType

# 1. Force PySpark to use standard localhost
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"

with open('setting.json', 'r') as f:
    config = json.load(f)

# 2. Rock-solid Spark Configuration
spark = SparkSession.builder \
    .appName("FlightDataProcessor") \
    .config("spark.network.timeout", "600s") \
    .config("spark.executor.heartbeatInterval", "120s") \
    .config("spark.driver.memory", "2g") \
    .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
    .getOrCreate()

# 3. Explicit Schema (Prevents Schema Inference Crashes)
telemetry_schema = StructType([
    StructField("speed", DoubleType(), True),
    StructField("altitude", DoubleType(), True),
    StructField("roll", DoubleType(), True)
])

batch_data = []
batch_lock = threading.Lock()

class SparkProcessorListener(stomp.ConnectionListener):
    def on_error(self, frame):
        print(f"⚠️ ActiveMQ Error: {frame.body}")
        
    def on_disconnected(self):
        print("⚠️ Warning: Disconnected from ActiveMQ.")

    def on_message(self, frame):
        try:
            data = json.loads(frame.body)
            with batch_lock:
                batch_data.append(data)
        except Exception as e:
            print(f"⚠️ Dropped malformed message: {e}")

host, port = config['activemq_ip'], config['activemq']['port']
user, password = config['activemq']['username'], config['activemq']['password']
dest_topic = config['activemq']['processed_topic']

conn = stomp.Connection([(host, port)])
conn.set_listener("", SparkProcessorListener())
conn.connect(user, password, wait=True)
conn.subscribe(destination=config['activemq']['raw_topic'], id=2, ack="auto")

print("PySpark Processor started. Batching every 8 seconds... (Press Ctrl + C to stop)")

try:
    while True:
        # Give Spark 8 solid seconds to gather data
        time.sleep(8.0)
        
        with batch_lock:
            current_batch = batch_data[:]
            batch_data.clear()
            
        if current_batch:
            try:
                # Using the explicit schema makes the process instant and crash-proof
                df = spark.createDataFrame(current_batch, schema=telemetry_schema)
                processed_df = df.withColumn("speed_warning", col("speed") > 750.0)
                
                for row in processed_df.toJSON().collect():
                    conn.send(body=row, destination=dest_topic)
                    print(f"⚙️ PySpark Processed & Sent: {row}")
                    
            except Exception as e:
                # If a batch fails, it skips it and safely waits for the next 8 seconds
                print(f"⚠️ Batch processing skipped due to error: {e}")

except KeyboardInterrupt:
    print("\nShutting down PySpark cleanly...")
finally:
    # 4. Guaranteed cleanup prevents locked ports on restart
    if conn.is_connected():
        conn.disconnect()
    spark.stop()