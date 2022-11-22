import datetime
import uuid
from typing import Dict, List
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from redmail import outlook
from myapp.models import Task, Notification


# get request
@require_http_methods(['GET'])
def get_all(request) -> HttpResponse:
    if len(get_all_tasks(request)) != 0:
        return render(request, "tasks.html", context=get_context(request, get_all_tasks(request)))
    return render(request, "tasks.html", context=default_context(request))



# get the context dictionary
def get_context(request, tasks: List[Dict]) -> Dict:
    return {
        "employees": get_all_users(request),
        "tasks": tasks,
        "unreadable": tasks[0].unread_employee_tasks(request)
    }



# in case when there is no tasks to return
def default_context(request) -> Dict:
    return {
        "employees": get_all_users(request),
        "tasks": "[]",
        "unreadable": 0
    }



# create new task
@require_http_methods(['POST'])
@user_passes_test(lambda user: user.is_staff)
def create_task(request) -> HttpResponseRedirect:
    if request.method != "POST":
        return HttpResponseRedirect("/tasks/")

    if not validate_data(request):
        messages.error(request, "البيانات التي ارسلتها غير صحيحه")
    else:
        assign_task(request, add_task(request))
        send_email(request)
        messages.success(request, "تم تخصيص المهمة بنجاح")

    return HttpResponseRedirect('/tasks/')



# receive the task
@user_passes_test(lambda user: not user.is_staff)
def receive_task(request, id: int) -> HttpResponseRedirect:
    if len(get_task(id)) != 0 and user_in_task(request, id):
        update_received_field(get_task(id)[0])
        messages.success(request, f"{id} ﺗﻢ استلام اﻟﻤﻬﻤﺔ المرقمه")
    return HttpResponseRedirect('/tasks/')



# achieve the task (task completion) 
@user_passes_test(lambda user: not user.is_staff)
def achieve_task(request, id: int) -> HttpResponseRedirect:
    if len(get_task(id)) != 0 and user_in_task(request, id):
        update_status_field(request, get_task(id)[0])
        messages.success(request, f"{id} ﺗﻢ انجاز اﻟﻤﻬﻤﺔ المرقمه")
    return HttpResponseRedirect('/tasks/')



# confirm the task
@user_passes_test(lambda user: user.is_staff)
def confirm_task(request, id: int) -> HttpResponseRedirect:
    if len(get_task(id)) != 0 and is_task_owner(request, id):
        update_status_field(request, get_task(id)[0])
        messages.success(request, f"{id} ﺗﻢ التأكيد على انجاز اﻟﻤﻬﻤﺔ المرقمه")
    return HttpResponseRedirect('/tasks/')



# delete the task
@user_passes_test(lambda user: user.is_staff)
def delete_task(request, id: int) -> HttpResponseRedirect:
    if len(get_task(id)) != 0 and is_task_owner(request, id):
        deactivate_task(get_task(id)[0])
        messages.success(request, f"{id} ﺗﻢ حذف اﻟﻤﻬﻤﺔ المرقمه")
    return HttpResponseRedirect('/tasks/')



# update the current task received
def update_received_field(task: Dict):
    if not task.received:
        task.received = True
        task.save()
        return True
    return False



# update the current task status
def update_status_field(request, task: Dict) -> bool:
    task.status = "منجزة" if request.user.is_staff else "بأنتظار الموافقة"
    task.save()
    return True



# deactivate the current task
def deactivate_task(task: Dict) -> bool:
    if task.active:
        task.active = False
        task.save()
        return True
    return False


# get all the active users in the same group
def get_all_users(request) -> List[dict]:
    if request.user.is_superuser:
        return User.objects.select_related("profile")
    return list(Group.objects.filter(name=request.user.groups.all()[0]))[0].user_set.all()



# get all the tasks in the current month
def get_all_tasks(request) -> List[dict]:
    if request.user.is_superuser:
        return Task.objects.prefetch_related("employees").order_by("-created_at")
    return [
        task for task in get_month_tasks()[0]
        if task.user.groups.filter(name=request.user.groups.all()[0]).exists() and task.active
    ]



# get all the employee's tasks
def get_employee_tasks(request) -> List[dict]:
    return [
        task for task in get_month_tasks()[0]
        if request.user in task.employees.all() and
           not task.received and task.active
    ]



