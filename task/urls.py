from django.urls import path
from task.views import systems

urlpatterns = [
  path("systems/", systems.SystemTasksView, name="systems_tasks_page")
]