from django.urls import path
from .views import HomePageView
from .employees.views import get_all_employees, register_user
from .tasks.views.director import get_all_director_tasks, create_task_to_staff
from .tasks.views.systems import (
  get_all, create_task, receive_task, achieve_task, 
  confirm_task, delete_task, rate_task
)
from .notifications.views.notifications import get_all_notifications
from .auth import auth
from django.contrib.auth.decorators import login_required

urlpatterns = [
  path("", login_required(HomePageView.as_view())),
  path("accounts/login/", auth.loginUser),
  path("logout/", auth.logoutUser),
  path("employees/", login_required(get_all_employees)),
  path("employees/register/", login_required(register_user)),
  path("tasks/systems/", login_required(get_all)),
  path("tasks/systems/create/", login_required(create_task)),
  path("tasks/systems/receive/<int:id>", login_required(receive_task)),
  path("tasks/systems/achieve/<int:id>", login_required(achieve_task)),
  path("tasks/systems/confirm/<int:id>", login_required(confirm_task)),
  path("tasks/systems/delete/<int:id>", login_required(delete_task)),
  path("tasks/systems/rate/<int:id>", login_required(rate_task)),
  path("tasks/director/", login_required(get_all_director_tasks)),
  path("tasks/director/create/", login_required(create_task_to_staff)),
  path("notifications/", login_required(get_all_notifications))
]