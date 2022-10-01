from django.urls import path
from .views import HomePageView
from .employees.views.systems import get_all_employees, register_user
from .employees.views.maintenance import MaintenanceEmployeesView
from .tasks.views.director import DirectorTasksView
from .tasks.views.systems import (
  get_all, create_task, receive_task, achieve_task, confirm_task, delete_task, rate_task
)
from .notifications.views.notifications import get_all_notifications
from .auth import auth
from django.contrib.auth.decorators import login_required

urlpatterns = [
  path("", login_required(HomePageView.as_view()), name="home_page"),
  path("accounts/login/", auth.loginUser, name="login_page"),
  path("logout/", auth.logoutUser, name="logout_user"),
  path("employees/systems/", login_required(get_all_employees)),
  path("employees/systems/register/", login_required(register_user)),
  path("employees/maintenance/", login_required(MaintenanceEmployeesView.as_view()), name="maintenance_employees_page" ),
  path("tasks/systems/", login_required(get_all), name="systems_tasks_page"),
  path("tasks/systems/create/", login_required(create_task)),
  path("tasks/systems/receive/<int:id>", login_required(receive_task)),
  path("tasks/systems/achieve/<int:id>", login_required(achieve_task)),
  path("tasks/systems/confirm/<int:id>", login_required(confirm_task)),
  path("tasks/systems/delete/<int:id>", login_required(delete_task)),
  path("tasks/systems/rate/<int:id>", login_required(rate_task)),
  path("tasks/director/", DirectorTasksView, name="director_tasks_page"),
  path("notifications/", login_required(get_all_notifications), name="notifications_page")
]