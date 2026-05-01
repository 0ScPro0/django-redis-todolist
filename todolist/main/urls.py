from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),  # Главная страница
    path("create/", views.create_task, name="task_create"),
    path("update/<int:task_id>/", views.update_task, name="task_update"),
    path("delete/<int:task_id>/", views.delete_task, name="task_delete"),
]
