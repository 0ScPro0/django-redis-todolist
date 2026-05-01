from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from .repository import task_repository
from .models import TaskCreate, TaskUpdate, TaskStatus
from .repository import task_repository


def index(request):
    """Main page"""
    # Get task list
    tasks = task_repository.list_tasks()

    # We pass them to the context under the name 'tasks', as the template expects
    return render(request, "main/index.html", {"tasks": tasks})


def create_task(request: HttpRequest):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        status_str = request.POST.get("status", "new")

        # Converting a string from a form to an Enum
        try:
            status = TaskStatus(status_str)
        except ValueError:
            status = TaskStatus.NEW

        # Create TaskCreate odject
        task_data = TaskCreate(name=name, description=description, status=status)

        # Save
        task_repository.create_task(task_data)

        return redirect("index")

    return render(request, "main/create.html")


def update_task(request: HttpRequest, task_id):
    """Update task"""
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        status_str = request.POST.get("status", "new")

        # Converting a string from a form to an Enum
        try:
            status = TaskStatus(status_str)
        except ValueError:
            status = TaskStatus.NEW

        # Create TaskUpdate odject
        task_data = TaskUpdate(
            id=task_id, name=name, description=description, status=status
        )

        # Save
        task_repository.update_task(task_data)

        return redirect("index")

    # GET request - show form with current task data
    current_task = task_repository.get_task(task_id)

    return render(
        request,
        "main/update.html",
        {
            "task": current_task,
            "task_id": task_id,
        },
    )


def delete_task(request, task_id):
    """Удаление задачи"""
    if request.method == "POST":
        task_repository.delete_task(task_id)
    return redirect("index")
