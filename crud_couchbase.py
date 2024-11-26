from couchbase_database import get_collection, get_cluster
from uuid import uuid4
from faker import Faker

fake = Faker()


def create_task(task_data):
    collection = get_collection()
    task_id = str(uuid4())
    task = {
        "id": task_id,
        "title": task_data.title,
        "description": task_data.description,
        "category_id": task_data.category_id,
        "completed": task_data.completed or False,  # Убедимся, что completed имеет значение
        "type": "task"
    }
    try:
        collection.insert(task_id, task)
        print(f"Task created with ID: {task_id}")
        return task
    except Exception as e:
        print(f"Error creating task: {e}")
        raise



def get_tasks_with_categories(skip=0, limit=10):
    cluster = get_cluster()
    query = '''
        SELECT t.id, t.title, t.description, t.completed, c.name AS category_name
        FROM `ToDo_backet` AS t
        LEFT JOIN `ToDo_backet` AS c ON t.category_id = c.id
        WHERE t.type = "task"
        ORDER BY t.id DESC  -- Сортировка по убыванию ID (новые задачи сверху)
        LIMIT $limit OFFSET $skip
    '''
    rows = cluster.query(query, limit=limit, skip=skip)
    return [row for row in rows]


def get_tasks_by_category(category_id, skip=0, limit=10):
    cluster = get_cluster()
    query = f'''
        SELECT t.id, t.title, t.description, t.completed, c.name AS category_name
        FROM `ToDo_backet` AS t
        LEFT JOIN `ToDo_backet` AS c ON t.category_id = c.id
        WHERE t.type = "task" AND t.category_id = "{category_id}"
        ORDER BY t.id
        LIMIT {limit} OFFSET {skip}
    '''
    return [row for row in cluster.query(query)]


def count_tasks(category_id=None):
    cluster = get_cluster()
    if category_id:
        query = f'SELECT COUNT(*) AS count FROM `ToDo_backet` WHERE type = "task" AND category_id = "{category_id}"'
    else:
        query = f'SELECT COUNT(*) AS count FROM `ToDo_backet` WHERE type = "task"'
    result = cluster.query(query)
    for row in result:
        return row["count"]
    return 0


def get_categories():
    cluster = get_cluster()
    query = f'SELECT META().id, name FROM `ToDo_backet` WHERE type = "category"'
    return [row for row in cluster.query(query)]


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


def get_task(task_id):
    collection = get_collection()
    try:
        result = collection.get(task_id)
        return result.content_as[dict]
    except Exception:
        return None

def seed_data():
    collection = get_collection()

    # Создание категорий
    category_ids = []
    for _ in range(10):  # Генерируем 10 категорий
        category_id = str(uuid4())
        category = {
            "id": category_id,
            "name": fake.word(),
            "type": "category"
        }
        try:
            collection.insert(category_id, category)
            category_ids.append(category_id)  # Сохраняем ID категории
        except Exception as e:
            print(f"Error creating category: {e}")

    print(f"Создано категорий: {len(category_ids)}")

    # Создание задач
    for _ in range(100):  # Генерируем 100 задач
        task_id = str(uuid4())
        category_id = fake.random_element(category_ids)  # Выбираем случайную категорию
        task = {
            "id": task_id,
            "title": fake.sentence(nb_words=5),
            "description": fake.text(max_nb_chars=200),
            "completed": fake.boolean(),
            "category_id": category_id,
            "type": "task"
        }
        try:
            collection.insert(task_id, task)
        except Exception as e:
            print(f"Error creating task: {e}")

    print("Создано задач: 100")

def mark_task_completed(task_id):
    collection = get_collection()
    try:
        task = get_task(task_id)
        if task is None:
            return None
        task["completed"] = True  # Обновляем статус на "completed"
        collection.replace(task_id, task)
        print(f"Task {task_id} marked as completed.")
        return task
    except Exception as e:
        print(f"Error marking task as completed: {e}")
        return None

