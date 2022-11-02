from re import T, U
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from myapp.models import Task
from typing import Dict, List
from redmail import outlook
import datetime, uuid
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import SimpleTemplateResponse
from django.contrib.auth.decorators import user_passes_test


# check if the user is in the same group
def check_group(user) -> bool:
  return bool(user.groups.filter(name="Systems").exists())



# get request
@user_passes_test(lambda user: check_group(user) or user.is_superuser)
def get_all(request) -> HttpResponse:
  if get_all_tasks() != []:
    return render(request, "systems_tasks.html", context = get_context(request, get_all_tasks()))
  return render(request, "systems_tasks.html", context = default_context())



# get the context dictionary
def get_context(request, tasks):
  return {
    "employees": get_all_users(),
    "tasks": tasks,
    "unreadable": tasks[0].unread_employee_tasks(request)
  }



# in case when there is no tasks to return
def default_context():
  return {
    "employees": get_all_users(),
    "tasks": "[]",
    "unreadable": 0
  }



# create new task
@user_passes_test(lambda user: check_group(user))
def create_task(request) -> HttpResponseRedirect:
  if request.method != "POST":
    return HttpResponseRedirect("/tasks/systems/")
  
  if not validate_data(request):
    messages.error(request, "البيانات التي ارسلتها غير صحيحه")
  else: 
    assign_task(request, add_task(request))
    send_email(request)
    messages.success(request, "تم تخصيص المهمة بنجاح")

  return HttpResponseRedirect('/tasks/systems/')



# receive the task 
@user_passes_test(lambda user: check_division(user))
def receive_task(request, id) -> HttpResponseRedirect:
  if id and get_task(id) and not request.user.is_staff:
    update_received_field(get_task(id)[0])
    messages.success(request, f"{id} ﺗﻢ استلام اﻟﻤﻬﻤﺔ المرقمه")
  return HttpResponseRedirect('/tasks/systems/')
  
  

# achieve the task (task completion) 
@user_passes_test(lambda user: check_division(user))
def achieve_task(request, id) -> HttpResponseRedirect:
  if id and get_task(id) and not request.user.is_staff:
    update_status_field(request, get_task(id)[0])
    messages.success(request, f"{id} ﺗﻢ انجاز اﻟﻤﻬﻤﺔ المرقمه")
  return HttpResponseRedirect('/tasks/systems/')



# confirm the task 
@user_passes_test(lambda user: check_division(user))
def confirm_task(request, id) -> HttpResponseRedirect:
  if id and get_task(id) and request.user.is_staff:
    update_status_field(request, get_task(id)[0])
    messages.success(request, f"{id} ﺗﻢ التأكيد على انجاز اﻟﻤﻬﻤﺔ المرقمه")
  return HttpResponseRedirect('/tasks/systems/')



# delete the task 
@user_passes_test(lambda user: check_division(user))
def delete_task(request, id) -> HttpResponseRedirect:
  if id and get_task(id) and request.user.is_staff:
    decactivate_task(get_task(id)[0])
    messages.success(request, f"{id} ﺗﻢ حذف اﻟﻤﻬﻤﺔ المرقمه")
  return HttpResponseRedirect('/tasks/systems/')



# assign a rate to the task 
@user_passes_test(lambda user: check_division(user))
def rate_task(request, id) -> HttpResponseRedirect:
  if request.method == "POST" and id and get_task(id) and request.user.is_staff:
    rate(get_task(id)[0], request.POST.get("task-rate"))
    messages.success(request, f"{id} ﺗﻢ تقييم اﻟﻤﻬﻤﺔ المرقمه")
  return HttpResponseRedirect('/tasks/systems/')



# update the current task received
def update_received_field(task):
  if not task.received:
    task.received = True
    task.save()



# update the current task status
def update_status_field(request, task) -> bool:
  task.status = "منجزة" if request.user.is_staff else "بأنتظار الموافقة"
  task.save()
  return True



# deactivate the current task
def decactivate_task(task):
  if task.active:
    task.active = False
    task.save()



# update the current rate field
def rate(task, rate_value):
  if task.rate == 0 and task.status == "منجزة":
    task.rate = rate_value
    task.save()



# get all the active users in the same group 
def get_all_users() -> List[dict]:
  return [
    user for user in User.objects.all().select_related("profile") 
    if check_group(user) and user.is_active
  ]



# get all the tasks in the current month 
def get_all_tasks() -> List[dict]:
  return [
    task for task in get_month_tasks()[0]
    if task.user.groups.filter(name="Systems").exists() and task.active
  ]



# get all the employee tasks 
def get_employee_tasks(request) -> List[dict]:
  return [
    task for task in get_month_tasks()[0]
    if request.user in task.employees.all() and 
    not task.received and task.active
  ]



# get the current month tasks
def get_month_tasks() -> List[dict]:
  return [Task.objects.prefetch_related("employees")
    .filter(start_date__range = (get_first_day(), get_last_day()))
    .order_by("-created_at")]



# get the month
def get_month() -> int:
  return datetime.datetime.now().month



# get the year
def get_year() -> int:
  return datetime.datetime.now().year



# get the first day in a month
def get_first_day() -> str:
  return str(datetime.datetime(get_year(), get_month(), 1).date())



# get the last day in a month
def get_last_day() -> str:
  if get_month() == 12:
    return str(datetime.datetime(get_year(), get_month(), 31).date())
  return str((datetime.datetime(get_year(), get_month() + 1, 1) + datetime.timedelta(days=-1)).date())



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
  return request.POST.get("start-date") <= request.POST.get("end-date")



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