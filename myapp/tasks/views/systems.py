from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from myapp.models import Task
import datetime 

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
    return [
      task 
      for task in Task.objects.prefetch_related("employees")
      .filter(start_date__range=(self.getFirstDayOfMonth(), self.getLastDayOfMonth()))
      .order_by("-created_at") 
      if task.user.profile.division == "الانظمة" 
    ]

  def getFirstDayOfMonth(self):
    return str(datetime.date.today().replace(day=1))
  
  def getLastDayOfMonth(self):
    return str(datetime.date.today().replace(day=31))

  
  def post(self, request):
    if (request.META.get("HTTP_X_CSRFTOKEN") != request.POST.get("csrftoken")):
      return JsonResponse({"errMsg": "Invalid request"})
    print("You hit save button through your template")
    return JsonResponse({"msg": "success"})