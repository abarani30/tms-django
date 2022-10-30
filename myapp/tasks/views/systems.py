from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from myapp.models import Task, Notification
from typing import Dict, List
from redmail import outlook
import datetime, ast, uuid
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template.response import SimpleTemplateResponse

# get request
def get_all(request) -> SimpleTemplateResponse:
  notification  = Notification.objects.prefetch_related("emps")
  return render(request, "systems_tasks.html", 
    {
      "employees": get_all_users(),
      "tasks": get_all_tasks(),
      "unreadable": notification[0].countUnreadableNotifications(request)
    }
  )

# create new task
def create_task(request) -> HttpResponseRedirect:
  if request.method != "POST":
    return HttpResponseRedirect("/tasks/systems/")

  if not validate_form_data(request):
    messages.error(request, "لا يمكن تنفيذ هذا الطلب")
  else:
    print("yes")
  return HttpResponseRedirect('/tasks/systems/')

# update the task 
def update_task(request, id) -> HttpResponseRedirect:
  if id: messages.success(request, f"{id} تم تحديث المهمة بألرقم")
  return HttpResponseRedirect('/tasks/systems/')


# get all the active users 
def get_all_users() -> List[dict]:
  return [
    user for user in User.objects.all().select_related("profile") 
    if user.profile.division == "الانظمة" and user.is_active
  ]

# get all the tasks in the current month 
def get_all_tasks() -> List[dict]:
  return [
    task for task in get_current_month()[0]
    if task.user.profile.division == "الانظمة" and task.active
  ]

# get the current month tasks
def get_current_month() -> List[dict]:
  return [Task.objects.prefetch_related("employees")
    .filter(start_date__range = (get_first_day(), get_last_day()))
    .order_by("-created_at")]

# get the first day in a month
def get_first_day() -> str:
  return str(datetime.date.today().replace(day=1))

# get the last day in a month
def get_last_day() -> str:
  return str(datetime.date.today().replace(day=31))

# validate the form data
def validate_form_data(request) -> bool:
   return bool(is_not_empty(request) and compare_dates(request))

# checks if the form data is empty or not
def is_not_empty(request) -> bool:
  return bool(
    request.POST.get("task-subject") and 
    request.POST.get("start-date") and 
    request.POST.get("end-date") and 
    len(request.POST.getlist("employees")) != 0
  )

# compare both the start_date and end_date
def compare_dates(request) -> bool:
  return request.POST.get("start-date") < request.POST.get("end-date")