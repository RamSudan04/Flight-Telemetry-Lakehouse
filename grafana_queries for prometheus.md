---

## 5. Prometheus Metrics Pipeline (PromQL)

For the metric-based pipeline, Grafana connects directly to Prometheus (`http://prometheus:9090`) using PromQL. 

### Data Source Configuration:
* **Type:** Prometheus
* **URL:** `http://prometheus:9090`

### PromQL Queries:

**1. Flight Speed Metric:**
```promql
flight_speed_knots


2. Flight Altitude Metric:

flight_altitude_feet

3. Flight Roll Metric:

flight_roll_degrees