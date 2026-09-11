# Flight Telemetry Data Architecture

## 1. Project Overview
This repository implements a multi-tiered Data Engineering architecture designed to process high-velocity flight telemetry. By routing message streams through specialized channels, the system bridges the gap between low-latency real-time tracking and distributed enterprise storage, ensuring optimal performance for varying analytical needs.

## 2. Pipeline Architecture
The system utilizes Apache ActiveMQ as the central message broker, fanning data out to four distinct paths:
*   **Pipeline 1 (Real-Time Time-Series):** Routes telemetry to InfluxDB for instantaneous visualization and tracking via Grafana.
*   **Pipeline 2 (Micro-Batch Analytics):** Employs Apache PySpark for live data aggregation, fault detection, and threshold alerting.
*   **Pipeline 3 (System Monitoring):** Uses Prometheus to scrape infrastructure health and container performance metrics.
*   **Pipeline 4 (Big Data Lakehouse):** Compresses high-speed streams into 100MB HDFS blocks via Apache NiFi, which are then mapped to a Hive Metastore for historical Trino SQL querying.

## 3. Execution: Individual Pipelines
To respect standard hardware memory limits, clear your Docker engine first (`docker rm -f $(docker ps -a -q)`), then run pipelines in isolation:

**Pipelines 1 & 3 (Time-Series & Monitoring)**
```bash
docker compose -f docker-compose.yml up -d influxdb grafana activemq prometheus
python producer.py
python influx_consumer.py
(Access dashboards at http://localhost:3001)

Pipeline 2 (Spark Analytics)

Bash
docker compose -f docker-compose.yml up -d activemq
python producer.py
python spark_processor.py
Pipeline 4 (Big Data Lakehouse)

Bash
docker compose -f docker-compose-lakehouse.yml up -d
python producer.py
(Configure the flow in NiFi at https://localhost:8443/nifi and map the Trino schema via the command line).

4. Execution: Combined System & Legal
If deploying on a high-performance workstation (16GB+ RAM), you can run the entire architecture simultaneously to watch data route through all four pipelines at once.

Bash
docker compose -f docker-compose.yml up -d
docker compose -f docker-compose-lakehouse.yml up -d
python producer.py
python influx_consumer.py
python spark_processor.py
Copyright (c) 2026 Ram Sudan. All Rights Reserved.
This project and its source code are strictly proprietary. No part of this software may be copied, reproduced, or distributed without prior written permission.
