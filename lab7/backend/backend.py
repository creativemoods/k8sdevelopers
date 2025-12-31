from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import time
import math
import random
import os

app = Flask(__name__)
CORS(app)

# App start time
start_time = time.time()

tasks = []

@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify({
        "firstname": os.getenv("FIRSTNAME", "World")
    })

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    task = request.json.get('task')
    if task:
        tasks.append({"task": task})
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
    app.run(host='0.0.0.0', debug=True)
