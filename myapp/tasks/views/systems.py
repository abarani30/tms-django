from re import T, U
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from myapp.models import Task
from typing import Dict, List
from redmail import outlook
import datetime, uuid
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template.response import SimpleTemplateResponse

# get request
def get_all(request) -> SimpleTemplateResponse:
  tasks = get_all_tasks()
  try:
    if tasks:
      return render(request, "systems_tasks.html", context = get_context(request, tasks))
  except Exception as e:
    return Http404(e.message)



# get the context dictionary
def get_context(request, tasks):
  return {
    "employees": get_all_users(),
    "tasks": tasks,
    "unreadable": tasks[0].unread_employee_tasks(request)
  }



# create new task
def create_task(request) -> HttpResponseRedirect:
  if request.method != "POST":
    return HttpResponseRedirect("/tasks/systems/")
  
  if not validate_data(request):
    messages.error(request, "ﻻ ﻳﻤﻜﻦ ﺗﻨﻔﻴﺬ ﻫﺬا اﻟﻄﻠﺐ")
  else: 
    assign_task(request, add_task(request))
    send_email(request)
    messages.success(request, "تم تخصيص المهمة بنجاح")

  return HttpResponseRedirect('/tasks/systems/')



# receive the task 
def receive_task(request, id) -> HttpResponseRedirect:
  if id and get_task(id) and not request.user.is_staff:
    update_received_field(get_task(id)[0])
    messages.success(request, f"{id} ﺗﻢ استلام اﻟﻤﻬﻤﺔ المرقمه")
  return HttpResponseRedirect('/tasks/systems/')
  
  

# achieve the task (task completion) 
def achieve_task(request, id) -> HttpResponseRedirect:
  if id and get_task(id) and not request.user.is_staff:
    update_status_field(request, get_task(id)[0])
    messages.success(request, f"{id} ﺗﻢ تحديث حالة اﻟﻤﻬﻤﺔ المرقمه")
  return HttpResponseRedirect('/tasks/systems/')



# confirm the task 
def confirm_task(request, id) -> HttpResponseRedirect:
  if id and get_task(id) and request.user.is_staff:
    update_status_field(request, get_task(id)[0])
    messages.success(request, f"{id} ﺗﻢ التأكيد على انجاز اﻟﻤﻬﻤﺔ المرقمه")
  return HttpResponseRedirect('/tasks/systems/')



# update the current task received
def update_received_field(task):
  task.received = True
  task.save()



# update the current task status
def update_status_field(request, task) -> bool:
  task.status = "منجزة" if request.user.is_staff else "بأنتظار الموافقة"
  task.save()
  return True



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



# get all the employee tasks 
def get_employee_tasks(request) -> List[dict]:
  return [
    task for task in get_current_month()[0]
    if request.user in task.employees.all() and 
    not task.received and task.active
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
def validate_data(request) -> bool:
   return bool(
    is_not_empty(request) and 
    compare_dates(request) and 
    len(is_employee(request.POST.getlist("employees"))) == 
    len(request.POST.getlist("employees"))
  )



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



# convert date from "m/d/Y" to "Y-m-d"
def convert_date(current_date):
  return datetime.datetime.strptime(current_date, "%m/%d/%Y").strftime("%Y-%m-%d")



# get the day from the current date
def get_day(current_date) -> str:
  year, month, day = (int(x) for x in current_date.split('-'))    
  return convert_day_name((datetime.date(year, month, day)).strftime("%A"))



# used to convert the day name from english to arabic
def convert_day_name(day) -> str:
  week: Dict[str] = {
    "Sunday": "اﻻﺣﺪ", "Monday": "اﻻﺛﻨﻴﻦ", "Tuesday": "اﻟﺜﻼﺛﺎء",
    "Wednesday": "اﻻﺭﺑﻌﺎء", "Thursday": "اﻟﺨﻤﻴﺲ", "Friday": "اﻟﺠﻤﻌﻪ", 
    "Saturday": "اﻟﺴﺒﺖ"
  }
  return week[day]



# used to check if the username exists or not
def is_employee(employees) -> List[dict]:
  return [
    User.objects.get(username=employee) for employee in employees
    if User.objects.filter(username=employee).exists()
  ]



# to create and save a new task
def add_task(request) -> List[dict]:
  return Task.objects.create(
    user        = request.user , 
    subject     = request.POST.get("task-subject"),
    start_date  = convert_date(request.POST.get("start-date")), 
    end_date    = convert_date(request.POST.get("end-date")),
    start_day   = get_day(convert_date(request.POST.get("start-date"))), 
    end_day     = get_day(convert_date(request.POST.get("end-date"))),
    no_of_users = len(request.POST.getlist("employees"))
  )



# assign the new task to each employee
def assign_task(request, task):
  for employee in is_employee(request.POST.getlist("employees")):
    task.employees.add(employee)



# send an email to each employee 
def send_email(request):
  for employee in is_employee(request.POST.getlist("employees")):
    outlook.username = request.user.email
    outlook.password = "prestige1"
    outlook.send(
      receivers=[employee.email],
      subject=f'{request.POST.get("task-subject")} {uuid.uuid4()}',
      html=f'<b>{request.POST.get("task-subject")}</b><br>يرجى النقر على <b>استلمت</b> في حال تم استلامك لهذه المهمه',
    )



# get the current task by id
def get_task(id):
  return Task.objects.filter(pk=id).prefetch_related("employees")