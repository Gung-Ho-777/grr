from grafanalib.core import Dashboard, Graph, Row, Target
from grr_grafanalib_dashboards.util import add_data_source
from grr_grafanalib_dashboards.reusable_panels import GENERAL_PANELS
from grr_grafanalib_dashboards.config import GRAFANA_DATA_SOURCE

GRR_COMPONENT = "frontend"

dashboard = Dashboard(
  title="{}s Dashboard".format(GRR_COMPONENT).title(),
  rows=[
    Row(panels=[panel(GRR_COMPONENT) for panel in row]) 
    for row in GENERAL_PANELS
    ] +
    [
      Row(panels=[
      Graph(
        title="QPS",
        targets=[
          Target(
            expr='sum(rate(frontend_request_count_total[1m]))',
            legendFormat="Requests",
          ),
        ],
      ),
      Graph(
        title="Request Latency Rate",
        targets=[
          Target(
            expr='sum(rate(frontend_request_latency_sum[10m])) / sum(rate(frontend_request_latency_count[10m]))',
            legendFormat="Latency",
          ),
        ],
      ),
      Graph(
        title="Well Known Flows Requests Rate",
        targets=[
          Target(
            expr='rate(well_known_flow_requests_total[10m])',
            legendFormat="Flow: {{flow}}",
          ),
        ],
      ),
      Graph(
        title="GRR Client Crashes",
        targets=[
          Target(
            expr='sum(rate(grr_client_crashes_total{job="grr_frontend"}[10m]))',
            legendFormat="Rate of Client crashes",
          ),
        ],
      )
    ]
    ),
  ]
).auto_panel_ids()

dashboard = add_data_source(dashboard, GRAFANA_DATA_SOURCE)
