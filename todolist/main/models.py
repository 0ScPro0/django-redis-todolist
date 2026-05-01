from typing import Dict, Optional
from dataclasses import dataclass
from enum import Enum

from .types import TaskStatus


@dataclass
class Task:
    id: int
    name: str
    description: str
    status: TaskStatus

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "status": self.status.value,  # Get value of enum var
        }

    @classmethod
    def from_dict(cls, task_id: int, data: Dict[str, str]) -> Optional["Task"]:
        """Create Task from Redis dictionary with validation"""
        try:
            return cls(
                id=task_id,
                name=data.get("name", ""),
                description=data.get("description", ""),
                status=TaskStatus(data.get("status", TaskStatus.NEW.value)),
            )
        except (ValueError, KeyError) as e:
            print(f"Ошибка валидации Task: {e}")
            return None


@dataclass
class TaskCreate:
    name: str
    description: str
    status: TaskStatus = TaskStatus.NEW


@dataclass
class TaskUpdate(Task):
    pass
