from enum import Enum


class TaskStatus(Enum):
    """
    Task Status
    - new
    - pending
    - completed
    """

    NEW = "new"
    PENDING = "pending"
    COMPLETED = "completed"
