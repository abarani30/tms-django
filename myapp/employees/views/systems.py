from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from myapp.models import Task

class SystemsEmployeesView(View):
  template_name = "systems_employees.html"

  def get(self, request):
    task = Task.objects.prefetch_related("employees")
    return render(request, self.template_name, 
      {
        "employees": self.getAllUsers(),
        "unreadable": task[0].unread_employee_tasks(request)
      }
    )

  def getAllUsers(self):
    return [user for user in User.objects.all().select_related("profile") if user.profile.division == "الانظمة" and user.is_active]