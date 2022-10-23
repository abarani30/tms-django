from django.urls import path
from .views import index
from .employees.views.systems import SystemsEmployeesView
from .employees.views.maintenance import MaintenanceEmployeesView
from .tasks.views.director import DirectorTasksView
from .tasks.views.systems import SystemTasksView
from .notifications.views.notifications import NotificationsView

urlpatterns = [
  path("", index, name="home_page"),
  path("employees/systems/", SystemsEmployeesView, name="systems_employees_page"),
  path("employees/maintenance/", MaintenanceEmployeesView, name="maintenance_employees_page" ),
  path("tasks/systems/", SystemTasksView, name="systems_tasks_page"),
  path("tasks/director/", DirectorTasksView, name="director_tasks_page"),
  path("notifications/", NotificationsView, name="notifications_page")
]