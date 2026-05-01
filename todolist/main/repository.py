from typing import Optional, List

from .models import Task, TaskCreate, TaskUpdate
from .redis import RedisClient, redis_client


class TaskRepository:
    def __init__(self, redis: RedisClient, model):
        self.redis = redis
        self.model = model

    def create_task(self, task_create: TaskCreate) -> Optional[Task]:
        """Create new task with auto generate ID"""
        # Generating new ID
        task_id = self.redis.get_next_task_id()

        # Create Task
        task = Task(
            id=task_id,
            name=task_create.name,
            description=task_create.description,
            status=task_create.status,
        )

        # Save in Redis as hash
        response = self.redis.hset(
            f"task_{task_id}",
            mapping=task.to_dict(),
        )

        if not response:
            return None

        return task

    def update_task(self, task: Task) -> Optional[Task]:
        """Update task"""
        response = self.redis.hset(f"task_{task.id}", mapping=task.to_dict())

        if not response:
            return None

        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get task by ID"""
        response = self.redis.hgetall(f"task_{task_id}")

        if not response:
            return None

        return Task.from_dict(task_id, response)

    def delete_task(self, task_id: int) -> bool:
        """Delete task"""
        return bool(self.redis.delete(f"task_{task_id}"))

    def list_tasks(self) -> list[Task]:
        """Возвращает все задачи"""
        keys: List[str] = self.redis.keys("task_*")  # type: ignore[assignment]
        tasks = []

        for key in keys:
            # Extracting the ID from the key
            task_id = int(key.split("_")[1])

            task = self.get_task(task_id)
            if task:
                tasks.append(task)

        return tasks


task_repository = TaskRepository(redis_client, Task)
