from celery_config import celery
import time
import uuid

@celery.task(bind=True)
def process_task(self):
    task_id = uuid.uuid4()  # Gera um UUID para a task
    self.update_state(state='PROGRESS', meta={'status': 'Iniciando', 'task_id': task_id})
    
    for i in range(5):
        time.sleep(2)  # Simula processamento
        self.update_state(state='PROGRESS', meta={'status': f'Progresso {i + 1}/5', 'task_id': task_id})
    
    return {'status': 'Finalizado', 'task_id': task_id, 'result': 'Tarefa concluída!'}
