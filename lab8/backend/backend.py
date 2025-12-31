from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import time
import math
import random
import os

# Config for instrumentation
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.trace import Status, StatusCode

# Set up the tracer provider and exporter
resource = Resource(attributes={
    "service.name": "backendx"
})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer_provider = trace.get_tracer_provider()

otlp_exporter = OTLPSpanExporter(endpoint=os.environ["OTEL_ENDPOINT"], insecure=True)
tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
# /Config for instrumentation

app = Flask(__name__)
CORS(app)
# Instrumentation
FlaskInstrumentor().instrument_app(app)
tracer = trace.get_tracer(__name__)

# App start time
start_time = time.time()

tasks = []

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    task = request.json.get('task')
    if task:
        with tracer.start_as_current_span("validate-task") as span:
            time.sleep(random.uniform(0.05, 0.2))  # Simulated validation delay
            if len(task) < 3:
                span.set_status(Status(StatusCode.ERROR, "Simulated failure"))
                return jsonify({"error": "Task too short"}), 400

        with tracer.start_as_current_span("generate-task-id") as span:
            task_id = random.randint(1000, 9999)
            span.set_attribute("task.id", task_id)
            time.sleep(0.2)

        with tracer.start_as_current_span("enrich-task") as span:
            # Simulate enrichment logic
            time.sleep(0.15)
            enriched = f"{request.json.get('task')} [enriched]"
            span.set_attribute("task.content", enriched)

        with tracer.start_as_current_span("save-task"):
            time.sleep(random.uniform(0.1, 0.4))  # Simulated DB or storage delay
            tasks.append({"task": enriched})

        return jsonify({"message": "Task added successfully!"}), 201
    return jsonify({"error": "No task provided"}), 400

@app.route('/api/tasks', methods=['DELETE'])
def delete_task():
    task = request.json.get('task')
#    print(task);
    tasks[:] = [t for t in tasks if t['task'] != task]
    return jsonify({"message": "Task deleted successfully!"})

# Health probes
@app.route('/api/health', methods=['GET'])
def health():
    return '', 200

@app.route('/api/ready', methods=['GET'])
def readiness_probe():
    elapsed = time.time() - start_time
    if elapsed < 20:
        return jsonify({"status": "not ready ("+str(elapsed)+")"}), 404
    return jsonify({"status": "ready"}), 200

@app.route('/api/metrics', methods=['GET'])
def prometheus_metrics():
    current_time = time.time()

    # Use the timestamp as the x input for sine
    t = int(current_time // 15)
    x = t / 10.0
    base = math.sin(x) * 50 + 50  # Sine wave between 0 and 100
    noise = random.uniform(-5, 5)
    value = round(base + noise, 2)

    # Prometheus expects timestamps in **milliseconds**
    timestamp_ms = t * 15000

    metric_lines = [
        '# HELP studentx_sine_metric A smooth sine-wave metric with noise',
        '# TYPE studentx_sine_metric gauge',
        f'studentx_sine_metric {value} {timestamp_ms}'
    ]

    return Response('\n'.join(metric_lines) + '\n', mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
