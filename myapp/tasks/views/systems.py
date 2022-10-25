from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from myapp.models import Task

class SystemTasksView(View):
  template_name = "systems_tasks.html"
  
  def get(self, request):
    return render(request, self.template_name, 
    {
      "employees": self.getAllUsers(),
      "tasks": self.getAllTasks()
    }
    )

  def getAllUsers(self):
    return [user for user in User.objects.all().select_related("profile") if user.profile.division == "الانظمة" and user.is_active]

  def getAllTasks(self):
    return [task for task in Task.objects.prefetch_related("employees").all().order_by("-created_at") if task.user.profile.division == "الانظمة"]