from prometheus_client import Counter, Histogram
import time
from flask import request

REQUEST_COUNT = Counter(
    'flask_http_request_total',
    'Total HTTP Requests',
    ['method', 'endpoint']
)

REQUEST_LATENCY = Histogram(
    'flask_http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)


ERROR_COUNT = Counter(
    'flask_http_errors_total',
    'Total HTTP errors',
    ['method', 'endpoint', 'status_code']
)

def setup_metrics(app):
    @app.before_request
    def start_timer():
        request.start_time = time.time()

    @app.after_request
    def record_metrics(response):
        request_latency = time.time() - request.start_time
        endpoint = request.endpoint or "unknown"
        method = request.method

        REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(request_latency)

        if response.status_code >= 400:
            ERROR_COUNT.labels(method=method, endpoint=endpoint, status_code=response.status_code).inc()

        return response
