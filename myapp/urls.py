from django.urls import path
from .views import HomePageView
from .employees.views.systems import SystemsEmployeesView
from .employees.views.maintenance import MaintenanceEmployeesView
from .tasks.views.director import DirectorTasksView
from .tasks.views.systems import SystemTasksView
from .notifications.views.notifications import NotificationsView
from .auth import auth
from django.contrib.auth.decorators import login_required

urlpatterns = [
  path("", login_required(HomePageView.as_view()), name="home_page"),
  path("accounts/login/", auth.loginUser, name="login_page"),
  path("logout/", auth.logoutUser, name="logout_user"),
  path("employees/systems/", login_required(SystemsEmployeesView.as_view()), name="systems_employees_page"),
  path("employees/maintenance/", login_required(MaintenanceEmployeesView.as_view()), name="maintenance_employees_page" ),
  path("tasks/systems/", login_required(SystemTasksView.as_view()), name="systems_tasks_page"),
  path("tasks/director/", DirectorTasksView, name="director_tasks_page"),
  path("notifications/", NotificationsView, name="notifications_page")
]