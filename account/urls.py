from django.urls import path
from account.views import home, systems

urlpatterns = [
  path("", home.index, name="home_page"),
  path("employees/systems/", systems.SystemsEmployeesView, name="systems_employees")
]