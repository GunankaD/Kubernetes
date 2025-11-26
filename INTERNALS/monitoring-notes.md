## EXERCISE 6.
0. to enter the virtual environment, go exercise6-monitoring folder
    > venv\Scripts\Activate.ps1
    - and run the above command. (this assumes virtual environment was already created)

1. prometheus client
    - A Prometheus client refers to a library or tool that allows an application to expose metrics in a format that the Prometheus monitoring system can scrape and collect.
    - create `delivery_metrics.py` which has 2 types of metrics: Gauge and Summary.
      - Gauges: `total_deliveries`, `pending_deliveries`, `on_the_way_deliveries` (use `.set(value)`).
      - Summary: `average_delivery_time` (use `.observe(value)`).
    - serve metrics on `http://localhost:8000/metrics` using `prometheus_client.start_http_server(8000, addr="0.0.0.0")`.
    - quick local check:
      > curl.exe http://localhost:8000/metrics

2. prometheus config
    - `prometheus.yml` defines scrape jobs, e.g.:
      ```
      scrape_configs:
        - job_name: "prometheus"
          static_configs:
            - targets: ["localhost:9090"]

        - job_name: "delivery_service"
          static_configs:
            - targets: ["host.docker.internal:8000"]
      ```
    - on Windows/Docker Desktop use `host.docker.internal:8000` so containers can reach the host service.

3. alert rules
    - put rules in `alert_rules.yml` and reference in `prometheus.yml` via `rule_files: - /etc/prometheus/alert_rules.yml`
    - example rules:
      - `HighPendingDeliveries`: `pending_deliveries > 10` for `15s` → severity `warning`
      - `HighAverageDeliveryTime`: `(average_delivery_time_sum / average_delivery_time_count) > 30` → severity `critical`

4. run Prometheus (PowerShell friendly)
    - stop old:
      > docker stop prometheus; docker rm prometheus
    - run:
      > docker run -d --name prometheus -p 9090:9090 `
        -v "${PWD}\prometheus.yml:/etc/prometheus/prometheus.yml" `
        -v "${PWD}\alert_rules.yml:/etc/prometheus/alert_rules.yml" `
        prom/prometheus
    - confirm:
      > curl.exe http://localhost:9090/api/v1/targets

5. run Grafana (PowerShell friendly)
    - run:
      > docker run -d --name grafana -p 3000:3000 grafana/grafana
    - open UI: http://localhost:3000 (default admin/admin)
    - add Prometheus datasource URL: `http://host.docker.internal:9090`
    - create panels using PromQL (examples below).

6. networking notes (Windows)
    - inside a container: `localhost` refers to the container itself.
    - to reach the Windows host from a container use: `host.docker.internal`.
    - if you run Prometheus on the host (not in a container), `localhost:8000` works.
    - avoid `--network=host` on Docker Desktop/Windows; use `-p` mappings instead.

7. verifying scrapes & data
    - Prometheus Targets page: http://localhost:9090/targets (shows UP/DOWN, last scrape)
    - fetch raw metrics from the exporter:
      > curl.exe http://localhost:8000/metrics
    - query via Prometheus API:
      > curl.exe "http://localhost:9090/api/v1/query?query=pending_deliveries"
    - Prometheus UI (Graph) queries:
      - `pending_deliveries`
      - `total_deliveries`
      - `on_the_way_deliveries`
      - `average_delivery_time_sum`
      - `average_delivery_time_count`

8. PromQL examples
    - current pending deliveries:
      ```
      pending_deliveries
      ```
    - recent average delivery time (using Summary sum & count):
      ```
      rate(average_delivery_time_sum[1m]) / rate(average_delivery_time_count[1m])
      ```
      (gives per-second average over last 1m; multiply/divide time windows as needed)
    - average over last 5m:
      ```
      increase(average_delivery_time_sum[5m]) / increase(average_delivery_time_count[5m])
      ```

9. alert testing
    - temporarily make the exporter emit `pending_deliveries` > 10 (it already does in your simulation) to trigger `HighPendingDeliveries`.
    - check Alerts in Prometheus UI: http://localhost:9090/alerts
    - to send notifications, add Alertmanager and configure `alerting:` in `prometheus.yml` to point to Alertmanager.

10. optional improvements
    - containerize the Python exporter (runs inside Docker) so you avoid `host.docker.internal`.
    - add Alertmanager and configure receivers (Slack/email).
    - create a Grafana dashboard JSON for easy reuse.

## One-liner summary
Python exporter → Prometheus scrapes & stores metrics → Grafana queries Prometheus to visualize. On Windows Docker use `host.docker.internal` for container → host communication.
