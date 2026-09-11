# Flight Telemetry Data Architecture

## 1. Project Overview
This repository implements a multi-tiered Data Engineering architecture designed to process high-velocity flight telemetry. By routing message streams through specialized channels, the system bridges the gap between low-latency real-time tracking and distributed enterprise storage, ensuring optimal performance for varying analytical needs.

## 2. Architecture Flowchart

```mermaid
graph TD
    A[Flight Telemetry Producer] -->|Generates JSON| B(Apache ActiveMQ)
    B -->|Stream| C[Python Consumer]
    C --> D[(InfluxDB)]
    D --> E[Grafana Real-Time Dashboard]
    B -->|Stream| F[Apache PySpark]
    F --> G[Live Analytics & Alerts]
    H[Prometheus] -->|Scrapes Container Health| E
    B -->|Stream| I[Apache NiFi]
    I -->|100MB Bin-Packing| J[(Hadoop HDFS Data Lake)]
    J --> K[Trino SQL Engine]
    K --> E

    3. Pipeline Breakdown
The system utilizes Apache ActiveMQ as the central message broker, fanning data out to four distinct paths:

Pipeline 1 (Real-Time Time-Series): Routes telemetry to InfluxDB for instantaneous visualization and tracking via Grafana.

Pipeline 2 (Micro-Batch Analytics): Employs Apache PySpark for live data aggregation, fault detection, and threshold alerting.

Pipeline 3 (System Monitoring): Uses Prometheus to scrape infrastructure health and container performance metrics.

Pipeline 4 (Big Data Lakehouse): Compresses high-speed streams into 100MB HDFS blocks via Apache NiFi, which are then mapped for historical Trino SQL querying.

4. Execution: Individual Pipelines
To respect standard hardware memory limits, you must clear your Docker engine first by typing docker rm -f $(docker ps -a -q) in your terminal. Then, run pipelines in isolation.

Pipelines 1 & 3: Time-Series & Monitoring

Step 1: Boot the stack by running docker compose -f docker-compose.yml up -d influxdb grafana activemq prometheus

Step 2: Start the data stream by running python producer.py

Step 3: Start the database consumer by running python influx_consumer.py

Step 4: View the live dashboards by opening http://localhost:3001 in your browser.

Pipeline 2: Spark Analytics

Step 1: Boot the broker by running docker compose -f docker-compose.yml up -d activemq

Step 2: Start the data stream by running python producer.py

Step 3: Start the analytics engine by running python spark_processor.py

Pipeline 4: Big Data Lakehouse

Step 1: Boot the architecture by running docker compose -f docker-compose-lakehouse.yml up -d

Step 2: Start the data stream by running python producer.py

Step 3: Build the drag-and-drop flow in Apache NiFi at https://localhost:8443/nifi

Step 4: Map the SQL schema by running docker exec -it <trino_container_name> trino

5. Execution: Combined System
If deploying on a high-performance workstation, you can run the entire architecture simultaneously to watch data route through all four pipelines at once.

Boot the primary stack: docker compose -f docker-compose.yml up -d

Boot the Lakehouse stack: docker compose -f docker-compose-lakehouse.yml up -d

Start the Python scripts: python producer.py, then python influx_consumer.py, then python spark_processor.py

6. Legal
Copyright (c) 2026 Ram Sudan. All Rights Reserved.
This project and its source code are strictly proprietary. No part of this software may be copied, reproduced, or distributed without prior written permission.
