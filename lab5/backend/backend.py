from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
