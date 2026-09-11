# Dual-Pipeline Grafana Flux Queries (DRDO Telemetry)

This document contains the Flux queries to visualize both the Direct (Raw) pipeline and the PySpark (Batch) pipeline simultaneously on the same dashboard panels.

**Data Source Configuration:**
* **Language:** Flux
* **Default Bucket:** `flight-data` (Note: Queries explicitly call `flight-data-spark` where needed)

## 1. Speed Comparison Panel
Plot these two queries on the same "Time series" graph to compare raw ingestion vs. 8-second PySpark batching.

**Query A (Raw Speed):**
```flux
from(bucket: "flight-data")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "telemetry")
  |> filter(fn: (r) => r["_field"] == "speed")
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
  |> yield(name: "Raw_Speed")

  #Query B (PySpark Speed):
  from(bucket: "flight-data-spark")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "telemetry")
  |> filter(fn: (r) => r["_field"] == "speed")
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
  |> yield(name: "PySpark_Speed")

  #2. Altitude Comparison Panel

   #Query A (Raw Altitude):
   from(bucket: "flight-data")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "telemetry")
  |> filter(fn: (r) => r["_field"] == "altitude")
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
  |> yield(name: "Raw_Altitude")
  
  #Query B (PySpark Altitude):
  from(bucket: "flight-data-spark")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "telemetry")
  |> filter(fn: (r) => r["_field"] == "altitude")
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
  |> yield(name: "PySpark_Altitude")

  #3. Roll Comparison Panel
  #Query A (Raw Roll):
  from(bucket: "flight-data")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "telemetry")
  |> filter(fn: (r) => r["_field"] == "roll")
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
  |> yield(name: "Raw_Roll")
  
  #Query B (PySpark Roll):
from(bucket: "flight-data-spark")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "telemetry")
  |> filter(fn: (r) => r["_field"] == "roll")
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
  |> yield(name: "PySpark_Roll")