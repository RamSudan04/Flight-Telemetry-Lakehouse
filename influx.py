import requests
import json
import time

with open('setting.json', 'r') as f:
    config = json.load(f)

ip = config['influxdb_ip']
port = config['influxdb']['port']
base_url = f"http://{ip}:{port}/api/v2"

setup_payload = {
    "username": config['influxdb']['username'],
    "password": config['influxdb']['password'],
    "org": config['influxdb']['org'],
    "bucket": config['influxdb']['direct_bucket'],
    "retentionPeriodHrs": 0
}

try:
    print("Initializing InfluxDB...")
    response = requests.post(f"{base_url}/setup", json=setup_payload)
    
    if response.status_code in [200, 201]:
        new_token = response.json()['auth']['token']
        
        # Save token
        config['influxdb']['token'] = new_token
        with open('setting.json', 'w') as f:
            json.dump(config, f, indent=2)
        print("✅ Token saved to setting.json.")
        
        # Get Org ID for creating extra buckets
        headers = {"Authorization": f"Token {new_token}"}
        org_res = requests.get(f"{base_url}/orgs?org={config['influxdb']['org']}", headers=headers)
        org_id = org_res.json()['orgs'][0]['id']
        
        # Create second bucket (PySpark)
        bucket_payload_spark = {"orgID": org_id, "name": config['influxdb']['spark_bucket']}
        requests.post(f"{base_url}/buckets", headers=headers, json=bucket_payload_spark)
        print(f"✅ Second bucket '{config['influxdb']['spark_bucket']}' created!")

        # Create third bucket (Prometheus)
        bucket_payload_prom = {"orgID": org_id, "name": config['influxdb']['prometheus_bucket']}
        requests.post(f"{base_url}/buckets", headers=headers, json=bucket_payload_prom)
        print(f"✅ Third bucket '{config['influxdb']['prometheus_bucket']}' created!")
        
    elif response.status_code == 409:
        print("ℹ️ InfluxDB is already configured.")
    else:
        print(f"❌ Error: {response.text}")
except Exception as e:
    print(f"❌ Failed to connect: {e}")