# get the current month tasks
def get_month_tasks() -> List[dict]:
    return [Task.objects.prefetch_related("employees")
                .filter(start_date__range=(get_first_day(), get_last_day()))
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
        len(get_employees(request)) ==
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
def convert_date(current_date: str):
    return datetime.datetime.strptime(current_date, "%m/%d/%Y").strftime("%Y-%m-%d")



# get the day from the current date
def get_day(current_date: str) -> str:
    year, month, day = (int(x) for x in current_date.split('-'))
    return convert_day_name((datetime.date(year, month, day)).strftime("%A"))



# used to convert the day name from english to arabic
def convert_day_name(day: str) -> str:
    week: Dict[str] = {
        "Sunday": "اﻻﺣﺪ", "Monday": "اﻻﺛﻨﻴﻦ", "Tuesday": "اﻟﺜﻼﺛﺎء",
        "Wednesday": "اﻻﺭﺑﻌﺎء", "Thursday": "اﻟﺨﻤﻴﺲ", "Friday": "اﻟﺠﻤﻌﻪ",
        "Saturday": "اﻟﺴﺒﺖ"
    }
    return week[day]



# used to check if the username exists or not
def get_employees(request) -> List[dict]:
    return [
        User.objects.get(username=employee) for employee in request.POST.getlist("employees")
        if employee in admin_group(request)
    ]



# check if the employee (user) is in the admin (staff) group
def admin_group(request) -> List[str]:
    return [user.username for user in request.user.groups.all()[0].user_set.all()]



# to create and save a new task
def add_task(request) -> List[dict]:
    return Task.objects.create(
        user=request.user,
        subject=request.POST.get("task-subject"),
        start_date=convert_date(request.POST.get("start-date")),
        end_date=convert_date(request.POST.get("end-date")),
        start_day=get_day(convert_date(request.POST.get("start-date"))),
        end_day=get_day(convert_date(request.POST.get("end-date"))),
        no_of_users=len(request.POST.getlist("employees"))
    )



# assign the new task to each employee
def assign_task(request, task: Dict):
    for employee in get_employees(request):
        task.employees.add(employee)



# send an email to each employee
def send_email(request):
    for employee in get_employees(request):
        outlook.username = request.user.email
        outlook.password = "prestige1"
        outlook.send(
            receivers=[employee.email],
            subject=f'{request.POST.get("task-subject")} {uuid.uuid4()}',
            html=f'<b>{request.POST.get("task-subject")}</b><br>يرجى النقر على <b>استلمت</b> في حال تم استلامك لهذه المهمه',
        )



# get the current task by id
def get_task(id: int) -> List[dict]:
    return Task.objects.filter(pk=id).prefetch_related("employees")


# check if the admin is the owner of the task
def is_task_owner(request, id: int) -> bool:
    return request.user == get_task(id)[0].user



# check if the user in the task employees
def user_in_task(request, id: int) -> bool:
    return request.user in get_task(id)[0].employees.all()



# get request
@user_passes_test(lambda user: user.is_superuser)
def get_all_director_tasks(request) -> HttpResponse:
  if len(get_all_notifications()) != 0:
    return render(request, "director_tasks.html", context = get_director_context(request, get_all_tasks()))
  return render(request, "director_tasks.html", context = default_director_context())



# post request
@user_passes_test(lambda user: user.is_superuser)
def create_task_to_staff(request):
    if not is_staff(request.POST.get("staff-name")):
        messages.error(request, "لا يوجد مسؤول بهذا الاسم")
    if not request.POST.get("task-subject"):
        messages.error(request, "يرجى كتابة موضوع المهمة")
    
    notification: List[dict] = notify_staff_user(request, request.POST.get("task-subject"))
    notification.emps.add(is_staff(request.POST.get("staff-name")))
    messages.success(request, "تم توجيه مسؤول الشعبة بنجاح")
    
    return HttpResponseRedirect("/tasks/")



# check if the employee (user) is in the admin (staff) group
def is_staff(staff_name) -> List[dict]:
    return User.objects.get(username=staff_name)



# create a new notification by the superuser to staff user
def notify_staff_user(request, message):
    return Notification.objects.create(
        user=request.user, 
        message=message
    )



# get all the director tasks
def get_all_notifications() -> List[dict]:
  return list(Notification.objects.prefetch_related("emp"))



# get the context dictionary
def get_director_context(request, tasks: List[dict]):
  return {
    "admins": get_all_staff(),
    "tasks": tasks,
  }



# in case when there is no notifications to return
def default_director_context():
  return {
    "admins": get_all_staff(),
    "tasks": "[]",
  }



# get all the staff user (not superusers)
def get_all_staff() -> List[dict]:
  return [
    user for user in User.objects.all().select_related("profile") 
    if user.is_staff and not user.is_superuser
  ]
