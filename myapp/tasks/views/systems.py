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

  # get all the active users 
  def getAllUsers(self):
    return [
      user for user in User.objects.all().select_related("profile") 
      if user.profile.division == "الانظمة" and user.is_active
    ]

  # get all the tasks in the current month 
  def getAllTasks(self):
    return [
      task 
      for task in Task.objects.prefetch_related("employees")
      .filter(start_date__range=(self.getFirstDayOfMonth(), self.getLastDayOfMonth()))
      .order_by("-created_at") 
      if task.user.profile.division == "الانظمة" 
    ]

  # get the first day in a month
  def getFirstDayOfMonth(self) -> str:
    return str(datetime.date.today().replace(day=1))
  
  # get the last day in a month
  def getLastDayOfMonth(self) -> str:
    return str(datetime.date.today().replace(day=31))

  # check if the request
  def checkHTTPRequest(self, request) -> bool:
    return (request.META.get("HTTP_X_CSRFTOKEN") != request.POST.get("csrftoken") or 
    request.headers.get("X-Requested-With") != "XMLHttpRequest" or 
    not request.user.is_staff)
    
  # get the form data from ajax request
  def getFormData(self, request) -> str:
    subject     = request.POST.get("subject")
    start_date  = request.POST.get("start_date")
    end_date    = request.POST.get("end_date")
    employees   = request.POST.get("employees") 
    return subject, start_date, end_date, employees


  def post(self, request):
    if self.checkHTTPRequest(request):
      return JsonResponse({"errMsg": "Invalid request"})

    subject, start_date, end_date, employees = self.getFormData(request)
    print(subject, start_date, end_date, employees)
    return JsonResponse({"msg": "success"})

  