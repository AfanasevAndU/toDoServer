from couchbase_database import get_collection
from couchbase_database import get_cluster
from uuid import uuid4

def create_task(task_data):
    collection = get_collection()
    task_id = str(uuid4())  
    task = {
        "id": task_id,
        "title": task_data.title,
        "description": task_data.description,
        "completed": task_data.completed
    }
    collection.insert(task_id, task)
    return task

def get_task(task_id):
    collection = get_collection()
    try:
        result = collection.get(task_id)
        return result.content_as[dict]
    except Exception:
        return None

def get_tasks(skip=0, limit=10):
    cluster = get_cluster()  # Получаем объект Cluster
    query = f'SELECT META().id, title, description, completed FROM `ToDo_backet` ORDER BY META().id LIMIT {limit} OFFSET {skip}'
    result = cluster.query(query)
    return [row for row in result]



def delete_task(task_id):
    collection = get_collection()
    try:
        result = get_task(task_id)
        if result is None:
            return None  
        collection.remove(task_id)
        return result
    except Exception as e:
        print(f"Error deleting task: {e}")
        return None
