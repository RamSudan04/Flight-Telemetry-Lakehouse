# Flight Telemetry Data Architecture

## Project Overview
This repository contains a comprehensive, multi-tiered Data Engineering architecture designed for flight telemetry. To handle varying requirements for latency, analytics, and historical storage, the system routes high-speed message streams through four distinct processing pipelines. 

## The Four Pipelines
This architecture utilizes Apache ActiveMQ as the central message broker, fanning out telemetry data to the following isolated pipelines:

*   **Pipeline 1: Real-Time Time-Series (Ultra-Low Latency)**
    *   **Flow:** ActiveMQ -> Python Consumer -> InfluxDB -> Grafana
    *   **Purpose:** Instantaneous metric visualization using Flux queries for live flight tracking.
*   **Pipeline 2: Micro-Batch Processing (Analytics & Alerting)**
    *   **Flow:** ActiveMQ -> Apache Spark (PySpark)
    *   **Purpose:** Real-time data aggregation, fault detection, and threshold warning flags.
*   **Pipeline 3: System Monitoring (Pull-Based Metrics)**
    *   **Flow:** Prometheus -> Grafana
    *   **Purpose:** Infrastructure health monitoring and metric scraping.
*   **Pipeline 4: Big Data Lakehouse (Historical Batch Storage)**
    *   **Flow:** ActiveMQ -> Apache NiFi -> Hadoop (HDFS) -> Trino -> Grafana
    *   **Purpose:** Compresses high-velocity streams into 100MB blocks via NiFi Bin-Packing, mapping them to a Hive Metastore for historical SQL querying via Trino.

## Operational Guide (Isolated Execution)
Due to the heavy JVM memory requirements of these enterprise systems, the pipelines are divided into specific `docker-compose` files to allow isolated execution on standard hardware.

**To run a specific pipeline, ensure all others are shut down first:**
`docker rm -f $(docker ps -a -q)`

**1. Booting the Time-Series & Monitoring Stack (Pipelines 1 & 3)**
```bash
docker-compose -f docker-compose.yml up -d
python producer.py
python influx_consumer.py

**2. Booting the Spark Analytics Stack (Pipeline 2)**

Bash
# Ensure ActiveMQ is running
python producer.py
python spark_processor.py
**3. Booting the Big Data Lakehouse (Pipeline 4)**

Bash
docker-compose -f docker-compose-lakehouse.yml up -d
python producer.py
# Access NiFi UI at https://localhost:8443/nifi to initialize the flow
Legal
Copyright (c) 2026 Ram Sudan. All Rights Reserved.
This architecture and its source code are proprietary. See the LICENSE file for details.
