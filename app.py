from flask import Flask, jsonify, render_template
from celery.result import AsyncResult
from tasks import process_task

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-task', methods=['POST'])
def start_task():
    task = process_task.apply_async()  # Envia a tarefa para o Celery
    return jsonify({'task_id': task.id}), 202

@app.route('/task-status/<task_id>')
def task_status(task_id):
    task_result = AsyncResult(task_id, backend=process_task.backend)
    if task_result.state == 'PENDING':
        response = {
            'state': task_result.state,
            'status': 'Pendente'
        }
    elif task_result.state != 'FAILURE':
        response = {
            'state': task_result.state,
            'status': task_result.info.get('status', ''),
            'task_id': task_result.info.get('task_id', ''),
        }
    else:
        response = {
            'state': task_result.state,
            'status': 'Erro',
        }
    return jsonify(response)
